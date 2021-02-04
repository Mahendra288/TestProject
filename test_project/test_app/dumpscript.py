import json
import os
from typing import Dict

from django.db.models import Q


class DumpScript:

    def __init__(self, model_fields_map, id_export_models=None):
        self.model_fields_map = model_fields_map
        self.id_export_models = (
            id_export_models if id_export_models else [])

    def dump_data(self):
        dump_data_dir = "dumped_data"
        self._create_dump_dir_if_not_exists(dump_data_dir)

        for model, query in self.model_fields_map.items():
            export_file_path, model_abs_path = self._get_export_file_details(
                model=model, dump_data_dir=dump_data_dir)
            model_objects = self._get_model_objects(
                model, query, model_abs_path)
            obj_dicts = [obj.__dict__ for obj in model_objects]
            self._update_obj_dicts_based_on_config(obj_dicts, model)
            self._dump_related_objects_data(model_objects)

            with open(export_file_path, "w+") as file:
                print("Dumping {} objects from {} model".format(
                    len(obj_dicts), model_abs_path))
                json.dump(obj_dicts, file, indent=4)
        print("Data extracted successfully.")

    @staticmethod
    def _get_model_objects(model, query, model_abs_path):
        is_lookup_str = isinstance(query, Dict)
        is_query_obj = isinstance(query, Q)

        if is_lookup_str and query:
            model_queryset = model.objects.filter(**query)
        elif is_query_obj:
            model_queryset = model.objects.filter(query)
        else:
            model_queryset = model.objects.all()

        if not model_queryset:
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

    @staticmethod
    def _get_export_file_details(model, dump_data_dir):
        model_abs_path = "{}.{}".format(
            model.__module__.split('.')[0], model.__qualname__)
        file_path = model_abs_path.replace('.', '_').lower() + ".json"
        file_path = os.path.join(dump_data_dir, file_path)
        return file_path, model_abs_path


from .models import Book

DumpScript(model_fields_map={Book: ""}).dump_data()
