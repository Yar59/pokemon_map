from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('Русское название', max_length=200)
    title_en = models.CharField('Английское название', max_length=200)
    title_jp = models.CharField('Японское название', max_length=200)
    image = models.ImageField(
        'Картинка',
        null=True,
        blank=True,
        default='../media/no_image.jpg'
    )
    text = models.TextField('Описание покемона', null=True, blank=True)
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
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    attack = models.IntegerField('Атака')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')
