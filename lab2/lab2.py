# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from graphs import *
import time

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):

	agenda = [[start]]

	while True:
		new_agenda = []
		for possible_path in agenda:
			for node in graph.get_connected_nodes(possible_path[-1]):
				if node is goal: return possible_path + [node]

				if node not in possible_path: new_agenda.append(possible_path + [node])

		agenda = new_agenda

		if len(agenda) is 0: return [start]	


    #raise NotImplementedError

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):

	agenda = [[start]]

	while True:
		new_agenda = []

		choosen_path = agenda[0]
		agenda.pop(0)

		for node in graph.get_connected_nodes(choosen_path[-1]):
			if node is goal: return choosen_path + [node]

			if node not in choosen_path: new_agenda.append(choosen_path + [node])

		agenda = new_agenda + agenda

		if len(agenda) is 0: return [start]

    #raise NotImplementedError


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.

#Extra implementation

def order_by_heuristic(agenda, graph, goal):

	agenda = sorted(agenda, key=lambda x: graph.get_heuristic(x[-1][-1], goal))

	return agenda

def order_by_pathlength(agenda, graph):

	agenda = sorted(agenda, key=lambda x: path_length(graph, x))

	return agenda

def order_by_heuristic_and_pathlength(agenda, graph, goal):

	agenda = sorted(agenda, key=lambda x: (graph.get_heuristic(x[-1][-1], goal)+path_length(graph, x)) )

	return agenda


def hill_climbing(graph, start, goal):

	agenda = [[start]]

	while True:
		new_agenda = []

		choosen_path = agenda[0]
		agenda.pop(0)

		for node in graph.get_connected_nodes(choosen_path[-1]):
			
			if node is goal: 
				return choosen_path + [node]

			if node not in choosen_path: new_agenda.append(choosen_path + [node])

		agenda = order_by_heuristic(new_agenda, graph, goal) + agenda

		if len(agenda) is 0: return [start]

    #raise NotImplementedError


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.

def beam_search(graph, start, goal, beam_width):
    agenda = [[start]]

    while True:
		new_agenda = []
		for possible_path in agenda:
			for node in graph.get_connected_nodes(possible_path[-1]):
				if node is goal: return possible_path + [node]

				if node not in possible_path: new_agenda.append(possible_path + [node])

		agenda = order_by_heuristic(new_agenda, graph, goal)[:beam_width]

		if len(agenda) is 0: return []	

    #raise NotImplementedError

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):

	result = 0

	for i in range(len(node_names)):
		if i < len(node_names) - 1:
			result += graph.get_edge(node_names[i], node_names[i+1]).length

	return result
    #raise NotImplementedError


def branch_and_bound(graph, start, goal):

	agenda = [[start]]
	path = [start]

	while True:
		new_agenda = []

		choosen_path = agenda[0]
		agenda.pop(0)

		for node in graph.get_connected_nodes(choosen_path[-1]):
			possible_path = choosen_path + [node]

			if node is goal and (len(path) is 1 or path_length(graph, path) > path_length(graph, possible_path)): 
				path = possible_path

			elif node not in choosen_path: 
				new_agenda.append(choosen_path + [node])

		agenda = order_by_pathlength(new_agenda + agenda, graph)

		if len(agenda) is 0 or (len(path) is not 1 and path_length(graph, path) < path_length(graph, agenda[0])):
			return path


    #raise NotImplementedError

def a_star(graph, start, goal):

	agenda = [[start]]
	path = [start]
	extended_nodes = []

	while True:

		new_agenda = []

		choosen_path = agenda[0]
		agenda.pop(0)

		if choosen_path[-1] not in extended_nodes:
			
			extended_nodes.append(choosen_path[-1])

			for node in graph.get_connected_nodes(choosen_path[-1]):
				possible_path = choosen_path + [node]

				if node is goal and (len(path) is 1 or path_length(graph, path) > path_length(graph, possible_path)): 
					path = possible_path

				elif node not in choosen_path:
					new_agenda.append(choosen_path + [node])

		agenda = order_by_heuristic_and_pathlength(new_agenda + agenda, graph, goal)

		if len(agenda) is 0 or (len(path) is not 1 and 
			(path_length(graph, path) + graph.get_heuristic(path[-1], goal)) < (path_length(graph, agenda[0]) + graph.get_heuristic(agenda[0][-1], goal))):
			return path


    #raise NotImplementedError


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):

	for node in graph.nodes:
		if graph.get_heuristic(node, goal) > path_length(graph, branch_and_bound(graph, node, goal)): return False

	return True
    #raise NotImplementedError

def is_consistent(graph, goal):

	for edge in graph.edges:
		if edge.length < abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)): return False

	return True
    #raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = '3'
WHAT_I_FOUND_INTERESTING = 'Everything'
WHAT_I_FOUND_BORING = 'Nothing'
