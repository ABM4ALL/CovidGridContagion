import random
from typing import TYPE_CHECKING

from Melodie import GridAgent

if TYPE_CHECKING:
    from source.scenario import CovidScenario
    from Melodie import AgentList
    from source.grid import CovidSpot
    from source.grid import CovidGrid


class CovidAgent(GridAgent):
    scenario: "CovidScenario"
    grid: "CovidGrid"
    spot: "CovidSpot"

    def set_category(self):
        self.category = 0

    def setup(self):
        self.x: int = 0
        self.y: int = 0
        self.health_state: int = 0
        self.age_group: int = 0

    def move(self):
        spot: "CovidSpot" = self.grid.get_spot(self.x, self.y)
        stay_prob = spot.stay_prob
        if random.uniform(0, 1) > stay_prob:
            move_radius = 1
            self.rand_move_agent(move_radius, move_radius)

    def infection(self, agents: "AgentList[CovidAgent]"):
        neighbors = self.grid.get_neighbors(self)
        for neighbor_category, neighbor_id in neighbors:
            neighbor_agent: "CovidAgent" = agents.get_agent(neighbor_id)
            if neighbor_agent.health_state == 1:
                if random.uniform(0, 1) < self.scenario.infection_prob:
                    self.health_state = 1
                    break

    def health_state_transition(self):
        if self.health_state == 1:
            transition_probs: dict = self.scenario.get_transition_probs(self.age_group)
            rand = random.uniform(0, 1)
            if rand <= transition_probs["s1_s1"]:
                pass
            elif transition_probs["s1_s1"] < rand <= transition_probs["s1_s1"] + transition_probs["s1_s2"]:
                self.health_state = 2
            else:
                self.health_state = 3
