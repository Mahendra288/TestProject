import factory
from django.db import transaction

from . import factories


@transaction.atomic
def populate_data():
    no_of_reporters = 99
    no_of_articles = 9999
    no_of_publications = 9
    no_of_affiliate_publications_for_each_pub = 9
    no_of_sponsors = 999

    # create and store some reporters
    print(f"creating {no_of_reporters} reporters.")
    reporters = factories.ReporterFactory.create_batch(size=no_of_reporters)

    # create and store some articles by linking the above reporters
    print(f"creating {no_of_articles} articles for reporters.")
    articles = factories.ArticleFactory.create_batch(
        size=no_of_articles, reporter=factory.Iterator(reporters))

    # create and store some publications for affiliates
    affiliate_publications = factories.PublicationFactory.create_batch(
        size=no_of_publications * no_of_affiliate_publications_for_each_pub)

    # create and store some publications
    publications = factories.PublicationFactory.create_batch(
        size=no_of_publications,
        affiliate=factory.Iterator(affiliate_publications))
    publications = publications + affiliate_publications

    # set some batch of publications randomly to every article
    factories.PublicationArticleFactory.create_batch(
        size=no_of_articles,
        publication=factory.Iterator(publications),
        article=factory.Iterator(articles))

    # create and store some sponsors
    sponsors = factories.SponsorFactory.create_batch(no_of_sponsors)

    # create and store sponsor publications
    factories.PublicationSponsorFactory.create_batch(
        size=no_of_sponsors, sponsor=factory.Iterator(sponsors),
        publication=factory.Iterator(publications))

    # create reporter bios for every reporter
    factories.ReporterBioFactory.create_batch(
        size=no_of_reporters, reporter=factory.Iterator(reporters))

    from django.contrib.auth.models import User
    User.objects.create_superuser(username="user", password="user")
