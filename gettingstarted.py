#!/bin/python


from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO, DEBUG
#
# from noaa_tools.geo import convert_lat_lon_to_geopy_location, get_county_state_zip_from_location

from noaa_tools.same_codes import get_same_code_for_lat_lon

basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = getLogger(__name__)

def get_args():
    parser = ArgumentParser(description='GPS tuple to SAMECODE')
    parser.add_argument('gps_coord_tuple', help='GPS Coordinate Tuple')
    # parser.add_argument('-v', '--verbose', help='Verbose log output', default=False, action='store_true')
    return parser.parse_args()

from noaa_tools.same_codes import get_nws_same_codes_map

def main():
    args = get_args()

    logger.info("Converting: %s", args.gps_coord_tuple)


    print(get_same_code_for_lat_lon(args.gps_coord_tuple))
    #
    # location = convert_lat_lon_to_geopy_location(args.gps_coord_tuple)
    # county, state, zip_code = get_county_state_zip_from_location(location)
    #
    # county = county.replace("County",'').strip(' ').lower()
    # state = state.strip(' ').lower()
    # zip_code = zip_code.strip(' ')
    #
    # same_code_by_state_and_county = get_nws_same_codes_map()
    #
    # # from pprint import pprint
    # #
    # # pprint(states)
    #
    #
    # print(same_code_by_state_and_county.find_same_code(state, county))



if __name__ == "__main__":
    main()
