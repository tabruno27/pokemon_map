from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    title_ru = models.CharField(max_length=200, verbose_name='Название (русский)')
    title_en = models.CharField(max_length=200,verbose_name='Название (английский)')
    title_jp = models.CharField(max_length=200, verbose_name='Название (японский)')
    photo = models.ImageField(upload_to='pokemon', default="default photo", verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='previous_evolutions', verbose_name='Предыдущая эволюция')
    next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='next_evolutions', verbose_name='Следующая эволюция')

    def __str__(self):
        return f'{self.title} ({self.title_ru}, {self.title_en}, {self.title_jp})'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at= models.DateTimeField(null=True, verbose_name='Появился в')
    disappeared_at= models.DateTimeField(null=True, verbose_name='Исчез в')
    level = models.IntegerField(default=1, verbose_name='Уровень')
    health = models.IntegerField(default=100, verbose_name='Здоровье')
    strength = models.IntegerField(default=10, verbose_name='Сила')
    defence = models.IntegerField(default=10,verbose_name='Защита')
    stamina = models.IntegerField(default=10, verbose_name='Выносливость')

    def __str__(self):
        return f"{self.pokemon.title} at ({self.lat}, {self.lon})"
