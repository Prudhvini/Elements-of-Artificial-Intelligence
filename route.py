'''Documentation
We considered this problem as a graph search problem and created a graph with vertices as cities. 
We use two classes to maintain the information about the graph and vertices.
The state space contains cities and their paths

We are handling the mistakes in the files wherever possible by making the values 0 if they are numeric and '' in case of strings

For BFS and DFS we are not considering the costs associated with the edges between the cities, we are considering all edges to have the same cost.
The code to include the costs associated with the edge is also implemented but to be in consistent with the assignment we have commented the code.
The code for uniform cost search is commented.

For A* we consider the routing option and the heuristic for each option is as follows:
Distance:
In case of distance we read the latitude and longitude values from city-gps.txt and calculate the euclidean distance between current city and goal city.
The euclidean distance heuristic is admissible because the distance between two cities in terms of latitude and logitude will definitely be less 
than the actual distance between the cities. Therefore it cannot be an over estimate.
The distance between two cities is selected as g(n)

Time:
For any two cities under consideration we find the euclidean distance between the cities, we multiply it by the speed value to get heuristic time value. 
(By unary method and time = (distance / speed))
The heuristic is admissibe because the time taken will be the minimum amount of time(speed being the bottle neck) to travel between cities. 
The cost to travel between two cities is selected as g(n)

Segments:
Assumption made here is that on one highway there will be no turns. Therefore we consider heuristic to be 0.
The cost is assumed to be 1 for each segment.
f(n) = g(n)

The following code can be execute by using the following commands
python route.py <city name 1> <city name 2> <routing_option> <route_algorithm>

Routing algorithms are:
bfs
dfs
astar

Routing options are:
distance
time
segments

The output format is as follows

Distance Time_taken Path(including cities and highways) 

Analysis:
Time taken: 
For 100 runs of the algorithms following are the times:
DFS-0.06 seconds
BFS-0.04 seconds
ASTAR-1.5 seconds
For 1000 runs of the algorithms following are the same:
DFS-0.67 seconds
BFS-0.38 seconds
ASTAR-15.5 seconds

Astar took 20 times more time compared to DFS and BFS
With use of better data structures, the performance of the algorithms can be enhanced.
For distance, we got BFS as the best routing option
For time , we got best results from A* all the time and BFS some times
For segments, A* was the best algorithm

An example for route between Bloomington,_Indiana and Indianapolis,_Indiana gave the following results
DFS:
194 4.05264180264 ['Bloomington,_Indiana', 'IN_37', 'Bedford,_Indiana', 'US_50', 'Seymour,_Indiana', 'I-65', 'Columbus,_Indiana', 'IN_46', 'Greensburg,_Indiana', 'IN_3', 'Rushville,_Indiana', 'IN_44', 'Shelbyville,_Indiana', 'IN_44', 'Franklin,_Indiana', 'I-65', 'Jct_I-65_&_I-465_S,_Indiana', 'I-74/465', 'Jct_I-74_&_I-465_E,_Indiana', 'US_421', 'Indianapolis,_Indiana']

BFS:
 74 1.42905982906 ['Bloomington,_Indiana', 'IN_46', 'Columbus,_Indiana', 'I-65', 'Franklin,_Indiana', 'I-65', 'Jct_I-65_&_I-465_S,_Indiana', 'I-65', 'Indianapolis,_Indiana']

Astar with distance:
 65.0 1.31581196581 ['Bloomington,_Indiana', 'IN_37', 'Martinsville,_Indiana', 'IN_44', 'Franklin,_Indiana', 'I-65', 'Jct_I-65_&_I-465_S,_Indiana', 'I-65', 'Indianapolis,_Indiana']

Astar with time:
 52.0 1.05221445221 ['Bloomington,_Indiana', 'IN_37', 'Martinsville,_Indiana', 'IN_37', 'Jct_I-465_&_IN_37_S,_Indiana', 'I-74/465', 'Jct_I-65_&_I-465_S,_Indiana', 'I-65', 'Indianapolis,_Indiana']

Astar with segments:
 65.0 1.31581196581 ['Bloomington,_Indiana', 'IN_37', 'Martinsville,_Indiana', 'IN_44', 'Franklin,_Indiana', 'I-65', 'Jct_I-65_&_I-465_S,_Indiana', 'I-65', 'Indianapolis,_Indiana']
'''

import sys
import collections
import math
import itertools
import operator
import time
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight={}):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
		
class graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = {}):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

def get_heuristic(x1,x2,y1,y2):
	return math.sqrt(((float(x1)-float(y1))*(float(x1)-float(y1)))+((float(x2)-float(y2))*(float(x2)-float(y2))))
	
