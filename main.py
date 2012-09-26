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

number_of_vertices = 10

g = Graph.GRG(number_of_vertices, 0.5)
while (g.cohesion() == 0):
	g = Graph.GRG(number_of_vertices,0.5)

proposed_mincut_value = 9999
nbr_iter = number_of_vertices*(number_of_vertices-1)*math.log(number_of_vertices)
print "number of iterations : ", int(nbr_iter)
for i in range(int(nbr_iter)):
	g_temp = g.copy()
	temp_proposed_mincut_value = random_mincut(g_temp)
	if (temp_proposed_mincut_value < proposed_mincut_value):
		proposed_mincut_value = temp_proposed_mincut_value
		print "iter : ", i, "improved to : ", proposed_mincut_value

print "random_mincut found : ", proposed_mincut_value

print "true value : ", g.mincut()