#!/usr/bin/env python3

import unittest
import softcalc


class TestSoftCalc(unittest.TestCase):
    def test_calc_softban(self):
        coords_1 = (35.698610, 139.700667)
        coords_2 = (35.633132, 139.534768)
        d, s = softcalc.calc_softban(coords_1, coords_2)
        self.assertEqual(d, 16.685542971006623, "Distance is wrong")
        self.assertEqual(s, 11, "Softban is wrong")

    def test_coord_finder_two(self):
        t1 = """100iv & rai
        Coords : 25.025553,121.56185
        ChainRaids (https://twitter.com/hashtag/ChainRaids?src=hash&ref_src=twsrc%5Etfw)
        Taipei 🇹🇼

        Coords : 25.027401,121.533104

        Current Time 2
        2 min cooldown?ref_src=twsrc%5Etfw)"""
        coord_list = softcalc.coord_finder(t1)
        self.assertEqual(len(coord_list), 2, "Can't find both coords")
        self.assertEqual(coord_list[0], "25.025553,121.56185")
        self.assertEqual(coord_list[1], "25.027401,121.533104")

    def test_coord_finder_one(self):
        t2 = """100iv & rai
        Coords : 25.025553,121.56185
        ChainRaids (https://twi"""
        coord_list = softcalc.coord_finder(t2)
        self.assertEqual(len(coord_list), 1)
        self.assertEqual(coord_list[0], "25.025553,121.56185")

    def test_coord_finder_three(self):
        t3 = """Coords : 25.005743,121.519298 
Coords : 24.992623,121.548795
Coords : 25.048323,121.517228"""
        coord_list = softcalc.coord_finder(t3)
        self.assertEqual(len(coord_list), 3)
        self.assertEqual(coord_list[0], "25.005743,121.519298")
        self.assertEqual(coord_list[1], "24.992623,121.548795")
        self.assertEqual(coord_list[2], "25.048323,121.517228")
