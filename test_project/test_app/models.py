from django.db import models


class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(
        "Publication", related_name="articles")
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


class Publication(models.Model):
    title = models.CharField(max_length=30)
    affiliate = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="affiliates",
        null=True, blank=True)
    sponsors = models.ManyToManyField("Sponsor", through="PublicationSponsor")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    budget_in_crores = models.FloatField()


class PublicationSponsor(models.Model):
    publication = models.ForeignKey("Publication", on_delete=models.CASCADE)
    sponsor = models.ForeignKey("Sponsor", on_delete=models.CASCADE)
    invested_amount = models.FloatField()

    def __str__(self):
        return "{} invested {} on {}".format(
            self.sponsor.name, self.invested_amount, self.publication.name)


class ReporterBio(models.Model):
    reporter = models.OneToOneField(Reporter, on_delete=models.CASCADE)
    address = models.TextField()
    no_of_articles_written = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.reporter.name} Bio"
