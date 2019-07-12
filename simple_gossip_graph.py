# Imports
import matplotlib.pyplot as plt
from networkx import nx
import math
import random
# Handy Functions
def avg(lst):
    return sum(lst)/ len(lst)
def irresponsive_node_prob():
    return random.uniform(0,1)
def faulty_node_candidates(n):
    faulty = []
    x = list(range(100))
    for i in range(n):
        i = random.randint(0,len(x)-1)
        faulty.append(x[i])
        x.pop(i)
    return faulty

# Graph Variables
n = 100
k = math.ceil(math.log(n,math.exp(1)))
faulty = faulty_node_candidates(50)
# Initialize graph
G = nx.Graph()
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
leader = random.randint(0,n-1)
# Record of nodes doing gossip. #interations = 2
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
    if count[active_node] < 2:
        for _ in range(k):
            g_node_index = random.randint(0,len(cache[active_node])-1)
            print(str(active_node) + " Selected " + str(cache[active_node][g_node_index]))
            if cache[active_node][g_node_index] in faulty:
                p = irresponsive_node_prob()
                if p > 0.7:
                    queue.append(cache[active_node][g_node_index])
                    G.add_edge(active_node,cache[active_node][g_node_index])
                    cache[active_node].pop(g_node_index)
            else:
                queue.append(cache[active_node][g_node_index])
                G.add_edge(active_node, cache[active_node][g_node_index])
                cache[active_node].pop(g_node_index)
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

print("+==========================================================+ ")
print("+==========================================================+ ")
print("+==========================================================+ ")
print("Power Law Analyis")

# for x in range(0,n):
#     print("Degree of " + str(x) + ":" +  str(G.degree[x]))
degrees = []
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

plt.scatter(X,Y)
plt.ylabel("# of nodes")
plt.xlabel("Degree of node")
plt.vlines(x=k,colors='r',ymin= 0 , ymax= 100 )
plt.vlines(x=mean,colors='b',ymin= 0 , ymax= 100 )
print(faulty)
# nx.draw(G,with_labels=True)
plt.show()