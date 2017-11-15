import networkx as nx
import numpy as np
import copy as cp
from requests import Requests
from wavelength import Wavelength

number_of_requests = 2
a = 50
muy = 1
lam = a * muy

# Generate network

G = nx.Graph()
for index in range(1, 18):
    G.add_node(index)
for index in range(1, 17):
    G.add_edge(index, index + 1, weight=0)
G.add_edge(17, 1, weight=0)
G.add_edge(17, 2, weight=0)
G.add_edge(17, 3, weight=0)
G.add_edge(17, 10, weight=0)
G.add_edge(17, 14, weight=0)
G.add_edge(17, 16, weight=0)
G.add_edge(16, 1, weight=0)
G.add_edge(14, 11, weight=0)
G.add_edge(10, 3, weight=0)
G.add_edge(10, 4, weight=0)
G.add_edge(7, 4, weight=0)

edges = list(G.edges())
com_edges = {}

for index in range(0, G.number_of_edges()):
    com_edges[edges[index]] = Wavelength()

# Generate source and destination
while True:
    check = False
    source = np.random.randint(1, 18, number_of_requests)
    destination = np.random.randint(1, 18, number_of_requests)
    for index in range(0, number_of_requests):
        if source[index] == destination[index]:
            check = True
    if not check:
        break


# Generate exponential interval time and holding time of requests
def generate_time(mean, number_requests):
    while True:
        condition = False
        time = np.random.exponential(mean, number_requests)
        for t in time:
            if t == 0:
                condition = True
        if not condition:
            break
    return time


events_time = generate_time(1/lam, number_of_requests)
holding_time = generate_time(1/muy, number_of_requests)

s = 0
time = []
for e in events_time:
    s += e
    time.append(s)

time_line = []
for index in range(0, number_of_requests):
    time_line.append(time[index] + holding_time[index])

time_new = time + time_line

# sort the whole time line
for index in range(len(time_new)):
    for j in range(len(time_new) - 1 - index):
        if time_new[j] > time_new[j + 1]:
            time_new[j], time_new[j + 1] = time_new[j + 1], time_new[j]

# put each request into a list
Req = []
for index in range(0, number_of_requests):
    req = Requests(time[index], time_line[index], source[index], destination[index], index)
    Req.append(req)

# put each request into a list following time_new
Events = []
for index in range(len(time_new)):
    for req in Req:
        if req.inTime == time_new[index]:
            Events.append(req)
        elif req.outTime == time_new[index]:
            temp = cp.copy(req)
            temp.isCall = 1
            Events.append(temp)

print(len(Events))

# algorithm


