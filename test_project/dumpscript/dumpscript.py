import json
import os
from collections import defaultdict
from typing import Dict

from django.db.models import Q


class DumpScript:

    DUMP_DATA_DIR = "dumped_data"

    def __init__(
            self, model_fields_map=None, id_export_models=None,
            models_to_exclude=None
    ):
        self.models_to_exclude = (
            models_to_exclude if models_to_exclude else [])
        self.model_fields_map = (
            model_fields_map if model_fields_map
            else self._get_models_fields_map_for_all_models())
        self.id_export_models = (
            id_export_models if id_export_models else [])

    def dump_data(self):
        dump_data_dir = self.DUMP_DATA_DIR
        self._create_dump_dir_if_not_exists(dump_data_dir)

        for model, query in self.model_fields_map.items():
            model_objects = self._get_model_objects(model, query)
            self._dump_model_objects_data(model_objects)
            self._dump_related_objects_data(model_objects)

        print("Data extracted successfully.")

    def _dump_related_objects_data(self, model_objects):
        related_objs = []
        for model_obj in model_objects:
            # noinspection PyProtectedMember
            fields = model_obj._meta.get_fields()
            pass

    def _dump_model_objects_data(self, model_objects):
        model_class_map = defaultdict(list)
        for obj in model_objects:
            model_class_map[obj.__class__].append(obj.__dict__)
        for model, obj_dicts in model_class_map.items():
            is_excluded_model = model in self.models_to_exclude
            if is_excluded_model:
                continue
            export_file_path, model_abs_path = self._get_export_file_details(
                model=model, dump_data_dir=self.DUMP_DATA_DIR)
            self._update_obj_dicts_based_on_config(obj_dicts, model)
            with open(export_file_path, "w+") as file:
                print("Dumping {} objects from {} model".format(
                    len(obj_dicts), model_abs_path))
                json.dump(obj_dicts, file, indent=4)

    def _get_model_objects(self, model, query):
        is_lookup_str = isinstance(query, Dict)
        is_query_obj = isinstance(query, Q)

        if is_lookup_str and query:
            model_queryset = model.objects.filter(**query)
        elif is_query_obj:
            model_queryset = model.objects.filter(query)
        else:
            model_queryset = model.objects.all()

        if not model_queryset:
            model_abs_path = self._get_model_abs_path(model)
            print(f"No records found from {model_abs_path} model.")
        return list(model_queryset)

    def _update_obj_dicts_based_on_config(self, obj_dicts, model):
        should_export_id = model in self.id_export_models
        # noinspection PyProtectedMember
        pk_name = model._meta.pk.name
        for obj_dict in obj_dicts:
            del obj_dict["_state"]
            if not should_export_id:
                del obj_dict[pk_name]

    @staticmethod
    def _create_dump_dir_if_not_exists(dump_data_dir):
        if not os.path.exists(dump_data_dir):
            os.makedirs(dump_data_dir)

    def _get_export_file_details(self, model, dump_data_dir):
        model_abs_path = self._get_model_abs_path(model)
        file_path = model_abs_path.replace('.', '_').lower() + ".json"
        file_path = os.path.join(dump_data_dir, file_path)
        return file_path, model_abs_path

    @staticmethod
    def _get_model_abs_path(model):
        model_abs_path = "{}.{}".format(
            model.__module__.split('.')[0], model.__qualname__)
        return model_abs_path

    def _get_models_fields_map_for_all_models(self):
        from django.apps import apps
        all_models_in_project = apps.get_models()
        filtered_models = list(
            set(all_models_in_project) - set(self.models_to_exclude))
        model_fields_map = {model: "" for model in filtered_models}
        return model_fields_map
