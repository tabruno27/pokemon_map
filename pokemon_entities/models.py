from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(default="default title")

    def __str__(self):
        return '{}'.format(self.title)