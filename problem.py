import random

def generate_problem(num_cities, ProbleDefinition):
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
   
   ProbleDefinition.CITIES = cities
   ProbleDefinition.SOLUTION = shortest_path_permutation
   ProbleDefinition.COST_FROM_TO = COST_FROM_TO
   ProbleDefinition.COUNT_CITIES = len(cities)
