#!/usr/bin/python3

# Sophie Lama           18 October 2024
# Theory of Computing   Project 01

import itertools
import time
from ast            import literal_eval
from collections    import defaultdict

# Types
Graph = dict[int, list]

# Functions
def read_graph(file):
    try:
        nodes_arr = file.readline().split(':')
        try: edges = literal_eval(file.readline().split(':').pop(2)[1:])
        except ValueError: return None
    except IndexError: # once the end of the file has been reached
        return None
    
    nodes = literal_eval(nodes_arr.pop(2)[1:-1]) # create list of nodes
    graph_status = nodes_arr.pop(1)[1:] # either 'Non-Hamiltonian graph' or 'Hamiltonian graph'
    edgeCount = len(edges)

    edge_graph: Graph = defaultdict(dict)
    for n in nodes:
        edge_graph[n] = []
    
    currentEdge = 0
    for edge_relationship in edges:
        source, target = edge_relationship
        edge_graph[source].append(target) # add connection between nodes to their lists of connections
        edge_graph[target].append(source) # not directed graph, connections go both ways

        currentEdge += 1
        if (currentEdge >= edgeCount): break # break once we've established every connection/edge

    return graph_status, nodes, edge_graph


def build_path(nodes, edges_dict): # Brute Force building a Hamiltonian path
    check_start_time = time.time()
    for perm in itertools.permutations(nodes): # for each permutation, attempt to build path
        no_connect_flag = 0
        i = 0
        while i < len(nodes)-1:
            source, destination = perm[i:i+2]
            if destination not in edges_dict[source]: # try to see if there's an edge btwn source, destination
                no_connect_flag = 1 # if not, give up on this permutation and move onto the next
                break
            i += 1
            
        if no_connect_flag == 0: # if no flags raised, then we found a Hamiltonian path passing through each vertex once
            return True
        
        check_end_time = time.time() # timeout after 5 minutes, move on to next graph
        if check_end_time - check_start_time > 5*60: return False

    return False # if we never found a Hamiltonian graph, return False


# Main Execution
def main():
    my_file = open("check_hamiltonian_path_test_cases_slama.txt") # file we're reading graphs from
    count = 0
    
    while data := read_graph(my_file):
        graph_identity, nodes, edge_graph = data
        count += 1

        start_time = time.time()
        stat = build_path(nodes, edge_graph) # go Brute Force mode
        end_time = time.time()

        if stat == True and graph_identity != "Hamiltonian graph":
            print(f'ERROR! {stat} and {graph_identity}')
        if stat == False and graph_identity != "Non-Hamiltonian graph":
            print(f'ERROR! {stat} and {graph_identity}')

        total_time = (end_time - start_time)*1000
        if count == 1: mode = "w"      
        else: mode = "a"
        f = open("output_slama.csv", mode)
        f.write(f'{stat},{len(nodes)},{total_time}\n')
        f.close()

    return

if __name__ == '__main__':
    main()