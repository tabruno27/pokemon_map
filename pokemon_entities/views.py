import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils import timezone


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
    current_time = timezone.localtime()
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
        for pokemon_entity in pokemon_entities:
            if pokemon_entity.appeared_at <= current_time <= pokemon_entity.disappeared_at:
                add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(pokemon.photo.url)
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    previous_evolution_data = None
    if requested_pokemon.previous_evolution:
        previous_evolution_data = {
            'title_ru': requested_pokemon.previous_evolution.title_ru,
            'title_en': requested_pokemon.previous_evolution.title_en,
            'title_jp': requested_pokemon.previous_evolution.title_jp,
            'img_url': request.build_absolute_uri(requested_pokemon.previous_evolution.photo.url),
            'pokemon_id': requested_pokemon.previous_evolution.id,
        }

    next_evolution_data  = None
    if requested_pokemon.next_evolution:
        next_evolution_data = {
            'title_ru': requested_pokemon.next_evolution.title_ru,
            'title_en': requested_pokemon.next_evolution.title_en,
            'title_jp': requested_pokemon.next_evolution.title_jp,
            'img_url': request.build_absolute_uri(requested_pokemon.next_evolution.photo.url),
            'pokemon_id': requested_pokemon.next_evolution.id,
        }

    pokemon_data = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        "pokemon_id": requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.photo.url),
        'description': requested_pokemon.description,
        'previous_evolution': previous_evolution_data,
        'next_evolution': next_evolution_data,
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in requested_pokemon.pokemonentity_set.all():
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_data['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data,
    })