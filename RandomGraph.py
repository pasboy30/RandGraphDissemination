# Imports
import matplotlib.pyplot as plt
from networkx import nx
import math
import random


rand = random.SystemRandom()

# Handy Functions
def avg(lst):
    return sum(lst)/ len(lst)
def irresponsive_node_prob():
    return rand.uniform(0,1)



# Graph Variables
n = 100
k = math.ceil(math.log(n,math.exp(1)))
itr = 0 
edge_iterations = []
for round in range(1,k+1):
    itr = round
    # Initialize graph
    G = nx.DiGraph()
    for x in range(0,n):
        G.add_node(x)

    # Node Parameters
    cache = {}
    count = {}
    for x in range(0,n):
        cache[x] = list(range(0,n))
        cache[x].remove(x)
        count[x] = 0

    # Gossip Initiator
    leader = rand.randint(0,n-1)
    # Record of nodes doing gossip. Number of interations = 2
    locale = set()
    # Processing timeline of nodes based on events held
    queue = []
    locale.add(leader)

    print("Leader selected: " + str(leader))
    print("--------------------------------------------")
    queue.append(leader)
    pointer = 0
    while (len(queue) != pointer):
        active_node = queue[pointer]
        if count[active_node] < itr:
            for _ in range(k):
                g_node_index = rand.randint(0,len(cache[active_node])-1)
                print(str(active_node) + " Selected " + str(cache[active_node][g_node_index]))
                p = irresponsive_node_prob()
                if p > 0.25:
                    queue.append(cache[active_node][g_node_index])
                    G.add_edge(active_node,cache[active_node][g_node_index])
                    cache[active_node].pop(g_node_index)
                else:
                    continue
            print("Locale:" + str(locale))
            print(queue)
            print("-----------------------------------------------")
            count[active_node] += 1
            pointer += 1
        else:
            locale.add(active_node)
            pointer += 1
    print("Sorted queue :" + str(queue.sort()))
    print(len(G.edges))
    edge_iterations.append(len(G.edges))

    print("+==========================================================+ ")
    print("+==========================================================+ ")
    print("+==========================================================+ ")
    print("Power Law Analysis")

    # for x in range(0,n):
    #     print("Degree of " + str(x) + ":" +  str(G.degree[x]))

    degrees = []
    for x in range(0,n):
        print("Indegree of " + str(x) + " is  " +  str(G.in_degree(x)))
        print("OutDegree of " + str(x) + " is  " +  str(G.out_degree(x)))
    for x in range(0,n):
        degrees.append(G.degree[x])
    mean = avg(degrees)

    power_law_analysis = {i:degrees.count(i) for i in degrees}
    print(power_law_analysis)
    X = []
    Y = []
    for zz in power_law_analysis.keys():
        X.append(zz)
        Y.append(power_law_analysis[zz])

    print(X)
    print(Y)
    plt.clf()
    plt.scatter(X,Y)
    plt.ylabel("# of nodes")
    plt.xlabel("Degree of node")
    plt.vlines(x=k,colors='r',ymin= 0 , ymax= 100 )
    plt.vlines(x=mean,colors='b',ymin= 0 , ymax= 100 )
    plt.title("# Edges = " + str(len(G.edges)))
    plt.savefig("DD"+"_itr"+str(itr)+".png")
    plt.clf()
    nx.draw(G,with_labels=True)
    plt.show()
    plt.savefig("G"+"_itr"+str(itr)+".png")
Y1 = edge_iterations
X1 = [range(1,len(edge_iterations)+1)]
plt.scatter(X1,Y1)
plt.ylabel("# of edges")
plt.xlabel("iterations (itr)")
plt.title("Growth in Graph Connectivity (Density)")
plt.savefig("Growth analysis"+"_itr"+str(itr)+".png")
plt.clf()