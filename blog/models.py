from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords


class Slugable:
    slug_from_field = ""

    def save(self, *args, **kwargs):
      if not self.slug:
          self.slug = getattr(self, self.slug_from_field)
      return super().save(args, kwargs)


class Article(Slugable, models.Model):
    def upload_to(self, *args, **kwargs):
        return f"article/{self.uuid}"

    slug_from_field = "title"

    tags = models.ManyToManyField("ArticleTag", related_name="articles")
    title = models.CharField(max_length=150)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def summary(self):
        return strip_tags(truncatewords(self.body, 50))

    class Meta:
        ordering = ["-creation_date"]


class ArticleTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
