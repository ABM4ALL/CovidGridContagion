from typing import Any, Dict
from Melodie import Scenario
import numpy as np
import pandas as pd


class CovidScenario(Scenario):
    def setup(self):
        self.period_num: int = 0
        self.agent_num: int = 0
        self.grid_x_size: int = 0
        self.grid_y_size: int = 0
        self.initial_infected_percentage: float = 0.0
        self.young_percentage: float = 0.0
        self.infection_prob: float = 0.0

    def load_data(self):
        self.df_transition_prob = self.load_dataframe(
            "Parameter_AgeGroup_TransitionProb.xlsx"
        )
        self.setup_transition_probs(self.df_transition_prob)
        self.simulator_scenarios = self.load_dataframe("SimulatorScenarios.xlsx")
        self.id_health_state = self.load_dataframe("ID_HealthState.xlsx")
        self.id_age_group = self.load_dataframe("ID_AgeGroup.xlsx")
        self.grid_stay_prob = self.load_matrix("Parameter_GridStayProb.xlsx")
        self.parameter_agent_params = self.generate_agent_dataframe()

    def setup_transition_probs(self, df: pd.DataFrame):
        self.transition_probs = {
            0: {
                "s1_s1": df.at[0, "prob_s1_s1"],
                "s1_s2": df.at[0, "prob_s1_s2"],
                "s1_s3": df.at[0, "prob_s1_s3"],
            },
            1: {
                "s1_s1": df.at[1, "prob_s1_s1"],
                "s1_s2": df.at[1, "prob_s1_s2"],
                "s1_s3": df.at[1, "prob_s1_s3"],
            },
        }

    def get_transition_probs(self, id_age_group: int):
        return self.transition_probs[id_age_group]

    @staticmethod
    def init_health_state(scenario: "CovidScenario"):
        state = 0
        if np.random.uniform(0, 1) <= scenario.initial_infected_percentage:
            state = 1
        return state

    @staticmethod
    def init_age_group(scenario: "CovidScenario"):
        age_group = 0
        if np.random.uniform(0, 1) > scenario.young_percentage:
            age_group = 1
        return age_group

    def generate_agent_dataframe(self):
        assert self.agent_num != 0

        def generator_func(id: int, scenario: "CovidScenario") -> Dict[str, Any]:
            return {
                "id_scenario": scenario.id,
                "id": id,
                "health_state": self.init_health_state(scenario),
                "age_group": self.init_age_group(scenario),
            }

        return pd.DataFrame(
            [generator_func(agent_id, self) for agent_id in range(self.agent_num)]
        )
