from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


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
