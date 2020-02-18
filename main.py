from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import pandas
import doctest


def get_film_location(path: str, search_year: int) -> dict:
    '''
    (str), (int) -> (dict)
    Returns a dictionary from a file where film location
    is a key and film title is the value.
    '''
    film_dict = {}
    with open(path, 'r', encoding="utf-8", errors='ignore') as f:
        for line in f:
            line = line.strip().split('\t')
            for index in range(len(line[0])):
                if line[0][index] == '(':
                    film_year = line[0][index+1:index+5]
                    if film_year.isdigit():
                        if int(film_year) == search_year:
                            film_title = line[0][:index]
                            film_location = line[-2] if line[-1][-1] == ')' else line[-1]
                            film_dict[film_location] = film_dict.get(
                                film_location, []) + [film_title]
                            break
    return film_dict


def get_country_location(location: str) -> str:
    '''
    (str) -> (str)
    Returns the name of the country by the coordinates.
    >>> get_country_location((49.83826, 24.02324))
    'Ukraine'
    '''
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    address = geolocator.reverse(location, language='en')
    country = address.raw['address']['country']
    return country


def check_country(country: str, location_dict: dict, your_location: tuple):
    '''
    (str), (dict) -> (list)
    Returns sorted list of films with their coordinates and distance to
    your location. (sorted by the distance to your location)
    '''
    country_set = set()
    Limit = 20
    for key in location_dict:
        if country in key:
            if Limit < 0:
                break
            try:
                Limit -= 1
                location = geolocator.geocode(key)
                coordinates = (location.latitude, location.longitude)
                distance = (
                    round(geodesic(your_location, coordinates).km, 0))
                country_set.add((distance, location_dict[key][0], coordinates))
            except AttributeError:
                pass
    country_set = sorted(list(country_set))
    country_set.sort()
    country_set = country_set[:10]
    return country_set


def draw_films(country_list: str):
    '''
    Draws given films on the map.
    '''
    for film in country_list:
        fg.add_child(folium.Marker(location=[film[2][0], film[2][1]],
                                   popup=film[1],
                                   icon=folium.Icon()))


def capitals(path: str):
    '''
    Draws markers on the map that show the capitals of all countries.
    '''
    data = pandas.read_csv(path)
    country = data['CountryName']
    capital = data['CapitalName']
    latitude = data['CapitalLatitude']
    longtitude = data['CapitalLongitude']
    for ct, cp, lt, ln in zip(country, capital, latitude, longtitude):
        fg.add_child(folium.CircleMarker(location=[lt, ln],
                                         radius=5,
                                         popup=cp,
                                         fill_color='green',
                                         color='green',
                                         fill_opacity=0.5))
    map.add_child(fg)


if __name__ == '__main__':
    doctest.testmod()
    input_year = int(
        input('Please enter a year you would like to have a map for: '))
    input_location = input(
        'Please enter your location (format: lat, long): ').split(', ')
    input_location = (float(input_location[0]), float(input_location[1]))
    print('Map is generating...\nPlease wait...')

    diction = get_film_location('locations.list', input_year)
    country = get_country_location(input_location)

    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)

    country_list = check_country(country, diction, input_location)

    map = folium.Map()
    fg = folium.FeatureGroup(name="Film_map")
    draw_films(country_list)
    capitals("country-capitals.csv")
    map.save(str(input_year) + '_Map.html')

    print(f'Finished. Please have look at the map {str(input_year)}_Map.html')
