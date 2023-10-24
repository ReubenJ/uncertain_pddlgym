from pddlgym.core import PDDLEnv
from dataclasses import dataclass
from pddlgym.structs import Literal

import numpy as np

from copy import deepcopy

@dataclass
class ProbabilisticLiteral:
    literals: list[Literal] | Literal
    probabilities: float

    def __init__(self, literals, probabilities):
        if not isinstance(literals, list):
            literals = [literals]
        
        assert sum(probabilities) == 1

        self.literals = literals
        self.probabilities = probabilities


class UncertainPDDLEnv(PDDLEnv):
    def __init__(self, *args, uncertainty: list[ProbabilisticLiteral]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uncertainty = uncertainty

        for problem in self.problems:
            for uncertain_set in self.uncertainty:
                for literal in uncertain_set.literals:
                    if literal in problem.initial_state:
                        problem.initial_state = problem.initial_state - {literal}
                    assert all(var in problem.objects for var in literal.variables)
                    assert literal.predicate in problem.predicates

        self.problems_initial = deepcopy(self.problems)



    def reset(self):
        self.problems = deepcopy(self.problems_initial)
        
        for uncertain_set in self.uncertainty:
            chosen_literal = np.random.choice(uncertain_set.literals, p=uncertain_set.probabilities)
            for problem in self.problems:
                problem.initial_state = problem.initial_state.union({chosen_literal})

        return super().reset()