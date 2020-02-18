from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import pandas


def get_film_location(path: str, search_year: int) -> dict:
    '''
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


def capitals(path):
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


def check_country(country, location_dict, your_location):
    country_set = set()
    Limit = 100
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
            except:
                pass
    country_set = sorted(list(country_set))
    country_set.sort()
    country_set = country_set[:10]
    return country_set


def get_coordinates_location(location):
    address = geolocator.reverse(location, language='en')
    country = address.raw['address']['country']
    return country


if __name__ == '__main__':
    input_year = int(
        input('Please enter a year you would like to have a map for: '))
    input_location = input(
        'Please enter your location (format: lat, long): ').split(', ')
    input_location = (float(input_location[0]), float(input_location[1]))
    diction = get_film_location('locations.list', input_year)
    country = get_coordinates_location(input_location)
    print(country)
    country_list = check_country(country, diction, input_location)
    print(country_list)
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    map = folium.Map()
    fg = folium.FeatureGroup(name="Kosiv map")
    for film in country_list:
        fg.add_child(folium.Marker(location=[film[2][0], film[2][1]],
                                   popup=film[1],
                                   icon=folium.Icon()))
    capitals("country-capitals.csv")
    map.save('Map_5.html')
    print('Map is generating...\nPlease wait...')
