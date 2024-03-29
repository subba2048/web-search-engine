import sys


def ret_graph():
    return {
        'A': {'B':5.5, 'C':2, 'D':6},
        'B': {'A':5.5, 'E':3},
        'C': {'A':2, 'F':2.5},
        'D': {'A':6, 'F':1.5},
        'E': {'B':3, 'J':7},
        'F': {'C':2.5, 'D':1.5, 'K':1.5, 'G':3.5},
        'G': {'F':3.5, 'I':4},
        'H': {'J':2},
        'I': {'G':4, 'J':4},
        'J': {'H':2, 'I':4},
        'K': {'F':1.5}
    }





start = 'A'                 
dest = 'k'                  
visited = []                
stack = []                  
graph = ret_graph()
path = []


stack.append(start)                  
visited.append(start)                
while stack:                         
    curr = stack.pop()            
    path.append(curr)
    for neigh in graph[curr]:        
        if neigh not in visited:       
            visited.append(neigh)       
            stack.append(neigh)         
            if neigh == dest :            
                print("FOUND:", neigh)
                print(path)
                sys.exit(0)
print("Not found")
print(path)


# graph = {'A': ['B', 'C', 'E'],
#          'B': ['A','D', 'E'],
#          'C': ['A', 'F', 'G'],
#          'D': ['B'],
#          'E': ['A', 'B','D'],
#          'F': ['C'],
#          'G': ['C']}
         
         
# def bfs(graph, initial):
    
#     visited = []
    
#     queue = [initial]
 

#     while queue:
        
#         node = queue.pop(0)
#         if node not in visited:
            
#             visited.append(node)
#             neighbours = graph[node]
 
            
#             for neighbour in neighbours:
#                 queue.append(neighbour)
#     return visited
 
# print(bfs(graph,'B'))