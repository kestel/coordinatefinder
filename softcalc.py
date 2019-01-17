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
    search = re.findall('(?P<lat1>\d{1,3}[,.]\d{3,})\D*(?P<long1>\d{1,3}[,.]\d{3,})', text)

    r = []
    for elem in search:
        if isinstance(elem, tuple):
            r.append(",".join(elem))
    return r


if __name__ == '__main__':
    t1 = """100iv & raid by Pokémon Go Fly Italy, [17.01.19 09:30]
Groudon Raid No.10 #ChainRaids (https://twitt
Taipei 🇹🇼

Coords : 25.025553,121.56185

Current Time 24 min
Join on 22


100iv & raid by Pokémon Go Fly Italy, [17.01.19 09:33]
Groudon Raid No.11#ChainRaids (https://twitter.com/hashtaref_src=twsrc%5Etfw)
Taipei 🇹🇼

Coords : 25.027401,121.533104

Current Time 28 min
Join on 26
8?ref_src=twsrc%5Etfw)"""
    t2 = """Latitude
40.741895
Longitude
-73.989308
"""
    t3 = """Coord1: 44.41398,8.883844
Coord2: 40.835965,73.89126"""
    coord_list = coord_finder(t1)
    if len(coord_list) == 2:
        d, s = calc_softban(*coord_list)
        print("D2: {}".format(d))
        print("S2: {}".format(s))
    elif len(coord_list) == 1:
        print(coord_list[0])
    print(coord_finder(t2))
    print(calc_softban(*coord_finder(t3)))
    coords_1 = (35.698610, 139.700667)
    coords_2 = (35.633132, 139.534768)

    d, s = calc_softban(coords_1, coords_2)
    print("Distance: {}".format(d))
    print("Softban: {}".format(s))
