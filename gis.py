import os
import networkx as nx
from operator import itemgetter


class Gis:
    # Gis reads gis.dat, stores all of the information in appropriate data
    # structures, and then answers queries efficiently.
    def __init__(self):
        # check if the file exists
        assert os.path.exists('gis.dat'), 'gis.dat does not exist.'

        # Create empty dictionaries to be filled with all cities and edges
        self.allCities = dict()
        self.allEdges = []

        # Create empty dictionaries to be used for selected cities and edges
        self.selCities = dict()
        self.selEdges = []

        # Create empty list to iterate through in parsing of edges
        citylist = []
        # Preempt "referenced before assignment" complaint in 2nd 'if' below
        name = ''
        i = 1

        with open('testgis.dat') as gisf:
            for line in gisf.readlines():
                if line.startswith('*'):
                    continue
                line.strip()
                if line[0].isalpha():
                    i = 1
                    (name, citydata) = line.split('[')
                    (city, state) = name.split(', ')
                    (latlon, pop) = citydata.split(']')
                    (lat, lon) = latlon.split(',')
                    self.allCities[name] = dict(zip([
                        'name', 'state', 'latitude', 'longitude', 'population'],
                        [name, state, int(lat), int(lon), int(pop.rstrip())]))
                    citylist.insert(0, name)
                if line[0].isdigit():
                    distlist = line.split()
                    for dist in distlist:
                        self.allEdges.insert(i-1, (name, citylist[i], int(dist)))
                        i += 1

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

        if attribute in {'name', 'state'}:
            if attribute is 'name':
                lowerBound = lowerBound.title()
                upperBound = upperBound.title()
            else:
                lowerBound = lowerBound[0:2].upper()
                upperBound = upperBound[0:2].upper()

            self.selCities = {c: d for (c, d) in self.selCities.items() if
                              lowerBound <= self.selCities[c][attribute] <=
                              upperBound or self.selCities[c][
                                  attribute].startswith(lowerBound or
                                                        upperBound)}
        elif attribute in {'latitude', 'longitude', 'population'}:
            if attribute in {'latitude', 'longitude'}:
                lowerBound *= 100
                upperBound *= 100
            self.selCities = {c: d for (c, d) in self.selCities.items() if
                              lowerBound <= self.selCities[c][attribute] <=
                              upperBound}
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

        self.selCities.update(self.allCities)

    def unselectAllCities(self):
        # Un-select all cities.
        # TODO: clean up this documentation
        # Create a list of all cities in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # cities are iterated through, not all cities (a trade off of
        # computational efficiency for spatial efficiency).

        self.selCities.clear()

    def selectEdges(self, lowerBound, upperBound):
        # Here lowerBound and upperBound specify a "distance range."
        # For example, if lowerBound is set to 0 and upperBound is set to
        # 500, this method will select all edges between pairs of cities
        # whose distance (as specified in gis.dat) is at most 500 miles.
        # Assume that initially no edges are selected.
        self.selEdges = [e for e in self.selEdges if lowerBound <= e[2] <=
                         upperBound]

    def selectAllEdges(self):
        # Select all edges.
        # TODO: clean up this documentation
        # The alledges list created during initialization is iterated
        # through rather than iterating through calls to G as a matter of
        # computational efficiency.

        self.selEdges.extend(self.allEdges)

    def unselectAllEdges(self):
        # Un-select all edges.
        # TODO: clean up this documentation
        # Create a list of all edges in the graph which is then iterated
        # through for removal. This ensures that only currently selected
        # edges are iterated through, not all edges (a trade off of
        # computational efficiency for spatial efficiency).

        self.selEdges.clear()

    def makeGraph(self):
        # This method makes and returns a graph whose vertex set is the set of
        # selected cities and whose edge set is all selected edges connecting
        # pairs of selected cities.
        # FIXME: Adds edges between all
        G = nx.Graph()
        G.add_weighted_edges_from(self.selEdges)
        G.remove_nodes_from([city for city in self.allCities if city not in
                             self.selCities])
        return G

    def printCities(self, attribute='name', choice='S'):
        # As before, attribute can be one of "name", "state", "latitude",
        # "longitude", and "population." This methods prints all selected
        # cities sorted in increasing order by the given attribute.
        # You should also implement printCities(), i.e., with no given
        # attribute, which should behave exactly like printCities("names").
        # The second parameter choice ('S' or 'F') determines whether the
        # requested output should be displayed in "short" form or "full" form.

        if choice is 'F':
            for data in sorted(self.selCities.values(), key=itemgetter(
                    attribute)):
                print("{} [{}, {}], {}".format(self.selCities[data['name']][
                                                   'name'], self.selCities[
                    data['name']]['latitude'], self.selCities[data['name']][
                    'longitude'], self.selCities[data['name']]['population']))
        else:
            for data in sorted(self.selCities.values(), key=itemgetter(
                    attribute)):
                    print("{}".format(self.selCities[data['name']]['name']))

    def printEdges(self):
        # This should print all selected edges, in no particular order.

        # TODO: is this the format it should be in? No formatting, etc?
        for edge in self.selEdges:
            print("{:>22} < -- {:<4} mi -- > {:<22}".format(edge[0], edge[2],
                                                            edge[1]))

    def printPopulationDistr(self, value=20000):
        if not self.selCities:
            print('No cities found\n')
        else:
            lowerBound = 0
            upperBound = value
            distrCities = [c['population'] for c in self.selCities.values()]
            while distrCities:
                thisDistr = [c for c in distrCities if c < upperBound]
                if thisDistr:
                    print("[{}, {}]  :  {}".format(lowerBound, upperBound,
                                                   len(thisDistr)))
                distrCities[0:len(thisDistr)] = []
                lowerBound += value
                upperBound += value

    def printPopulatedStates(self, num):
        print("{} most populated states.\n{}".format(num, '-' * 43))
        for data in (sorted(self.selCities.values(), key=itemgetter(
                'population'), reverse=True))[0:num]:
            print("{} {}".format(self.selCities[data['name']]['state'],
                                 self.selCities[data['name']]['population']))

    def testMinMaxConsDistance(self):
        print("Goal:  minimize the maximum distance between any pair of\n "
              "consecutive cities on path from source to destination.\n")
        G = nx.minimum_spanning_tree(self.makeGraph())
        while True:
            source = input("Source (City, State):  ")
            target = input("Target (City, State):  ")
            print()
            if not source or not target:
                break
            elif nx.has_path(G, source, target):
                path = nx.shortest_path(G, source, target)
                H = G.copy()
                H.remove_nodes_from([city for city in H if city not in path])
                cost = max(H.edges(data=True), key=lambda t: t[2].get('weight'))
                print("Cost of optimal solution: {}".format(cost[2]['weight']))
                print("\nPath from {} to {}:".format(source, target))
                for city in path:
                    print(city)
            else:
                print("No path found")
            print('\n{}\n'.format('*' * 36))

    def tour(self, start):
        # This method outputs a traveling salesman tour on the selected
        # cities (and using the selected edges) starting from start.
        G = self.makeGraph()
        print("Traveling Salesman Tour starting from {} is ".format(start),
              end='')
        if (start in G) and (min(list(nx.degree(G).values())) >= 2):
            # The tour is computed using the nearest neighbor heuristic, i.e.,
            # at any point in the tour, the next city chosen is the closest to
            # current city among all the unvisited cities.
            unvisited = G.nodes()
            current = start
            total = 0
            tsp = [current]
            while unvisited:
                options = [city for city in list(G[current].keys()) if city in
                        unvisited]
                minn = ['', float('inf')]
                for city in options:
                    if G[current][city]['weight'] < minn[1]:
                        minn = [city, G[current][city]['weight']]
                #if minn[0] == start:
                #    print("not possible.")
                #    break
                total += minn[1]
                tsp.append(minn[0])
                current = minn[0]
                unvisited.remove(current)
                # max(G[current] in unvisited, key=lambda t: t[1].get('weight'))
            # In the output, exactly four cities are printed on each line except
            # possibly the last line of the output which may have fewer than
            # four cities.
            print("as follows.\n")
            while len(tsp) > 3:
                print("{} -- > {} -- > {} -- > {}".format(tsp[0], tsp[1],
                                                          tsp[2], tsp[3]))
                del tsp[0:4]
            if tsp:
                while len(tsp) > 1:
                    print("{} -- > ".format(tsp.pop(0)))
                print("{}".format(tsp.pop(0)))
            print("\nTour length:  {}".format(total))
        else:
            print("not possible.")