import random

import factory
from faker import Faker

from test_project.test_app import models

fake_generator = Faker()


class ReporterFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Reporter

    first_name = fake_generator.first_name()
    last_name = fake_generator.last_name()

    @factory.LazyAttribute
    def email(self):
        return f"{self.last_name}{self.first_name}@gmail.com"


class ArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Article

    headline = fake_generator.text()
    reporter = factory.SubFactory(ReporterFactory)


class PublicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Publication

    title = fake_generator.company()


class SponsorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Sponsor

    name = f"{fake_generator.last_name()} {fake_generator.first_name()}"
    budget_in_crores = round(random.uniform(9, 999), 2)


class PublicationSponsorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.PublicationSponsor

    publication = factory.SubFactory(PublicationFactory)
    sponsor = factory.SubFactory(SponsorFactory)
    invested_amount = round(random.uniform(9, 999), 2)


class ReporterBioFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.PublicationSponsor

    reporter = factory.SubFactory(ReporterFactory)
    address = fake_generator.address()
    no_of_articles_written = random.randint(9, 99)


def populate_data():

    # create and store some reporters
    # create and store some articles by linking the above reporters
    # create and store some publications
    # create and store some publications for affiliates
    # set affiliates for some publications
    # set some batch of publications randomly to every article
    # create and store some sponsors
    # create and store sponsor publications
    # with above publications ans sponsors
    # create reporter bios for every reporter
    pass
