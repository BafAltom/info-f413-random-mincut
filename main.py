from igraph import *
import random

#nb_verticles = 5
#g = Graph(nb_verticles)
#g.mincut()

# Generation : http://igraph.sourceforge.net/doc/python/igraph.GraphBase-class.html

g = Graph.GRG(10, 0.5)
assert(g.cohesion() > 0)
#print(g.get_edgelist())

while (g.vcount() > 2):
	print ""
	print g
	edge_list = g.get_edgelist()
	rand_edge_id = random.randint(0,g.ecount()-1)
	chosen_edge = edge_list[rand_edge_id]
	print "chosen edge: ", chosen_edge
	chosen_edge_source = chosen_edge[0] # source vertices
	chosen_edge_target = chosen_edge[1] # target vertices
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

print g

print g.mincut()