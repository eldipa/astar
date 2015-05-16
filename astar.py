from heapq import heapify, heappush, heappop

class ProblemDefinition(object):
  pass # define me


class Node(object):
  __slots__ = ('is_closed', 'is_garbage',
               'path', 'path_cost',
               'is_solution',
               'name',
               'predicted_total_cost_F', )

  def __init__(self, path, path_cost):
     self.is_closed = False
     self.is_garbage = False

     self.path = path
     self.path_cost = path_cost

     self.is_solution = (len(path) == ProblemDefinition.COUNT_CITIES + 1)
     if self.is_solution:
        self.name = "PossibleSolution"
     else:
        self.name = (self.path[0], frozenset(self.path[1:-1]), self.path[-1])

     self.predicted_total_cost_F = self.path_cost + ProblemDefinition().heuristic_function(self)

  def next_nodes(self):
     if len(self.path) == ProblemDefinition.COUNT_CITIES:
        return [Node(path = self.path + (self.path[0],),
                     path_cost = self.path_cost + ProblemDefinition.COST_FROM_TO[(self.path[-1], self.path[0])])]
     else:
        assert len(self.path) < ProblemDefinition.COUNT_CITIES
        next_cities = ProblemDefinition.CITIES - set(self.path) # not visited cities

        return [Node(path = self.path + (next_city,),
                     path_cost = self.path_cost + ProblemDefinition.COST_FROM_TO[(self.path[-1], next_city)])
                       for next_city in next_cities]

  def __str__(self):
     return str(self.path) + " cost: " + str(self.path_cost)

  def __repr__(self):
     return str(self)


def find_path(possible_starting_points, heuristic_function, threshold_cost=2**30):
  try:
     ProblemDefinition.heuristic_function = heuristic_function
     open_list   = []
     closed_list = set()

     # set up, initialize the open list
     for p in possible_starting_points:
        n = Node(path=(p,), path_cost=0)
        open_list.append(n)

     open_list_by_cost = [(n.predicted_total_cost_F, n) for n in open_list]
     heapify(open_list_by_cost)
     open_list = dict([(n.name, n) for F, n in sorted([(n.predicted_total_cost_F, n) for n in open_list])])

     #import pdb; pdb.set_trace()
     while open_list:
        # search for the minimun next node
        current_node = open_list_by_cost[0][1]

        if current_node.is_garbage:
           heappop(open_list_by_cost) # remove and discard, this node is just garbage
           continue

        # did we found the solution?
        if current_node.is_solution:
           return current_node

        # we still searching the solution,
        del open_list[current_node.name]
        heappop(open_list_by_cost)
        closed_list.add(current_node.name)

        # review the next nodes (adjacents)
        next_nodes = current_node.next_nodes()

        for n in next_nodes:
           if n.name in closed_list:
              continue # ignore this

           if n.path_cost > threshold_cost:
              continue # discard this, is too expensive

           if n.name not in open_list:
              open_list[n.name] = n
              heappush(open_list_by_cost, (n.predicted_total_cost_F, n))
              continue    # this is new, add it to process later

           assert n.name in open_list   # if we reach here, the node is already know

           old_node = open_list[n.name]
           if old_node.path_cost > n.path_cost: # compare the "G" cost
              open_list[n.name] = n
              old_node.is_garbage = True # dont pop the old node, just mark it as garbage
              heappush(open_list_by_cost, (n.predicted_total_cost_F, n))
              continue    # the node is better, update!

           # nothing, the node is worst, ignore it

     return None # no path found, sorry
  except KeyboardInterrupt:
     print "best so far:", current_node.path_cost


def find_path_fast_start(possible_starting_points, heuristic_function, suboptimal_heuristic_function):
  solution = find_path(possible_starting_points, suboptimal_heuristic_function)

  threshold_cost = solution.path_cost
  print threshold_cost
  return find_path(possible_starting_points, heuristic_function, threshold_cost)