def binding_edges(request):
    print("BINDING")
    print("src:", request.source)
    print("des:", request.des)

    while True:
        check = False
        all_paths = list(nx.all_simple_paths(G, request.source, request.des))
        # sort all_paths in ascesding order
        sorted_paths = []
        len_paths = []
        for path in all_paths:
            len_paths.append(len(path))
        len_paths.sort()
        for l in len_paths:
            for path in all_paths:
                if len(path) == l:
                    sorted_paths.append(path)
                    break
                all_paths.remove(path)
        for path in sorted_paths:
            print(path)
            # chosen_path = nx.shortest_path(G, request.source, request.des, weight='weight')
            chosen_path = path
            list_of_wl = list(range(0, 8))
            path_is_set = False
            while list_of_wl != [] and not path_is_set:
                # choose random wavelength
                chosen_wl = np.random.choice(list_of_wl)
                print("chosen wavelength: ", chosen_wl)
                condition_loop = True
                # loop through the wavelength list of each edge
                for i in range(0, len(chosen_path) - 1):
                    # pick out one edge
                    temp_edges1 = (chosen_path[i], chosen_path[i + 1])
                    temp_edges2 = (chosen_path[i + 1], chosen_path[i])
                    for edg in com_edges:
                        if edg == temp_edges1 or edg == temp_edges2:
                            weight = com_edges[edg].get_wavelength(chosen_wl)
                            # check whether the chosen wavelength is free
                            if weight == 0:
                                condition_loop = False
                            elif weight == 1:
                                condition_loop = True
                            elif weight == 2:
                                condition_loop = True
                            break
                # if the chosen wavelength is free then take it and set the path for the request
                if condition_loop:
                    request.set_wavelength(chosen_wl)
                    # loop through the path
                    for i in range(0, len(request.get_path()) - 1):
                        # pick one edge
                        temp_edges1 = (request.get_path()[i], request.get_path()[i + 1])
                        temp_edges2 = (request.get_path()[i + 1], request.get_path()[i])
                        for edg in com_edges:
                            if edg == temp_edges1 or edg == temp_edges2:
                                # assign the chosen wavelength for each edge
                                com_edges[edg].use_wavelength(chosen_wl)
                                print("wavelength ", chosen_wl, " on ", edg, ": ", com_edges[edg].get_wavelength(chosen_wl))

                                break
                        # ---add weight for the chosen path
                        # G[request.get_path()[i]][request.get_path()[i + 1]]['weight'] += 1
                    request.set_path(chosen_path)
                    path_is_set = True
                # if the chosen wavelength is not free then discard the wavelength
                # and choose the other wavelength randomly
                else:
                    list_of_wl.remove(chosen_wl)
            if path_is_set:
                check = True
                break
        if check:
            break

    request.print_details()
    for event in Events:
        if event != request and event.index == request.index:
            event.set_path(request.get_path())
            event.set_wavelength(request.get_wavelength())
            event.print_details()
            print()
            break
            # for i in range(0, len(req.path) - 1):
            #     for edges in comEdges:
            #         if edges == (req.path[i], req.path[i+1]) or edges == (req.path[i+1], req.path[i]):
            #             comEdges[edges].fiber1[1] += 1
            #             print(edges, comEdges[edges].fiber1)

            # if G[req.path[i]][req.path[i+1]]['weight'] < 1:
            #     G[req.path[i]][req.path[i + 1]]['weight'] += 1
            # elif


def release_edges(request):
    print("RELEASED")
    request.print_details()
    chosen_wl = request.get_wavelength()
    for i in range(0, len(request.get_path()) - 1):
        temp_edges1 = (request.get_path()[i], request.get_path()[i + 1])
        temp_edges2 = (request.get_path()[i + 1], request.get_path()[i])
        for edg in com_edges:
            if edg == temp_edges1 or edg == temp_edges2:
                com_edges[edg].release_wavelength(chosen_wl)
                print("wavelength ", chosen_wl, " on ", edg, ": ", com_edges[edg].get_wavelength(chosen_wl))
        G[request.get_path()[i]][request.get_path()[i + 1]]['weight'] -= 1
    print("path ", request.get_path(), " is clear, wavelength ", chosen_wl, " is released")
    # request.path = []


for e in Events:
    if e.isCall == 0:
        binding_edges(e)
    elif e.isCall == 1:
        release_edges(e)
for i in range(0, len(edges)):
    print(edges[i], "   ", com_edges[edges[i]].get_data())

"""all_paths = list(nx.all_simple_paths(G, 1, 16))
len_paths = []
sort_paths = []
for path in all_paths:
    len_paths.append(len(path))
    # print(path)
len_paths.sort()
print(len_paths)
for lens in len_paths:
    for path in all_paths:
        if len(path) == lens:
            sort_paths.append(path)
            break
    all_paths.remove(path)
for path in sort_paths:
    print(path)
print(len(all_paths)"""
        # for e in Events:
        #     if e != Events[0] and e.inTime == Events[0].inTime:
        #         e.path = Events[0].path
        #         e.print_details()

        # print(G.number_of_nodes())
        # print(events)
        # print(holding_time)
        # print(time)
        # print(time_line)
        # print("final source:     ", source)
        # print("final destination:", destination)
