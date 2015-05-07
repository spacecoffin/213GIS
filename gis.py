import networkx as nx
import os

class Gis:
    # Gis reads gis.dat, stores all of the information in appropriate data
    # structures, and then answers queries efficiently.
    def __init__(self, gisdat='gis.dat'):
        # check if the file exists
        assert os.path.exists(gisdat), 'City data file \'%s\' does not ' \
                                       'exist.' % gisdat
        file = open(gisdat, 'r')
        self.words = [w.rstrip('\n') for w in file.readlines()]
        self.mapper = {}
        self.keepwords = []

        file.close()

    def selectCities(attribute, lowerBound, upperBound):
        # This method will be used to “select” a set of cities that satisfy
        # some conditions.
        # The argument attribute is a string that can be one of “name”,
        # “state”, “latitude”, “longitude”, and “population.”
        # These examples should indicate to you that while attribute is
        # guaranteed to be a string, lowerBound and upperBound will have
        # different types, depending on the value of attribute.
        # An important property that selectCities is required to have is that
        # it selects only from those cities that are already selected. This
        # allows us to use selectCities repeatedly to select a set of cities
        # that satisfy several constraints.

        return()

    def selectAllCities(self): # self?
        # These methods respectively select and un-select all cities.

        return()

    def unselectAllCities(self): # self?
        # These methods respectively select and un-select all cities.

        return()

    def selectEdges(lowerBound, upperBound):
        # Here lowerBound and upperBound specify a "distance range."
        # For example, if lowerBound is set to 0 and upperBound is set to
        # 500, this method will select all edges between pairs of cities
        # whose distance (as specified in gis.dat) is at most 500 miles.
        # Assume that initially no edges are selected.

        return()

    def selectAllEdges(self): # self?
        # These methods respectively select and un-select all edges.

        return()

    def unselectAllEdges(self): # self?
        # These methods respectively select and un-select all edges.

        return()

    def makeGraph(self):
        # This method makes and returns a graph whose vertex set is the set of
        # selected cities and whose edge set is all selected edges connecting
        # pairs of selected cities.
        # Using algorithms studied in class, we can find out if in such a
        # graph it is possible to travel from any "high population" city to
        # any other “high population” city, without visiting any "low
        # population" city and furthermore using only hops of length at most
        # 200 miles.

        return()

    def printCities(attribute, choice):
        # As before, attribute can be one of "name", "state", "latitude",
        # "longitude", and "population." This methods prints all selected
        # cities sorted in increasing order by the given attribute.
        # You should also implement printCities(), i.e., with no given
        # attribute, which should behave exactly like printCities("names").
        # The second parameter choice ('S' or 'F') determines whether the
        # requested output should be displayed in "short" form or "full" form.

        return()

    def printEdges(self):
        # This should print all selected edges, in no particular order.

        return()