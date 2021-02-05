import random

import factory
from faker import Faker

from . import models

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


class PublicationArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Article.publications.through

    publication = factory.SubFactory(PublicationFactory)
    article = factory.SubFactory(ArticleFactory)


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
