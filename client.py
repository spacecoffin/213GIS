from gis import Gis

def main():
    gsystem = Gis()
    
    gsystem.selectAllCities()
    gsystem.selectAllEdges()
    
    delimiter = '\n*************************************\n'
    
    #### EXPERIMENT 1 ####
    gsystem.printCities()
    print(delimiter)
    
    # print full display
    gsystem.printCities('population', 'F')
    print(delimiter)
    
    #### EXPERIMENT 2 ####
    # select all cities with latitudes between 40N and 50N
    # and longitudes between 85W and 130W.
    gsystem.selectCities('latitude',40,50)
    gsystem.selectCities('longitude',85,130)
    
    print('Population distribution of cities with latitudes between\n 40N and 50N and longitudes between 85W and 130W.\n')
    
    gsystem.printPopulationDistr()
    
    print(delimiter)
    
    # print population distribution of cities in CA
    gsystem.selectAllCities()
    gsystem.selectCities('state','CA')
    
    print('Population distribution of cities in California.\n')
    gsystem.printPopulationDistr(30000)
    
    print(delimiter)
    
    #### EXPERIMENT 3 ####
    
    # print 'num' most populated states in non-increasing
    # order of their population.
    
    gsystem.selectAllCities()
    
    num = 3
    gsystem.printPopulatedStates(num)
    print(delimiter)
    
    #### EXPERIMENT 4 ####
    gsystem.testMinMaxConsDistance()
    print(delimiter)
    
    #### EXPERIMENT 5 ####
    gsystem.selectAllCities()
    gsystem.selectAllEdges()
    
    # print TSP tour starting from Yakima, WA, with
    # exactly 4 cities on each line except possibly the
    # last line.
    gsystem.tour('Yakima, WA')
    
    print(delimiter)
    
    gsystem.unselectAllEdges()
    gsystem.tour('Yakima, WA')
    print(delimiter)
    
    #### EXPERIMENT 6 ####
    gsystem.selectAllCities()
    gsystem.selectAllEdges()
    gsystem.selectEdges(1500,3000)
    
    gsystem.minCut()
    print(delimiter)
    
main()