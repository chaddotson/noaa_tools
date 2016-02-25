from geopy import Point
from geopy.geocoders import Nominatim


def convert_lat_lon_to_geopy_location(lat_lon_as_string):
    geolocator = Nominatim()
    location = geolocator.reverse(Point(lat_lon_as_string))
    return location


def get_county_state_zip_from_location(geopy_location):
    return geopy_location.address.split(',')[3:6]
