from igraph import *
# igraph: http://igraph.sourceforge.net/
import random
import math

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
	print "number of iterations : ", int(nbr_iter)
	for i in range(nbr_iter):
		g_temp = g.copy()
		result = random_mincut(g_temp)
		if (result < best_mincut_value):
			best_mincut_value = result
			print "iter : ", i, "improved to : ", best_mincut_value

	print "best mincut found : ", best_mincut_value

	print "mincut was : ", g.mincut()	

def generate_random_graph(number_of_vertices, GRG_radius):
	g = Graph.GRG(number_of_vertices, GRG_radius)
	graph_build_counter = 0
	while (g.cohesion() == 0):
		graph_build_counter += 1
		g = Graph.GRG(number_of_vertices,GRG_radius)
	print "found connex graph after ", graph_build_counter, " tries."
	return g

g = generate_random_graph(15,0.8)
find_mincut(g)