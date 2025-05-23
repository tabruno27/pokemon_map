from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, null=False, blank=True, verbose_name='Название (русский)')
    title_en = models.CharField(max_length=200, null=False, blank=True, verbose_name='Название (английский)')
    title_jp = models.CharField(max_length=200, null=False, blank=True, verbose_name='Название (японский)')
    photo = models.ImageField(upload_to='pokemon', default="default photo", null=True, blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционирует',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL)

    def __str__(self):
        return f'({self.title_ru}, {self.title_en}, {self.title_jp})'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=False, verbose_name='Покемон', related_name='entities')
    lat = models.FloatField(verbose_name='Широта', null=True, blank=True,)
    lon = models.FloatField(verbose_name='Долгота', null=True, blank=True,)
    appeared_at= models.DateTimeField(null=True, blank=True, verbose_name='Появился в')
    disappeared_at= models.DateTimeField(null=True,blank=True, verbose_name='Исчез в')
    level = models.IntegerField(default=1, null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(default=100, null=True, blank=True, verbose_name='Здоровье')
    health = models.IntegerField(default=100, null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(default=10, null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(default=10, null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(default=10, null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f"{self.pokemon.title_ru} at ({self.lat}, {self.lon})"
