import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:
        appeared_at = timezone.localtime(pokemon_entity.appeared_at)
        disappeared_at = timezone.localtime(pokemon_entity.disappeared_at)
        time_now = timezone.now()
        if appeared_at < time_now < disappeared_at:
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            add_pokemon(
                folium_map,
                pokemon_entity.latitude,
                pokemon_entity.longitude,
                image_url
            )
    pokemons_for_page = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_for_page:
        try:
            image_url = request.build_absolute_uri(pokemon.image.url)
        except ValueError:
            image = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        appeared_at = timezone.localtime(pokemon_entity.appeared_at)
        disappeared_at = timezone.localtime(pokemon_entity.disappeared_at)
        time_now = timezone.now()
        if appeared_at < time_now < disappeared_at:
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            add_pokemon(
                folium_map,
                pokemon_entity.latitude,
                pokemon_entity.longitude,
                image_url
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
