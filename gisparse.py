import os
#import re

if __name__ == '__main__':
    gisdat = 'gis.dat'

    # check if the file exists
    assert os.path.exists(gisdat), 'City data file \'%s\' does not ' \
                                   'exist.' % gisdat
    file = open(gisdat, 'r')

    # Problem: Do not read preamble as data.
    # Solution: If line begins with '*' char, go to the next line without
    # storing any data.

    while True:
        line = file.readline()
        if not line:    # check for EOF
            break
        if line[0] is '*':
            continue
        else:
            line.strip()


    file.close()

    """
    wordch = []
    prevNonWhite = None
    period = '.'
    apostrophe = "'"
    while True:
        chr = file.read(1)
        if not chr:               # check if end-of-file
            if len(wordch) >= 2 and (wordch[0].islower() or prevNonWhite != '.'):
                addToWordList(''.join(wordch))
            break
        elif chr.isalpha():
            wordch.append(chr)
        elif chr is apostrophe and (len(wordch) >= 2 or wordch[0] == "I"):
            wordch.append(chr)
        elif chr is apostrophe:
            prevNonWhite = apostrophe
        elif prevNonWhite is apostrophe:
            wordch = []
            prevNonWhite = period if chr is period else None
        elif len(wordch) >= 2 and (wordch[0].islower() or prevNonWhite is period):
            addToWordList(''.join(wordch))
            wordch = []
            prevNonWhite = period if chr is period else None
        else:
            wordch = []
            prevNonWhite = period if chr is period else None
        finally:
            file.close()
    """




    # self.words = [w.rstrip('\n') for w in file.readlines()]
    # self.mapper = {}
    # self.keepwords = []