import factory

from .models import Author, Book


class AuthorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: "Author {}".format(n))


class BookFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Book

    name = factory.Sequence(lambda n: "Book {}".format(n))
    price = factory.Sequence(lambda n: n)
    author = factory.SubFactory(AuthorFactory)
