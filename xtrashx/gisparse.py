import os

def gisread():
    with open('gis.dat', 'r') as gisfile:
        for line in gisfile:
            line.rstrip()
            if line and not line.startswith('*'):
                yield line

if __name__ == '__main__':

    # check if the file exists
    assert os.path.exists('gis.dat'), \
        'City data file \'gis.dat\' does not exist.'

    gisfile = open('gis.day', 'r')

    for line in open('gis.day', 'r'):
        line.rstrip()
        if line and not line.startswith('*'):
