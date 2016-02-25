from logging import getLogger
import requests

from noaa_tools.errors import FailedToLoadNWSSameCodesMap
from noaa_tools.geo import convert_lat_lon_to_geopy_location, get_county_state_zip_from_location

logger = getLogger(__name__)

nws_same_code_url="http://www.nws.noaa.gov/nwr/data/SameCode.txt"

states = {
    'ak': 'alaska',
    'al': 'alabama',
    'ar': 'arkansas',
    'as': 'american samoa',
    'az': 'arizona',
    'ca': 'california',
    'co': 'colorado',
    'ct': 'connecticut',
    'dc': 'district of columbia',
    'de': 'delaware',
    'fl': 'florida',
    'ga': 'georgia',
    'gu': 'guam',
    'hi': 'hawaii',
    'ia': 'iowa',
    'id': 'idaho',
    'il': 'illinois',
    'in': 'indiana',
    'ks': 'kansas',
    'ky': 'kentucky',
    'la': 'louisiana',
    'ma': 'massachusetts',
    'md': 'maryland',
    'me': 'maine',
    'mi': 'michigan',
    'mn': 'minnesota',
    'mo': 'missouri',
    'mp': 'northern mariana islands',
    'ms': 'mississippi',
    'mt': 'montana',
    'na': 'national',
    'nc': 'north carolina',
    'nd': 'north dakota',
    'ne': 'nebraska',
    'nh': 'new hampshire',
    'nj': 'new jersey',
    'nm': 'new mexico',
    'nv': 'nevada',
    'ny': 'new york',
    'oh': 'ohio',
    'ok': 'oklahoma',
    'or': 'oregon',
    'pa': 'pennsylvania',
    'pr': 'puerto rico',
    'ri': 'rhode island',
    'sc': 'south carolina',
    'sd': 'south dakota',
    'tn': 'tennessee',
    'tx': 'texas',
    'ut': 'utah',
    'va': 'virginia',
    'vi': 'virgin islands',
    'vt': 'vermont',
    'wa': 'washington',
    'wi': 'wisconsin',
    'wv': 'west virginia',
    'wy': 'wyoming',
    'alabama': 'al',
    'alaska': 'ak',
    'american samoa': 'as',
    'arizona': 'az',
    'arkansas': 'ar',
    'california': 'ca',
    'colorado': 'co',
    'connecticut': 'ct',
    'delaware': 'de',
    'district of columbia': 'dc',
    'florida': 'fl',
    'georgia': 'ga',
    'guam': 'gu',
    'hawaii': 'hi',
    'idaho': 'id',
    'illinois': 'il',
    'indiana': 'in',
    'iowa': 'ia',
    'kansas': 'ks',
    'kentucky': 'ky',
    'louisiana': 'la',
    'maine': 'me',
    'maryland': 'md',
    'massachusetts': 'ma',
    'michigan': 'mi',
    'minnesota': 'mn',
    'mississippi': 'ms',
    'missouri': 'mo',
    'montana': 'mt',
    'national': 'na',
    'nebraska': 'ne',
    'nevada': 'nv',
    'new hampshire': 'nh',
    'new jersey': 'nj',
    'new mexico': 'nm',
    'new york': 'ny',
    'north carolina': 'nc',
    'north dakota': 'nd',
    'northern mariana islands': 'mp',
    'ohio': 'oh',
    'oklahoma': 'ok',
    'oregon': 'or',
    'pennsylvania': 'pa',
    'puerto rico': 'pr',
    'rhode island': 'ri',
    'south carolina': 'sc',
    'south dakota': 'sd',
    'tennessee': 'tn',
    'texas': 'tx',
    'utah': 'ut',
    'vermont': 'vt',
    'virgin islands': 'vi',
    'virginia': 'va',
    'washington': 'wa',
    'west virginia': 'wv',
    'wisconsin': 'wi',
    'wyoming': 'wy'
}

class SameCodeIndex(object):
    def __init__(self):
        self._map = {}

    def add(self, state, county, same_code):
        same_code = same_code.strip(' ').lower()
        county = county.strip(' ').lower()
        state = state.strip(' ').lower()

        if state not in self._map:
            self._map[state] = {}

        self._map[state][county] = same_code

    def find_same_code(self, state, county):

        if len(state) != 2:
            state = states[state]

        return self._map[state][county]


def get_nws_same_codes_map():

    response = requests.get(nws_same_code_url);

    if response.status_code != 200:
        e = FailedToLoadNWSSameCodesMap(response.status_code)
        logger.exception(e)
        raise e

    # TODO: what to do when it fails!

    content = response.text.splitlines()

    same_code_index = SameCodeIndex()
    for entry in content:
        same_code, county, state = entry.split(',')
        same_code = same_code.strip(' ').lower()
        county = county.strip(' ').lower()
        state = state.strip(' ').lower()

        same_code_index.add(state, county, same_code)

    return same_code_index


def get_same_code_for_lat_lon(lat_lon_as_string):
    location = convert_lat_lon_to_geopy_location(lat_lon_as_string)
    county, state, zip_code = get_county_state_zip_from_location(location)

    county = county.replace("County",'').strip(' ').lower()
    state = state.strip(' ').lower()
    zip_code = zip_code.strip(' ')

    same_code_by_state_and_county = get_nws_same_codes_map()

    return same_code_by_state_and_county.find_same_code(state, county)
