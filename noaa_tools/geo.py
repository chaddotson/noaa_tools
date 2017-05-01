from collections import namedtuple
from geopy import Point
from geopy.geocoders import Nominatim


def convert_lat_lon_to_geopy_location(lat_lon_as_string):
    geolocator = Nominatim()
    location = geolocator.reverse(Point(lat_lon_as_string))
    return location


USLocation = namedtuple("USLocation", field_names=['city', 'county', 'state', 'zip'])


def get_us_location_from_lat_lon(lat, lon):
    geopy_location = convert_lat_lon_to_geopy_location("{0},{1}".format(lat, lon))
    return USLocation(*map(lambda x: x.strip(), geopy_location.address.split(',')[1:5]))
