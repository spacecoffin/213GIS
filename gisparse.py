import os
import re

if __name__ == '__main__':
    gisdat = 'gis.dat'

    # check if the file exists
    assert os.path.exists(gisdat), 'City data file \'%s\' does not ' \
                                   'exist.' % gisdat
    file = open(gisdat, 'r')

    # Problem: Do not read preamble as data.
    # Solution: If line begins with '*' char, go to the next line without
    # storing any data.

    # self.words = [w.rstrip('\n') for w in file.readlines()]
    # self.mapper = {}
    # self.keepwords = []

    file.close()