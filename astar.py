from heapq import heapify, heappush, heappop

class ProbleDefinition(object):
   pass # define me


class Node(object):
   def __init__(self, name, parent):
      self.is_closed = False
      self.is_garbage = False
      self.name = name
      self.parent = parent
      if parent:
         self.id = parent.id.union(frozenset([self.name]))
         self.path_length = parent.path_length + 1
         self.partial_cost_G = parent.partial_cost_G + parent.cost_to_go_to(self)
      else:
         self.id = frozenset([self.name])
         self.path_length = 1
         self.partial_cost_G = 0

      self.predicted_total_cost_F = self.partial_cost_G + self.heuristic_remain_cost_H()

   def update(self, other_node):
      assert other_node.id == self.id
      self.is_closed = other_node.is_closed
      self.name =  other_node.name
      self.parent =  other_node.parent
      self.path_length =  other_node.path_length
      self.partial_cost_G =  other_node.partial_cost_G
      self.predicted_total_cost_F =  other_node.predicted_total_cost_F

   def heuristic_remain_cost_H(self):
      return ProbleDefinition.COUNT_CITIES - len(self.id)

   def cost_to_go_to(self, to_node):
      return ProbleDefinition.COST_FROM_TO[(self.name, to_node.name)]

   def is_solution(self):
      return self.path_length == len(ProbleDefinition.CITIES)

   def next_nodes(self):
      all_cities = set(ProbleDefinition.CITIES);
      next_cities = all_cities - self.id # not visited cities

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

   open_list_by_cost = [(n.predicted_total_cost_F, n) for n in open_list]
   heapify(open_list_by_cost)
   open_list = dict([(n.id, n) for F, n in sorted([(n.predicted_total_cost_F, n) for n in open_list])])
 
   #import pdb; pdb.set_trace()  
   while open_list:
      # search for the minimun next node
      current_node = open_list_by_cost[0][1]

      if current_node.is_garbage:
         heappop(open_list_by_cost) # remove and discard, this node is just garbage
         continue

      # did we found the solution?
      if current_node.is_solution():
         return current_node

      # we still searching the solution,
      del open_list[current_node.id]
      heappop(open_list_by_cost)
      current_node.is_closed = True

      # review the next nodes (adjacents)
      next_nodes = current_node.next_nodes()
      
      open_list_by_cost_unordered = False
      for n in next_nodes:
         if n.is_closed:
            continue # ignore this

         if n.id not in open_list:
            open_list[n.id] = n
            heappush(open_list_by_cost, (n.predicted_total_cost_F, n))
            continue    # this is new, add it to process later

         assert n.id in open_list   # if we reach here, the node is already know

         old_node = open_list[n.id]
         if old_node.partial_cost_G > n.partial_cost_G:
            open_list[n.id] = n
            old_node.is_garbage = True # dont pop the old node, just mark it as garbage
            heappush(open_list_by_cost, (n.predicted_total_cost_F, n)) 
            continue    # the node is better, update!

         # nothing, the node is worst, ignore it

   return None # no path found, sorry
