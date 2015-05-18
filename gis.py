import os
import networkx as nx
from decimal import Decimal, getcontext
from operator import itemgetter


class Gis:
    # Gis reads gis.dat, stores all of the information in appropriate data
    # structures, and then answers queries efficiently.
    def __init__(self):
        # check if the file exists
        assert os.path.exists('gis.dat'), 'gis.dat does not exist.'

        # Create an empty graph with no nodes or edges
        self.G = nx.Graph()
        self.citylist = []
        citystate = ''
        getcontext().prec = 5

        with open('testgis.dat') as gisf:
            getcontext().prec = 5
            for line in gisf.readlines():
                if line.startswith('*'):
                    continue
                line.strip()
                if line[0].isalpha():
                    (citystate, citydata) = line.split('[')
                    (city, state) = citystate.split(', ')
                    (latlon, pop) = citydata.split(']')
                    (lat, lon) = latlon.split(',')
                    self.G.add_node(citystate, state=state, name=citystate,
                               latitude=float(Decimal(lat) * Decimal(0.01)),
                               longitude=float(Decimal(lon) * Decimal(0.01)),
                               population=int(pop.rstrip()))
                    self.citylist.insert(0, citystate)
                if line[0].isdigit():
                    i=0
                    distlist = line.split()
                    for dist in distlist:
                        int(dist)
                        self.G.add_edge(citystate, self.citylist[i],
                                        weight=dist)
                        i=i+1

        self.H = self.G
        #self.allcities = self.G.nodes()
        #self.allcities.sort()
        self.citylist.sort()
        self.alledges = self.G.edges()

    def selectCities(self, attribute, lowerBound, upperBound):
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

        if attribute is 'name':
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                      ord(lowerBound[0]) <= ord((a['name'])[0])
                                      <= ord(upperBound[0])])
        elif attribute is 'state':
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                      ord(lowerBound[0]) <= ord((a['state'])[0])
                                      <= ord(upperBound[0])])
        elif attribute is 'latitude':
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                    lowerBound <= a['latitude'] <= upperBound])
        elif attribute is 'longitude':
            self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                    lowerBound <= a['longitude'] <= upperBound])
        elif attribute is 'population':
           self.H = self.H.subgraph([c for c, a in self.H.node.items() if
                                    lowerBound <= a['population'] <=
                                    upperBound])
        else:
            print('"{}" is not a valid attribute.\nPlease enter one of '
                  '"name", "state", "latitude", "longitude" or '
                  '"population".'.format(attribute))

    def selectAllCities(self):
        # Select all cities.
        # The allcities list created during initialization is iterated
        # through rather than iterating through calls to G as a matter of
        # computational efficiency.
        self.H.add_nodes_from(self.citylist)

    def unselectAllCities(self):
        # Un-select all cities.
        # Create a list of all cities in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # cities are iterated through, not all cities (a trade off of
        # computational efficiency for spatial efficiency).
        nlist = self.H.nodes()
        self.H.remove_nodes_from(nlist)

    def selectEdges(self, lowerBound, upperBound):
        # Here lowerBound and upperBound specify a "distance range."
        # For example, if lowerBound is set to 0 and upperBound is set to
        # 500, this method will select all edges between pairs of cities
        # whose distance (as specified in gis.dat) is at most 500 miles.
        # Assume that initially no edges are selected.

        return ()

    def selectAllEdges(self):
        # Select all edges.
        # The alledges list created during initialization is iterated
        # through rather than iterating through calls to G as a matter of
        # computational efficiency.
        self.H.add_edges_from(self.alledges)

    def unselectAllEdges(self):
        # Un-select all edges.
        # Create a list of all edges in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # edges are iterated through, not all edges (a trade off of
        # computational efficiency for spatial efficiency).
        elist = self.H.edges()
        self.H.remove_edges_from(elist)

    def makeGraph(self):
        # This method makes and returns a graph whose vertex set is the set of
        # selected cities and whose edge set is all selected edges connecting
        # pairs of selected cities.
        # Using algorithms studied in class, we can find out if in such a
        # graph it is possible to travel from any "high population" city to
        # any other "high population" city, without visiting any "low
        # population" city and furthermore using only hops of length at most
        # 200 miles.

        return ()

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
                    print("{} [{:.2f}, {:.2f}], {}".format(city,
                                                self.H.node[city]['latitude'],
                                                self.H.node[city]['longitude'],
                                                self.H.node[city]['population']))
            else:
                for city, data in sorted(nx.get_node_attributes(self.H,
                                        attribute).items(), key=itemgetter(1),
                                        reverse=True):
                    print("{} [{:.2f}, {:.2f}], {}".format(city,
                                                self.H.node[city]['latitude'],
                                                self.H.node[city]['longitude'],
                                                self.H.node[city]['population']))
        else:
            if attribute is 'name':
                for city in sorted(self.H.nodes()):
                    print(city)
            else:
                for city, data in sorted(nx.get_node_attributes(self.H,
                                        attribute).items(), key=itemgetter(1),
                                        reverse=True):
                    print("{}".format(self.H.node[city]['name']))

    def printEdges(self):
        # This should print all selected edges, in no particular order.

        return ()