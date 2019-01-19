#!/usr/bin/env python3

import re
import geopy.distance


def calc_softban(coords_1, coords_2):
    """
    Calculate distance and softban
    :param coords_1:
    :param coords_2:
    :return: distance in km and softban in minutes
    """
    dist = geopy.distance.distance(coords_1, coords_2).km
    softban = 120  # type: float in minutes
    if dist < 1:
        softban = 0.5
    elif 1 <= dist < 5:
        softban = 2
    elif 5 <= dist < 10:
        softban = 6
    elif 10 <= dist < 25:
        softban = 11
    elif 25 <= dist < 30:
        softban = 14
    elif 30 <= dist < 65:
        softban = 22
    elif 65 <= dist < 81:
        softban = 25
    elif 81 <= dist < 100:
        softban = 35
    elif 100 <= dist < 250:
        softban = 45
    elif 250 <= dist < 500:
        softban = 60
    elif 500 <= dist < 750:
        softban = 75
    elif 750 <= dist < 1000:
        softban = 90
    elif 1000 <= dist < 1500:
        softban = 120
    else:
        softban = 120
    return dist, softban


def coord_finder(text: str):
    """
    Parse input text and return list of found coords in text str
    :param text:
    :return:
    """
    search = re.findall('(?P<lat1>-?\d{1,3}[,.]\d{3,})[a-zA-Z,. \n]+(?P<long1>-?\d{1,3}[,.]\d{3,})', text)

    r = []
    for elem in search:
        # print(elem)
        if isinstance(elem, tuple):
            r.append(",".join(elem))
    return r


if __name__ == '__main__':
    t3 = """Coord1: 44.41398,8.883844
Coord2: 40.835965,73.89126"""
    t4 = """Coord1: -44.41398,8.883844
Coord2: 40.835965,-73.89126"""
    t5 = """19.431324, -99.427927, 40.835965,73.89126"""
    print(coord_finder(t3))
    print(coord_finder(t4))
    print(coord_finder(t5))
    print(calc_softban(*coord_finder(t5)))
