from sortedcontainers import SortedList

from .common import Node, NoSolutionError


def uniform_cost_graph(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = SortedList([starting_node], key=lambda n: -n.path_cost)
    explored = set()
    iterations = 0
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if (child.state not in explored and
                    child.state not in [n.state for n in frontier]):
                if problem.goal_test(child.state):
                    return child.solution()
                frontier.add(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError()


def uniform_cost_tree(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = SortedList([starting_node], key=lambda n: -n.path_cost)
    iterations = 0
    while frontier:
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if problem.goal_test(child.state):
                return child.solution()
            frontier.add(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError()