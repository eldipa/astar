# OKs
#-----

def null(ProblemDefinition, node):
  return 0

def remain_hops_by_min(ProblemDefinition, node):
  return (ProblemDefinition.COUNT_CITIES - len(node.path)) * ProblemDefinition.MIN

def sum_of_N_min_hops(ProblemDefinition, node):
  return sum(ProblemDefinition.MINs[:(ProblemDefinition.COUNT_CITIES - len(node.path) + 1)])


# Suboptimal solutions
#----------------------

def remain_hops_by_mean(ProblemDefinition, node):
  return (ProblemDefinition.COUNT_CITIES - len(node.path) + 1) * ProblemDefinition.MEAN