def bfs_search(start_city,end_city):
	nodes = []
	visited = []
	path = []
	
	if (g.get_vertex(start_city) == None):
		return None
		
	if (start_city == end_city):
		return [start_city]

	if (start_city not in nodes):
		nodes = nodes +[start_city]

	path = find_path_bfs(start_city, end_city, 0, 0.0, nodes, visited)
	if path != []:
		print path.pop(), path.pop(), path
	else:
		print "No path found between %s and %s"%(start_city, end_city)

def find_path_bfs(start_city, end_city, distance, time, nodes, visited):
	if(nodes == []):
		return []

	node_list=[]
	edge_dict={}
	path = []

	current = nodes.pop(0)
	visited = visited + [current]
	for node in g.get_vertex(current).get_connections():
		temp = g.get_vertex(current).get_weight(node)
		edge_dict.setdefault(node.get_id(),[])
		edge_dict[node.get_id()].append(int(temp[0]))
		edge_dict[node.get_id()].append(float(temp[0])/float(temp[1]))
		edge_dict[node.get_id()].append(temp[2].rstrip())
		node_list = node_list + [node.get_id()]
	
	#edge_dict = dict(itertools.izip(node_list,cost_list))
	#edge_dict = sorted(edge_dict.iteritems(), key=operator.itemgetter(1))

	for node in edge_dict:
		if node == end_city:
			return [current] + [edge_dict[node][2]] + [end_city] + [time + float(edge_dict[node][1])] + [distance + int(edge_dict[node][0])]
		elif node not in nodes and node not in visited:
			nodes = nodes + [node]

	if nodes == []:
		return path

	path = find_path_bfs(start_city, end_city, distance, time, nodes, visited)

	if path != []:
		for node in edge_dict:
			if(path[0] == node):
				cost1 = int(path.pop()) + int(edge_dict[node][0])
				cost2 = float(path.pop()) + float(edge_dict[node][1])
				path = [current] + [edge_dict[node][2]] + path + [cost2] + [cost1]
	return path

def dfs_search(start_city, end_city):
	path = find_path_dfs(start_city, end_city, 0, 0.0)
	if path != []:
		print path.pop(), path.pop(), path
	else:
		print "No path found between %s and %s"%(start_city, end_city)

def find_path_dfs(start_city, end_city, distance, time, path=[]):
	highway_list=[]
	node_list=[]
	edge_dict={}
	
	path = path + [start_city]
	if start_city == end_city:
		return path + [time] + [distance]

	if (g.get_vertex(start_city) == None):
		return []

	for node in g.get_vertex(start_city).get_connections():
		
		temp = g.get_vertex(start_city).get_weight(node)
		node_list = node_list + [node.get_id()]
		edge_dict.setdefault(node.get_id(),[])
		edge_dict[node.get_id()].append(int(temp[0]))
		if temp[1] == '0' or temp[0] == '0':
			edge_dict[node.get_id()].append(float(0))
		else:
			edge_dict[node.get_id()].append(float(temp[0])/float(temp[1]))
		if temp[2] == 'Unknown':
			edge_dict[node.get_id()].append(temp[2])
		else:
			edge_dict[node.get_id()].append(temp[2].rstrip())
		
	#implement for uniform cost search
	"""if route_option == 'distance':
		edge_dict = sorted(edge_dict.items(), key=lambda (k, v): v[0])
	elif route_option == 'time':
		edge_dict = sorted(edge_dict.items(), key=lambda (k, v): v[1])"""

	for node in edge_dict:
		if node not in path:
			cost1 = distance + int(edge_dict[node][0])
			cost2 = time + float(edge_dict[node][1])
			cost3 = path + [edge_dict[node][2]]
			newpath = find_path_dfs(node, end_city, cost1, cost2, cost3)
			if newpath:
				return newpath
	return []

def astar_search(start_city,end_city,route_option):
	print "astar"
	#nodes = []
	path = []
	openlist = {}
	closedlist = []
	
	if (g.get_vertex(start_city) == None):
		return None
		
	if (start_city == end_city):
		return [start_city]

	inputfile = open("city-gps.txt")
	lat = {}
	longt = {}
	inputfile = inputfile.readlines()
	for line in inputfile:
		latitude = line.split(" ")[1]
		longitude = line.split(" ")[2]
		if latitude == None:
			lat[line.split(" ")[0]] = 0
		else:
			lat[line.split(" ")[0]] = line.split(" ")[1]
		if longitude == None:
			longt[line.split(" ")[0]] = 0
		else:
			longt[line.split(" ")[0]] = line.split(" ")[2]

	g.get_vertex(start_city).parent = []
	openlist[g.get_vertex(start_city)] = get_heuristic(lat[start_city],longt[start_city],lat[end_city],longt[end_city])	
	path = find_path_astar(start_city, end_city, 0, lat, longt, openlist, closedlist, route_option)
	cost = 0
	path1 =[]
	length = len(path)
	if path != []:
		time = 0
		length = len(path)
		for i in range(0,length):
			path1 = path1 + [path[i].get_id()]
			if i < length-1:
				temp = g.get_vertex(path[i].get_id()).get_weight(path[i+1])
				cost += float(temp[0])
				time = time + (float(temp[0])/float(temp[1]))
				path1 = path1 + [temp[2].rstrip()]
		print cost,time,path1
	else:
		print "No path found between %s and %s"%(start_city,end_city)

