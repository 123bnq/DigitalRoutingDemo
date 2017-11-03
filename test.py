import networkx as nx
import numpy as np
import copy as cp
from requests import Requests
from wavelength import Wavelength

number_of_requests = 3
a = 5
muy = 1
lam = a*muy

# Generate network

G = nx.Graph()
for i in range(1, 18):
    G.add_node(i)
for i in range(1, 17):
    G.add_edge(i, i+1, weight = 0)
G.add_edge(17, 1, weight = 0)
G.add_edge(17, 2, weight = 0)
G.add_edge(17, 3, weight = 0)
G.add_edge(17, 10, weight = 0)
G.add_edge(17, 14, weight = 0)
G.add_edge(17, 16, weight = 0)
G.add_edge(16, 1, weight = 0)
G.add_edge(14, 11, weight = 0)
G.add_edge(10, 3, weight = 0)
G.add_edge(10, 4, weight = 0)
G.add_edge(7, 4, weight = 0)

edges = list(G.edges())
comEdges = {}

for i in range(0, G.number_of_edges()):
    comEdges[edges[i]] = Wavelength()


# Generate source and destination
while True:
    check = False
    source = np.random.randint(1, 18, number_of_requests)
    destination = np.random.randint(1, 18, number_of_requests)
    for i in range(0, number_of_requests):
        if source[i] == destination[i]:
            check = True
    if not check:
        break


# Generate exponential interval time and holding time of requests
def generate_time(mean, number_of_requests):
    while True:
        check = False
        time = np.random.exponential(mean, number_of_requests)
        for t in time:
            if t == 0: check = True
        if not check: break
    return time


events = generate_time(1/lam, number_of_requests)
holding_time = generate_time(1/muy, number_of_requests)

s = 0
time = []
for e in events:
    s += e
    time.append(s)

timeline = []
for i in range(0, number_of_requests):
    timeline.append(time[i] + holding_time[i])

timeNew = time + timeline
# print("before",timeNew)

for i in range(len(timeNew)):
    for j in range(len(timeNew) - 1 - i):
        if timeNew[j] > timeNew[j+1]:
            timeNew[j], timeNew[j+1] = timeNew[j+1], timeNew[j]

Req = []
for i in range(0, number_of_requests):
    req = Requests(time[i], timeline[i], source[i], destination[i], i)
    Req.append(req)

Events = []
for i in range(len(timeNew)):
    for req in Req:
        if req.inTime == timeNew[i]:
            Events.append(req)
        elif req.outTime == timeNew[i]:
            temp = cp.copy(req)
            temp.isCall = 1
            Events.append(temp)


print(len(Events))


def bindingEdges(req):
    print("src:", req.source)
    print("des:", req.des)
    # while True:
    #     check = False
    req.path = nx.shortest_path(G, req.source, req.des, weight = 'weight')
    req.printDetails()
    for e in Events:
        if e != req and e.inTime == req.inTime:
            e.path = req.path
            e.printDetails()
            print()
    # for i in range(0, len(req.path) - 1):
    #     for edges in comEdges:
    #         if edges == (req.path[i], req.path[i+1]) or edges == (req.path[i+1], req.path[i]):
    #             comEdges[edges].fiber1[1] += 1
    #             print(edges, comEdges[edges].fiber1)

            # if G[req.path[i]][req.path[i+1]]['weight'] < 1:
            #     G[req.path[i]][req.path[i + 1]]['weight'] += 1
            # elif

def releaseEdges(req):
    req.path = []


for e in Events:
    if e.isCall == 0:
        bindingEdges(e)
# for e in Events:
#     if e != Events[0] and e.inTime == Events[0].inTime:
#         e.path = Events[0].path
#         e.printDetails()

# print(G.number_of_nodes())
# print(events)
# print(holding_time)
# print(time)
# print(timeline)
# print("final source:     ", source)
# print("final destination:", destination)