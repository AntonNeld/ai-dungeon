from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.actions import Action


class SingularAI(BaseModel):
    kind: Literal["singular"]
    action: Action

    def next_action(self, percept, random_generator):
        return self.action