def find_path_astar(start_city, end_city, weight, lat, longt, openlist, closedlist, route_option):
	if(openlist == []):
		return None
	path = []

	current = openlist.popitem()

	if str(current[0].get_id())==end_city:
		return [current[0]]

	closedlist.append(g.get_vertex(current[0].get_id()))
	for node in g.get_vertex(current[0].get_id()).get_connections():
		if node not in closedlist:
			temp = g.get_vertex(current[0].get_id()).get_weight(node)
			if route_option == 'distance':
				cost = float(temp[0])
			elif route_option == 'time':
				cost = float(temp[0])/float(temp[1])
			elif route_option == 'segments':
				cost = 1
			if node not in openlist:
				if route_option == 'distance':
					if node.get_id() not in lat:
						openlist[node] = 1000000 + cost
					else:	
						openlist[node] = get_heuristic(lat[node.get_id()],longt[node.get_id()],lat[end_city],longt[end_city]) + cost
					
					
				elif route_option == 'time':
					if node.get_id() not in lat:
						openlist[node] = cost
					else:
						h_time = float(temp[1])* get_heuristic(lat[node.get_id()],longt[node.get_id()],lat[end_city],longt[end_city])
						openlist[node] = h_time + cost
				else:
					openlist[node] = cost
					
				node.parent = g.get_vertex(current[0].get_id())
	if openlist=={}:
		return []
	openlist = collections.OrderedDict(sorted(openlist.items(), key=lambda t: t[1]))
	newlist = openlist.items()
	newlist.reverse()
	openlist = collections.OrderedDict(newlist)
	path = find_path_astar(start_city, end_city, weight, lat, longt,openlist,closedlist,route_option)
	
	if path == []:
		return []

	if path[0].parent != []:
		path = [path[0].parent] + path
	return path
		
	
def word_find(line,city):
	for part in line.split():
		if city in part:
			return 1

def create_graph(city_list,index,route_option,end_city):
	with open('road-segments.txt','r') as f2:
		for i,line in enumerate(f2):
			edge_weight = {}
			common = word_find(line,city_list[index])
			if common:			
				if(line.split(" ")[2] == None):
					edge_weight[0] = '0'
				else:
					edge_weight[0] = line.split(" ")[2]
				if(line.split(" ")[3] == None):
					edge_weight[1] = '0'
				else:
					edge_weight[1] = line.split(" ")[3]
				if(line.split(" ")[4] == ''):
					edge_weight[2] = "Unknown"
				else:
					edge_weight[2] = line.split(" ")[4]
				
				if(city_list[index] == line.split(" ")[0]):
					if(g.get_vertex(city_list[index]) == None):
						g.add_vertex(city_list[index])
						city_list.append(city_list[index])
					if(g.get_vertex(line.split(" ")[1]) == None):
						g.add_vertex(line.split(" ")[1])
						city_list.append(line.split(" ")[1])
					if(line.split(" ")[1] != city_list[index]):
						g.add_edge(city_list[index],line.split(" ")[1],edge_weight)
				elif(city_list[index] == line.split(" ")[1]):
					if(g.get_vertex(city_list[index]) == None):
						g.add_vertex(city_list[index])
						city_list.append(city_list[index])
					if(line.split(" ")[0] != city_list[index]):
						g.add_edge(city_list[index],line.split(" ")[0],edge_weight)
	
def main():
	start_city = sys.argv[1]
	end_city = sys.argv[2]
	route_option = sys.argv[3]
	route_algorithm = sys.argv[4]
	
	global g
	g = graph()
	global f1
	
	city_list = [start_city]
	index = len(city_list)
	
	while index <= len(city_list):
		create_graph(city_list,index-1,route_option,end_city)		
		index=index+1
		
	#start = time.clock()
	#for i in range(0,1000):
	if(route_algorithm == 'bfs'):
		bfs_search(start_city,end_city)
		#print "BFS time taken = "
	if(route_algorithm == 'dfs'):
		dfs_search(start_city,end_city)
		#print "DFS time taken = "
	if(route_algorithm == 'astar'):
		astar_search(start_city,end_city,route_option)
		#print "A* time taken = "
	#print time.clock() - start
if __name__ == "__main__":main()
