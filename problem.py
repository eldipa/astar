import random

def generate_problem(num_cities, ProblemDefinition):
   # build the cities
   cities = list(range(num_cities))

   # create the solution first
   shortest_path_costs = [random.randint(1, 10) for i in cities]

   shortest_path_permutation = list(cities) # copy
   random.shuffle(shortest_path_permutation) # this is the solution

   shortest_path_total_cost = sum(shortest_path_costs)

   # create the city mesh (all the paths and costs)
   base = int(shortest_path_total_cost / (len(cities) * 0.5))
   COST_FROM_TO = dict([((i,j), random.randint(1, 10) + base) for i in cities for j in cities])

   # explicit cost for self
   for i in cities:
      COST_FROM_TO[(i,i)] = 0

   # force the costs for the solution
   for i in range(len(shortest_path_permutation) - 1):
      COST_FROM_TO[(shortest_path_permutation[i], shortest_path_permutation[i+1])] = shortest_path_costs[i]

   # force the cost of the last path (close the circuit)
   COST_FROM_TO[(shortest_path_permutation[-1], shortest_path_permutation[0])] = shortest_path_costs[-1]
   
   ProblemDefinition.CITIES = frozenset(cities)
   ProblemDefinition.SOLUTION = shortest_path_permutation
   ProblemDefinition.SOLUTION_COST = shortest_path_total_cost
   ProblemDefinition.COST_FROM_TO = COST_FROM_TO
   ProblemDefinition.COUNT_CITIES = len(cities)
   

def load_problem(filename, ProblemDefinition, filename_solution=None):

   with open(filename, 'r') as source:
      data = map(int, filter(None, map(lambda s: s.strip(), source.read().split(";"))))

   count_of_cities = data[0]
   costs = data[1:]

   expected_count_of_costs = count_of_cities * int(count_of_cities/2) if \
                                                         count_of_cities % 2 == 1 \
                             else count_of_cities * ((count_of_cities/2)-1) + (count_of_cities/2)
   assert len(costs) == expected_count_of_costs

   cities = range(count_of_cities)
   N = len(cities)

   # create the city mesh (all the paths and costs)
   COST_FROM_TO = {}
   x = 0
   for i in range(N-1):
      for j in range(i+1, N):
         COST_FROM_TO[(i,j)] = COST_FROM_TO[(j,i)] = costs[x]
         x += 1

   # explicit cost for self
   for i in cities:
      COST_FROM_TO[(i,i)] = 0

   ProblemDefinition.CITIES = frozenset(cities)
   ProblemDefinition.SOLUTION = None # unknown
   ProblemDefinition.SOLUTION_COST = None # unknown
   ProblemDefinition.COST_FROM_TO = COST_FROM_TO
   ProblemDefinition.COUNT_CITIES = len(cities)
   
   if filename_solution:
      with open(filename_solution, 'r') as source:
         data = map(int, filter(None, map(lambda s: s.strip(), source.read().split(";")))[:-1])
         
      ProblemDefinition.SOLUTION = tuple(data[:len(cities)+1])
      ProblemDefinition.SOLUTION_COST = data[len(cities)+1]

def test(filename, filename_solution):
   import astar
   load_problem(filename, astar.ProblemDefinition, filename_solution)

   solution_node = astar.find_path([0])
   solution = str(tuple(solution_node.path))
   solution_cost = solution_node.path_cost

   expected_solution = str(astar.ProblemDefinition.SOLUTION)
   expected_cost = astar.ProblemDefinition.SOLUTION_COST

   if expected_solution != solution or expected_cost != solution_cost:
      print "Solution found    : (%i) %s" % (solution_cost, solution)
      print "Solution expected : (%i) %s" % (expected_cost, expected_solution)

   else:
      print "Ok"
