from heapq import heapify, heappush, heappop

COUNT_CITIES = 10

COST_FROM_TO = dict([((i,j), 1) for i in range(COUNT_CITIES) for j in range(COUNT_CITIES)])

for i in range(COUNT_CITIES):
   COST_FROM_TO[(i,i)] = 0

CITIES = list(range(COUNT_CITIES))

def HeuristicCost(node):
   return 0

class Node(object):
   def __init__(self, name, parent):
      self.name = name
      self.parent = parent
      if parent:
         self.path_length = parent.path_length + 1
         self.partial_cost_G = parent.partial_cost_G + parent.cost_to_go_to(self)
      else:
         self.path_length = 1
         self.partial_cost_G = 0

      self.id = frozenset(self.build_path())
      self.predicted_total_cost_F = self.partial_cost_G + self.heuristic_remain_cost_H()

   def heuristic_remain_cost_H(self):
      return COUNT_CITIES - len(self.build_path())

   def cost_to_go_to(self, to_node):
      return COST_FROM_TO[(self.name, to_node.name)]

   def is_solution(self):
      return self.path_length == len(CITIES)

   def next_nodes(self):
      all_cities = set(CITIES);
      next_cities = all_cities - set(self.build_path()) # not visited cities

      nodes = []
      for c in next_cities:
         n = Node(name=c, parent=self)
         nodes.append(n)

      return nodes

   def build_path(self):
      if self.parent:
         return self.parent.build_path() + [self.name]
      else:
         return [self.name]

   def __str__(self):
      return str(self.name) + " -> " + str(self.build_path())

   def __repr__(self):
      return str(self.name) + " -> " + str(self.build_path())


def find_path(possible_starting_points):
   open_list   = []
   closed_list = []

   # set up, initialize the open list
   for p in possible_starting_points:
      n = Node(name=p, parent=None)
      open_list.append(n)

   open_list = [n for F, n in sorted([(n.predicted_total_cost_F, n) for n in open_list])]
   assert 0 < open_list[0] and all([open_list[i] <= open_list[i+1] for i in range(len(open_list)-1)])
 
   #import pdb; pdb.set_trace()  
   while open_list:
      # search for the minimun next node
      open_list = [n for F, n in sorted([(n.predicted_total_cost_F, n) for n in open_list])]
      assert 0 < open_list[0] and all([open_list[i] <= open_list[i+1] for i in range(len(open_list)-1)])
      
      current_node = open_list[0]

      # did we found the solution?
      if current_node.is_solution():
         return current_node

      # we still searching the solution,
      del open_list[0]
      closed_list.append(current_node)

      # review the next nodes (adjacents)
      next_nodes = current_node.next_nodes()
      
      for n in next_nodes:
         if n.id in [q.id for q in closed_list]:
            continue # ignore this

         if n.id not in [q.id for q in open_list]:
            open_list.append(n)
            continue    # this is new, add it to process later

         assert n.id in [q.id for q in open_list]   # if we reach here, the node is already know

         old_node = filter(lambda q: q.id == n.id, open_list)[0]
         if old_node.partial_cost_G > n.partial_cost_G:
            open_list.remove(old_node)
            open_list.append(n) 
            continue    # the node is better, update!

         # nothing, the node is worst, ignore it

   return None # no path found, sorry
