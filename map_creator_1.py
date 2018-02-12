import folium
from geopy import Nominatim
from euro_countries1 import  countries


def create_map():
    """
      -> None
    This function inputs a year of film creation and maximum amount of films on a map and creates file with
    map with films
    """
    year, number_coordinates = input_year_and_place()
    film_list = search_by_year(year, number_coordinates)
    with_coord = add_coordinates_and_area(film_list)
    save_map(with_coord)
    print('Map generation is finished. Please, open file "Map.html"')
def input_year_and_place():
    """
    ->(int, int)
    This function returns number of places and year
    """
    year = int(input("Enter year:"))
    number_coordinates = int(input("Enter maximal number of places:"))
    return (year, number_coordinates)
def process_film(film):
    """
    (str) -> (tuple)
    This function processes film and returns it in view of tuple (year, film, place)
    """
    film = film.split()
    name = ''
    year = ''
    episode = ''
    place = ''
    name = film[0]
    del film[0]
    if name.count('"') == 1:
        while name.count('"') != 2:
            name += ' ' + film[0]
            del film[0]
    year = film[0][1:-1]
    del film[0]
    if '{' not in film[0]:
        episode = '-'
    else:
        episode = film[0]
        del film[0]
        if '{' in episode and '}' not in episode:
            while '{' in episode and '}' not in episode:
                episode += ' ' + film[0]
                del film[0]
        episode = episode[1:-1]
    place = ' '.join(film)
    if '(' in place and ')' in place:
        while '(' in place:
            place = place[:-1]
        place = place[:-1]
    return (year, name, place)
def search_by_year(year, number_coordinates):
    """
    (int, int) -> list((tuple(str, str)))
    This function inputs year and number of coordinates and outputs list of films with given year with place and
    in list not longer then number of coordinates
    """
    year = str(year)
    film_list = []
    with open('locations.list', 'r', encoding='utf-8', errors='ignore') as data:
        read = False
        for line in data:
            if read:
                if len(film_list) >= number_coordinates:
                    break
                else:
                    film = line
                    if film:
                        film = process_film(line)
                        if film[0] == year:
                            film_list.append(film[1:])
            elif '==============' in line:
                read = True
    return  film_list
def define_area(country):
    """
    (str) -> (str)
    This function outputs 'Europe' if country is european, 'USA" if country is 'United States of America" else
    'other'
    """
    if country in countries or country[1:] in countries:
        return "Europe"
    elif country in ' United States of America':
        return "USA"
    else:
        return "other"
def find_coordinates(place):
    """
    (str) -> (tuple)
    This function inputs name of place and returns tuple with it`s coordinates
    """
    geolocator = Nominatim()
    location = geolocator.geocode(place, timeout=138)
    if location:
        return (location.latitude, location.longitude, location.raw['display_name'].split(',')[-1])
def add_coordinates_and_area(film_list):
    """
    (list) -> (dict)
    This function inputs coordinates and outputs it as a dictionary with region as key and dictiondary with keys
    'name' and 'coordinates'
    """
    film_list_1 = []
    for i, j  in enumerate(film_list):
        name = j[0]
        place = find_coordinates(j[1])
        if place:
            film_list_1.append((define_area(place[2]), name, place[:2]))
    film_dict = {}
    for i in film_list_1:
        if i[0] in film_dict:
            film_dict[i[0]].append({'name':i[1], 'coordinates':i[2]})
        else:
            film_dict[i[0]] = [{'name':i[1], 'coordinates':i[2]}]
    return film_dict
def save_map(film_dict):
    """
    (dict) -> None
    This function inputs film dictionary and saves map in file
    """
    map_films = folium.Map()
    for i in film_dict:
        group = folium.FeatureGroup(name = i)
        for j in film_dict[i]:
            group.add_child(folium.Marker(list(j['coordinates']), popup=j['name'],
                                              icon=folium.Icon(color='blue', icon='info-sign')))
        map_films.add_child(group)
    map_films.add_child(folium.LayerControl())
    map_films.save('Map.html')


create_map()