from logging import getLogger
from os.path import join, dirname, realpath

from noaa_tools.geo import get_us_location_from_lat_lon

logger = getLogger(__name__)

# NOAA Same Code URL: http://www.nws.noaa.gov/nwr/data/SameCode.txt

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
            self._map[state.lower()] = {}

        self._map[state][county] = same_code

    def find_same_code(self, state, county):
        state = state.lower()
        county = county.lower().split(' ')[0]

        if len(state) != 2:
            state = states[state]

        return self._map[state][county]


def load_nws_same_code_index():

    if load_nws_same_code_index.__index__ is not None:
        return load_nws_same_code_index.__index__

    same_code_file = join(dirname(realpath(__file__)), "resources", "noaa_same_codes.txt")

    content = []

    with open(same_code_file, "r") as f:
        content = f.readlines()

    load_nws_same_code_index.__index__ = SameCodeIndex()
    for entry in content:

        same_code, county, state = entry.strip().lower().split(',')
        same_code = same_code.strip(' ')
        county = county.strip(' ')
        state = state.strip(' ')

        load_nws_same_code_index.__index__.add(state, county, same_code)

    return load_nws_same_code_index.__index__

load_nws_same_code_index.__index__ = None


def get_same_code_for_lat_lon(lat, lon):
    location = get_us_location_from_lat_lon(lat, lon)

    same_code_by_state_and_county = load_nws_same_code_index()

    return same_code_by_state_and_county.find_same_code(location.state, location.county)

