#!/usr/bin/python
# -*- coding: utf-8 -*-

from igraph import *
# igraph: http://igraph.sourceforge.net/
import random
import math

random.seed()

# Nombre de graphes qui vont être testés
NUMBER_OF_TESTS = 10000
# Proportion d'itérations qui ne vont pas être effectuées (par rapport à la borne minimale vue au cours)
CONFIDENCE_FACTOR = 100 # def: 5 
# Bornes min/max du nombre de sommets de chaque graphe
VERTICES_NB_MIN = 5 # def: 5 
VERTICES_NB_MAX = 10 # def: 10
# Borne min/max du radius GRG de chaque graphe (une plus grande valeur signifie plus d'arêtes)
GRG_RADIUS_MIN = 0.4 # def: 0.4
GRG_RADIUS_MAX = 1.0 # def: 0.9
# Utilise (True) ou non (False) les graphes pour lesquels la coupe minimale n'a pas été trouvée dans les statistiques
REMOVE_FAILED_TESTS_IN_STATS = True
# Affiche (True) ou non (False) un résumé des tests pour lesquels la coupe minimale n'a pas été trouvée
DISPLAY_FAILURES = False
# Recommence l'exécution si aucune faute n'a été trouvée (peut prendre beaucoup de temps...)
CONTINUE_ON_PERFECT_TEST = False

class TestResult: # Classe stockant un résumé de l'exécution d'un test
	def __init__(self, graph):
		#self.graph = graph
		self.number_of_vertices = graph.vcount()
		self.number_of_edges = graph.ecount()
		self.number_of_iterations = None
		self.improving_iterations = []
		self.improved_values = []
		self.found_value = None
		self.correct_value = None

	def consistencyCheck(self):
		assert(len(self.improving_iterations) == len(self.improved_values))
		assert(self.found_value != None)
		assert(self.correct_value != None)

	def __str__(self):
		self.consistencyCheck()
		s = "Test with a graph of " + str(self.number_of_vertices) + " verticles and " + str(self.number_of_edges) + " edges.\n"
		s += "Used " + str(self.number_of_iterations) + " iterations.\n"
		for i in range(len(self.improving_iterations)):
			s += "- Found value : " + str(self.improved_values[i]) + " at iteration " + str(self.improving_iterations[i]) + "\n"
		s += "Final value : " + str(self.found_value) + "\n"
		s += "Correct value : " + str(self.correct_value) + "\n"
		return s

def random_mincut_one_instance(g):
	while (g.vcount() > 2 and g.ecount() > 0):
		edge_list = g.get_edgelist()
		if (g.ecount() == 1): rand_edge_id = 0 # hotfix pour des graphes non connexes
		else: rand_edge_id = random.randint(0,g.ecount()-1)
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

def random_mincut_all(graph, myTestResult):
	number_of_vertices = graph.vcount()
	best_mincut_value = 999999
	required_nbr_iter = int(number_of_vertices*(number_of_vertices-1)*math.log(number_of_vertices))
	nbr_iter = max(1,required_nbr_iter/CONFIDENCE_FACTOR)
	myTestResult.number_of_iterations = nbr_iter
	for i in range(nbr_iter):
		g_temp = graph.copy()
		result = random_mincut_one_instance(g_temp)
		if (result < best_mincut_value):
			best_mincut_value = result
			myTestResult.improving_iterations.append(i)
			myTestResult.improved_values.append(best_mincut_value)

	myTestResult.found_value = best_mincut_value
	myTestResult.correct_value = int(graph.mincut().value)
	return myTestResult

def generate_random_connex_graph(number_of_vertices, GRG_radius):
	g = Graph.GRG(number_of_vertices, GRG_radius)
	while (g.cohesion() == 0):
		g = Graph.GRG(number_of_vertices,GRG_radius)
	return g

def strRound2(aFloat):
	return str(round(aFloat,2))

if __name__ == "__main__":
	anotherRound = True
	while (anotherRound):
		tests_results = []
		for i in range(NUMBER_OF_TESTS):
			if (NUMBER_OF_TESTS < 1000): print "test " + str(i+1) + " of " + str(NUMBER_OF_TESTS) + "..."
			elif(((i+1)%(NUMBER_OF_TESTS/100)) == 0): print "test " + str(i+1) + " of " + str(NUMBER_OF_TESTS) + "..."
			
			number_of_vertices = random.randint(VERTICES_NB_MIN,VERTICES_NB_MAX)
			GRG_radius = random.randint(GRG_RADIUS_MIN*100,GRG_RADIUS_MAX*100)/float(100)
			g = generate_random_connex_graph(number_of_vertices, GRG_radius)
			result = TestResult(g)
			random_mincut_all(g, result)
			tests_results.append(result)

		# compute some statistics on tests_results
		current_prop_sum = 0
		current_failure_sum = 0
		current_failure_value = 0
		current_max_useful = 0
		current_max_useful_2 = 0
		current_max_useful_3 = 0
		for tr in tests_results:
			tr.consistencyCheck()
			#failure count and value
			if(tr.found_value != tr.correct_value):
				if (DISPLAY_FAILURES):
					print "-----------------------"
					print "Failure :"
					print tr
				current_failure_sum += 1
				current_failure_value += tr.found_value - tr.correct_value
				if (REMOVE_FAILED_TESTS_IN_STATS):
					continue
			# max useful
			number_of_correction = len(tr.improving_iterations)
			if (number_of_correction == 0):
				print tr
			last_useful_iteration_abs = tr.improving_iterations[number_of_correction-1]
			last_useful_iteration_rel = last_useful_iteration_abs / float(tr.number_of_iterations)
			if (last_useful_iteration_rel > current_max_useful):
				current_max_useful_3 = current_max_useful_2
				current_max_useful_2 = current_max_useful
				current_max_useful = last_useful_iteration_rel
			# proportion of useful work
			current_prop_sum += last_useful_iteration_rel

		prop_average = None
		if(REMOVE_FAILED_TESTS_IN_STATS):
			prop_average = current_prop_sum/(len(tests_results) - current_failure_sum)
		else:
			prop_average = current_prop_sum/len(tests_results)

		if (CONTINUE_ON_PERFECT_TEST and current_failure_sum == 0): anotherRound = True
		else: anotherRound = False

	print "------------------------"
	print "confidence factor: " + str(CONFIDENCE_FACTOR)
	print "failures : " + str(current_failure_sum) + " = " + strRound2(100*current_failure_sum/float(NUMBER_OF_TESTS)) + "% of tests"
	if (current_failure_sum > 0): print "...with an average of " + strRound2(current_failure_value/float(current_failure_sum)) + " absolute error"
	if (REMOVE_FAILED_TESTS_IN_STATS): print "(Failed tests were removed from the following stats)"
	print "Three latest useful iterations (relative to total #iter) : " + strRound2(current_max_useful) + ", " + strRound2(current_max_useful_2) + ", " + strRound2(current_max_useful_3)
	print "Proportion of useful work : " + strRound2(prop_average) + " (" + strRound2(prop_average/CONFIDENCE_FACTOR) + " without confidence factor)"