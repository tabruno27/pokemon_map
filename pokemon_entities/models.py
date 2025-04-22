from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='pokemon', default="default photo")
    description = models.TextField(blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='previous_evolutions')
    next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='next_evolutions')

    def __str__(self):
        return f'{self.title} ({self.title_ru}, {self.title_en}, {self.title_jp})'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at= models.DateTimeField(null=True)
    disappeared_at= models.DateTimeField(null=True)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    defence = models.IntegerField(default=10)
    stamina = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.pokemon.title} at ({self.lat}, {self.lon})"
