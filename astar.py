COST_FROM_TO = {
   (1,1): 0,
   (1,2): 9,
   (1,3): 9,
   (1,4): 1,
   (2,1): 1,
   (2,2): 0,
   (2,3): 1,
   (2,4): 1,
   (3,1): 1,
   (3,2): 1,
   (3,3): 0,
   (3,4): 1,
   (4,1): 1,
   (4,2): 1,
   (4,3): 9,
   (4,4): 0,
}

CITIES = [1, 2, 3, 4]

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

      self.total_predicted_cost_F = self.partial_cost_G + self.heuristic_remain_cost_H()

   def heuristic_remain_cost_H(self):
      return 0

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
      return str(self.name)

   def __repr__(self):
      return str(self.name)

def find_path(possible_starting_points):
   open_list   = []
   closed_list = []

   # set up, initialize the open list
   for p in possible_starting_points:
      n = Node(name=p, parent=None)
      open_list.append(n)

 
   #import pdb; pdb.set_trace()  
   while open_list:
      # search for the minimun next node
      min_cost = 2**30
      current_node = None
      for n in open_list:
         if n.total_predicted_cost_F < min_cost:
            min_cost = n.total_predicted_cost_F
            current_node = n


      # did we found the solution?
      if current_node.is_solution():
         return current_node

      # we still searching the solution,
      open_list.remove(current_node)
      closed_list.append(current_node)

      # review the next nodes (adjacents)
      next_nodes = current_node.next_nodes()
      
      for n in next_nodes:
         if n.name in [q.name for q in closed_list]:
            continue # ignore this

         if n.name not in [q.name for q in open_list]:
            open_list.append(n)
            continue    # this is new, add it to process later

         assert n.name in [q.name for q in open_list]   # if we reach here, the node is already know

         old_node = filter(lambda q: q.name == n.name, open_list)[0]
         if old_node.partial_cost_G > n.partial_cost_G:
            open_list.remove(old_node)
            open_list.append(n)
            continue    # the node is better, update!

         # nothing, the node is worst, ignore it

   return None # no path found, sorry
