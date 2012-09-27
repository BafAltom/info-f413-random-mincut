from igraph import *
# igraph: http://igraph.sourceforge.net/
import random
import math

class TestResult:
	def __init__(self, graph, number_of_iterations):
		self.number_of_vertices = graph.vcount()
		self.number_of_edges = graph.ecount()
		self.number_of_iterations = number_of_iterations
		self.improving_iterations = []
		self.improved_value = []
		self.found_value = None
		self.correct_value = None

	def __str__(self):
		assert(len(self.improving_iterations) == len(self.improved_value))
		assert(self.found_value != None)
		assert(self.correct_value != None)
		reprString = "Test with a graph of " + str(self.number_of_vertices) + " verticles and " + str(self.number_of_edges) + " edges.\n"
		reprString += "Used " + str(self.number_of_iterations) + " iterations.\n"
		for i in range(len(self.improving_iterations)):
			reprString += "Found value :\t" + str(self.improved_value[i]) + "\tat iteration\t" + str(self.improving_iterations[i]) + "\n" 
		reprString += "Final value :\t" + str(self.found_value) + "\n"
		reprString += "Correct value :\t" + str(self.correct_value) + "\n"
		return reprString

def random_mincut(g):
	while (g.vcount() > 2):
		edge_list = g.get_edgelist()
		rand_edge_id = random.randint(0,g.ecount()-1)
		chosen_edge = edge_list[rand_edge_id]
		chosen_edge_source = chosen_edge[0]
		chosen_edge_target = chosen_edge[1]
		for e in edge_list:
			if (e[0] == chosen_edge_target or e[1] == chosen_edge_target):
				if (e[0] == chosen_edge_target and e[1] != chosen_edge_source):
					g.add_edge(chosen_edge_source, e[1])
				elif (e[1] == chosen_edge_target and e[0] != chosen_edge_source):
					g.add_edge(e[0], chosen_edge_source)
				edge_id = g.get_eid(e[0], e[1])
				g.delete_edges(edge_id)

		assert(g.degree(chosen_edge_target) == 0)
		g.delete_vertices(chosen_edge_target)
	return g.ecount()

def find_mincut(graph):
	number_of_vertices = graph.vcount()
	best_mincut_value = graph.ecount() + 1 # borne superieure
	nbr_iter = int(number_of_vertices*(number_of_vertices-1)*math.log(number_of_vertices))
	myTestResult = TestResult(graph, nbr_iter)
	for i in range(nbr_iter):
		g_temp = g.copy()
		result = random_mincut(g_temp)
		if (result < best_mincut_value):
			best_mincut_value = result
			myTestResult.improving_iterations.append(i)
			myTestResult.improved_value.append(best_mincut_value)

	myTestResult.found_value = best_mincut_value
	myTestResult.correct_value = int(g.mincut().value)
	return myTestResult

def generate_random_connex_graph(number_of_vertices, GRG_radius):
	g = Graph.GRG(number_of_vertices, GRG_radius)
	graph_build_counter = 0
	while (g.cohesion() == 0):
		graph_build_counter += 1
		g = Graph.GRG(number_of_vertices,GRG_radius)
	print "found connex graph after ", graph_build_counter, " tries."
	return g

testResults = []
for i in range(10):
	g = generate_random_connex_graph(15,0.8)
	result = find_mincut(g)
	testResults.append(result)
	#print(result)

# compute some statistics on testResults
currentSum = 0
for tr in testResults:
	number_of_correction = len(tr.improving_iterations)
	last_useful_iteration = tr.improving_iterations[number_of_correction-1]
	proportion_of_useful_work = last_useful_iteration/float(tr.number_of_iterations)
	currentSum += proportion_of_useful_work
average = currentSum/len(testResults)
print "prop of useful work :\t" + str(average)