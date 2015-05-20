import os
import networkx as nx
# TODO: use decimals/floats for lat/lon -or- ints as in description?
#from decimal import Decimal, getcontext
from operator import itemgetter


class Gis:
    # Gis reads gis.dat, stores all of the information in appropriate data
    # structures, and then answers queries efficiently.
    def __init__(self):
        # check if the file exists
        assert os.path.exists('gis.dat'), 'gis.dat does not exist.'

        # Create an empty graph with no nodes or edges
        self.G = nx.Graph()
        self.H = nx.Graph()
        citylist = []
        citystate = ''

        with open('testgis.dat') as gisf:
            # getcontext().prec = 5
            for line in gisf.readlines():
                if line.startswith('*'):
                    continue
                line.strip()
                if line[0].isalpha():
                    (citystate, citydata) = line.split('[')
                    (city, state) = citystate.split(', ')
                    (latlon, pop) = citydata.split(']')
                    (lat, lon) = latlon.split(',')
                    # TODO: decide if the auxilliary 'name' attribute is needed.
                    self.G.add_node(citystate, state=state, name=citystate,
                                    latitude=int(lat),
                                    # float(Decimal(lat) * Decimal(0.01)),
                                    longitude=int(lon),
                                    population=int(pop.rstrip()))
                    citylist.insert(0, citystate)
                if line[0].isdigit():
                    i = 1
                    distlist = line.split()
                    for dist in distlist:
                        int(dist)
                        self.G.add_edge(citystate, citylist[i],
                                        weight=dist)
                        i += 1

        # Create list of all cities and edges for later use to avoid
        # reiterating through graph in subsequent functions calls.
        self.allCities = self.G.nodes(data=True)
        self.allEdges = self.G.edges(data=True)

    def selectCities(self, attribute, lowerBound, upperBound=None):
        # This method will be used to "select" a set of cities that satisfy
        # some conditions.
        # The argument attribute is a string that can be one of "name",
        # "state", "latitude", "longitude", and "population."
        # These examples should indicate to you that while attribute is
        # guaranteed to be a string, lowerBound and upperBound will have
        # different types, depending on the value of attribute.
        # An important property that selectCities is required to have is that
        # it selects only from those cities that are already selected. This
        # allows us to use selectCities repeatedly to select a set of cities
        # that satisfy several constraints.

        if upperBound is None:
            if type(lowerBound) is str:
                upperBound = lowerBound
            elif type(lowerBound) is int:
                upperBound = float("inf")

        # TODO: simplify/redo this scheme to eliminate cases

        # TODO: is there a way to turn 'name' and 'state' into int vals
        # generically?

        # TODO: Add type assertions?

        if attribute in {'name', 'state'}:
            if attribute is 'name':
                lowerBound = lowerBound.title()
                upperBound = upperBound.title()
            else:
                lowerBound = lowerBound[0:2].upper()
                upperBound = upperBound[0:2].upper()
        # TODO: I wonder if the above returns a soft copy, potentially
        # causing a problem with above if statement assigning upper to lower...
        # Maybe that should be copied rather than redirected?
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                      lowerBound <= a[attribute] <= upperBound
                                      or a[attribute].startswith(lowerBound
                                                                 or
                                                                 upperBound)])
        elif attribute in {'latitude', 'longitude', 'population'}:
            if attribute in {'latitude', 'longitude'}:
                lowerBound *= 100
                upperBound *= 100
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                      lowerBound <= a[attribute] <= upperBound])
        else:
            print('"{}" is not a valid attribute.\nPlease enter one of '
                  '"name", "state", "latitude", "longitude" or '
                  '"population".'.format(attribute))


    def selectAllCities(self):
        # Select all cities.
        # TODO: clean up this documentation
        # The allcities list created during initialization is iterated
        # through rather than iterating through calls to G as a matter of
        # computational efficiency.

        self.H.add_nodes_from(self.allCities)

    def unselectAllCities(self):
        # Un-select all cities.
        # TODO: clean up this documentation
        # Create a list of all cities in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # cities are iterated through, not all cities (a trade off of
        # computational efficiency for spatial efficiency).

        self.H.clear()

    def selectEdges(self, lowerBound, upperBound):
        # Here lowerBound and upperBound specify a "distance range."
        # For example, if lowerBound is set to 0 and upperBound is set to
        # 500, this method will select all edges between pairs of cities
        # whose distance (as specified in gis.dat) is at most 500 miles.
        # Assume that initially no edges are selected.
        #FIXME: this is edges you doofus
        self.H = self.H.subgraph([e for e, a in self.H.node.items() if
                                      lowerBound <= a['weight'] <= upperBound])

    def selectAllEdges(self):
        # Select all edges.
        # TODO: clean up this documentation
        # The alledges list created during initialization is iterated
        # through rather than iterating through calls to G as a matter of
        # computational efficiency.

        self.H.add_edges_from(self.allEdges)

    def unselectAllEdges(self):
        # Un-select all edges.
        # TODO: clean up this documentation
        # Create a list of all edges in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # edges are iterated through, not all edges (a trade off of
        # computational efficiency for spatial efficiency).

        self.H.remove_edges_from(self.H.edges())

    def makeGraph(self):
        # This method makes and returns a graph whose vertex set is the set of
        # selected cities and whose edge set is all selected edges connecting
        # pairs of selected cities.

        return self.H

    def printCities(self, attribute='name', choice='S'):
        # As before, attribute can be one of "name", "state", "latitude",
        # "longitude", and "population." This methods prints all selected
        # cities sorted in increasing order by the given attribute.
        # You should also implement printCities(), i.e., with no given
        # attribute, which should behave exactly like printCities("names").
        # The second parameter choice ('S' or 'F') determines whether the
        # requested output should be displayed in "short" form or "full" form.

        if choice is 'F':
            if attribute is 'name':
                for city in sorted(self.H.nodes()):
                    print("{} [{}, {}], {}".format(city,
                                                           self.H.node[city][
                                                               'latitude'],
                                                           self.H.node[city][
                                                               'longitude'],
                                                           self.H.node[city][
                                                               'population']))
            else:
                # TODO: Is nx.get_node_attributes(self.H, attribute)
                # equivalent to self.H.nodes(data=True) <- pulling only
                # 'attribute'?
                for city, d in sorted(nx.get_node_attributes(self.H,
                                                             attribute).items(),
                        key=itemgetter(1)):
                    print("{} [{}, {}], {}".format(city,
                                                           self.H.node[city][
                                                               'latitude'],
                                                           self.H.node[city][
                                                               'longitude'],
                                                           self.H.node[city][
                                                               'population']))
        else:
            if attribute is 'name':
                for city in sorted(self.H.nodes()):
                    print(city)
            else:
                for city, data in sorted(nx.get_node_attributes(self.H,
                                                                attribute).items(),
                        key=itemgetter(1)):
                    print("{}".format(self.H.node[city]['name']))

    def printEdges(self):
        # This should print all selected edges, in no particular order.

        # TODO: is this the format it should be in? No formatting, etc?
        for edge in self.H.edges():
            print(edge)

    def printPopulationDistr(self, value='range'):
        if value is 'range':
            pass

            """
            self.H.subgraph([c for c, a in self.H.node.items() if
                             lowerBound <= a['population'] <=
                             upperBound])
            i = 1
            count = 0
            for city in self.H.nodes(data=True):
                if self.H.node[city]['population'] <= i * 20000:
                    count += 1
                # call selectCities for each range!


           self.H = self.H.subgraph([c for c, a in self.H.node.items() if
           lowerBound <= a['population'] <= upperBound])
            """