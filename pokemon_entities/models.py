from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(default="default photo")

    def __str__(self):
        return '{}'.format(self.title)

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at= models.DateTimeField(null=True)
    disappeared_at= models.DateTimeField(null=True)