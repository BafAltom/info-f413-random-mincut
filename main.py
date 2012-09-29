from igraph import *
# igraph: http://igraph.sourceforge.net/
import random
import math

random.seed()

NUMBER_OF_TESTS = 1000
CONFIDENCE_FACTOR = 5 # nice value : 5
REMOVE_FAILED_TESTS_IN_STATS = False
DISPLAY_FAILURES = False

class TestResult:
	def __init__(self, graph):
		#self.graph = graph
		self.number_of_vertices = graph.vcount()
		self.number_of_edges = graph.ecount()
		self.number_of_iterations = None
		self.improving_iterations = []
		self.improved_value = []
		self.found_value = None
		self.correct_value = None

	def __str__(self):
		assert(len(self.improving_iterations) == len(self.improved_value))
		assert(self.found_value != None)
		assert(self.correct_value != None)
		s = "Test with a graph of " + str(self.number_of_vertices) + " verticles and " + str(self.number_of_edges) + " edges.\n"
		s += "Used " + str(self.number_of_iterations) + " iterations.\n"
		for i in range(len(self.improving_iterations)):
			s += "- Found value : " + str(self.improved_value[i]) + " at iteration " + str(self.improving_iterations[i]) + "\n"
		s += "Final value : " + str(self.found_value) + "\n"
		s += "Correct value : " + str(self.correct_value) + "\n"
		return s

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

def find_mincut(graph, myTestResult):
	number_of_vertices = graph.vcount()
	best_mincut_value = graph.ecount() + 1 # borne superieure
	required_nbr_iter = int(number_of_vertices*(number_of_vertices-1)*math.log(number_of_vertices))
	nbr_iter = required_nbr_iter/CONFIDENCE_FACTOR
	myTestResult.number_of_iterations = nbr_iter
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
	while (g.cohesion() == 0):
		g = Graph.GRG(number_of_vertices,GRG_radius)
	return g

testResults = []
for i in range(NUMBER_OF_TESTS):
	number_of_vertices = random.randint(5,10)
	GRG_radius = random.randint(40,90)/float(100)
	if (NUMBER_OF_TESTS < 1000): print "test " + str(i+1) + " of " + str(NUMBER_OF_TESTS) + "..."
	elif(((i+1)%(NUMBER_OF_TESTS/10)) == 0): print "test " + str(i+1) + " of " + str(NUMBER_OF_TESTS) + "..."
	g = generate_random_connex_graph(number_of_vertices, GRG_radius)
	result = TestResult(g)
	find_mincut(g, result)
	testResults.append(result)

def strRound2(aFloat):
	return str(round(aFloat,2))

# compute some statistics on testResults
current_prop_sum = 0
current_failure_sum = 0
current_failure_value = 0
current_max_useful = 0
current_max_useful_2 = 0
current_max_useful_3 = 0
for tr in testResults:
	#failure count and value
	if(tr.found_value != tr.correct_value):
		if (DISPLAY_FAILURES):
			print "-----------------------------------------------------------"
			print "Failure :"
			print tr
		current_failure_sum += 1
		current_failure_value += tr.found_value - tr.correct_value
		if (REMOVE_FAILED_TESTS_IN_STATS):
			continue
	# max useful
	number_of_correction = len(tr.improving_iterations)
	last_useful_iteration_abs = tr.improving_iterations[number_of_correction-1]
	last_useful_iteration_rel = last_useful_iteration_abs / float(tr.number_of_iterations)
	if (last_useful_iteration_rel > current_max_useful):
		current_max_useful_3 = current_max_useful_2
		current_max_useful_2 = current_max_useful
		current_max_useful = last_useful_iteration_rel
	# proportion of useful work
	proportion_of_useful_work = last_useful_iteration_abs/float(tr.number_of_iterations)
	current_prop_sum += proportion_of_useful_work
prop_average = current_prop_sum/len(testResults)
print "-----------------------------------------------------------"
print "confidence factor: " + str(CONFIDENCE_FACTOR)
print "failures : " + str(current_failure_sum) + " = " + strRound2(current_failure_sum/float(NUMBER_OF_TESTS)) + "% of tests with an average of " + strRound2(current_failure_value/float(current_failure_sum)) + " absolute error (failures were removed from following stats)"
print "Three latest useful iteration (relative to total #iter) : " + strRound2(current_max_useful) + ", " + strRound2(current_max_useful_2) + ", " + strRound2(current_max_useful_3)
print "Proportion of useful work : " + strRound2(prop_average) + " (" + strRound2(prop_average/CONFIDENCE_FACTOR) + " without confidence factor)"
