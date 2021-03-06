from typing import Tuple, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.actions import Action, PickUp, DoNothing, Move
from .problems.pathfinding import PathfindingProblem, get_heuristic
from .search import a_star_graph, NoSolutionError


class ExploringVacuumAI(BaseModel):
    # Exploring vacuum cleaner agent for exercise 2.11d.
    kind: Literal["exploringVacuum"]
    passable: Dict[str, bool] = {}
    position: Tuple[int, int] = (0, 0)
    last_action: Action = Field(DoNothing(), alias="lastMove")

    def update_state_percept(self, percept):
        x = percept["position"]["x"]
        y = percept["position"]["y"]
        if self.position != (x, y):
            self.position = (x, y)
            self.passable[str((x, y))] = True
        elif self.last_action.action_type == "move":
            if self.last_action.direction == "up":
                self.passable[str((x, y+1))] = False
            elif self.last_action.direction == "down":
                self.passable[str((x, y-1))] = False
            elif self.last_action.direction == "left":
                self.passable[str((x-1, y))] = False
            elif self.last_action.direction == "right":
                self.passable[str((x+1, y))] = False

    def next_action(self, percept, random_generator):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return PickUp()

        targets = set()
        obstructions = set()

        for key in self.passable:
            coords = key[1:-1].split(",")
            x = int(coords[0])
            y = int(coords[1])
            if self.passable[key]:
                for pos in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if str(pos) not in self.passable:
                        targets.add(pos)
            else:
                obstructions.add((x, y))
        if not targets:
            return DoNothing()
        my_x = percept["position"]["x"]
        my_y = percept["position"]["y"]
        problem = PathfindingProblem((my_x, my_y), targets, obstructions, [])
        try:
            plan = a_star_graph(problem, get_heuristic(problem))
            return Move(direction=plan[0])
        except NoSolutionError:
            return DoNothing()

    def update_state_action(self, action):
        self.last_action = action
