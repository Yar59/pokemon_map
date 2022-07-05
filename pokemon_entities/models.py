from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('Русское название', max_length=200)
    title_en = models.CharField('Английское название', max_length=200, blank=True)
    title_jp = models.CharField('Японское название', max_length=200, blank=True)
    image = models.ImageField(
        'Картинка',
        blank=True,
        default='../media/no_image.jpg'
    )
    text = models.TextField('Описание покемона', blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Предыдущая эволюция',
        blank=True,
        null=True,
        related_name='next_evolutions',
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities',
    )
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    attack = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)
