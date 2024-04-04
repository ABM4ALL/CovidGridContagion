from Melodie import Spot, Grid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scenario import CovidScenario


class CovidSpot(Spot):
    def setup(self):
        self.stay_prob = 0.0


class CovidGrid(Grid):
    scenario: "CovidScenario"

    def setup(self):
        self.set_spot_property("stay_prob", self.scenario.grid_stay_prob)
