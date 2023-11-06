import os

import pytest
from pddlgym.structs import Literal, Predicate, Type, TypedEntity

from uncertain_pddlgym.core import ProbabilisticLiteral, UncertainPDDLEnv


def test_test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    domain_file = os.path.join(dir_path, "pddl/sokoban.pddl")
    problem_dir = os.path.join(dir_path, "pddl/test_uncertain_sokoban")

    at_predicate = Predicate("at", 2)
    thing = Type("thing")
    location = Type("location")
    player = TypedEntity("player-01", thing)
    pos_1 = TypedEntity("pos-6-4", location)
    pos_2 = TypedEntity("pos-6-5", location)
    lit_1 = Literal(predicate=at_predicate, variables=[player, pos_1])
    lit_2 = Literal(predicate=at_predicate, variables=[player, pos_2])

    uncertainty = [
        ProbabilisticLiteral(
            literals=[
                lit_1,
                lit_2,
            ],
            probabilities=[
                0.4,
                0.6,
            ],
        ),
    ]

    env = UncertainPDDLEnv(
        domain_file,
        problem_dir,
        uncertainty=uncertainty,
        raise_error_on_invalid_action=True,
        dynamic_action_space=True,
    )

    checks = 100

    which_lit = [0, 0]

    for _ in range(checks):
        obs, _ = env.reset()
        assert lit_1 in obs.literals or lit_2 in obs.literals
        assert not (lit_1 in obs.literals and lit_2 in obs.literals)
        if lit_1 in obs.literals:
            which_lit[0] += 1
        else:
            which_lit[1] += 1


    for i in range(2):
        assert which_lit[i] / checks == pytest.approx(
            uncertainty[0].probabilities[i], abs=0.1
        )

def test_empty_literal():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    domain_file = os.path.join(dir_path, "pddl/sokoban.pddl")
    problem_dir = os.path.join(dir_path, "pddl/test_uncertain_sokoban")

    clear = Predicate("clear", 1)
    location = Type("location")
    pos_1 = TypedEntity("pos-6-4", location)
    lit_1 = Literal(predicate=clear, variables=[pos_1])

    uncertainty = [
        ProbabilisticLiteral(
            literals=[
                lit_1,
                None
            ],
            probabilities=[
                0.5,
                0.5,
            ],
        ),
    ]

    env = UncertainPDDLEnv(
        domain_file,
        problem_dir,
        uncertainty=uncertainty,
        raise_error_on_invalid_action=True,
        dynamic_action_space=True,
    )

    checks = 100

    which_lit = [0, 0]

    for _ in range(checks):
        obs, _ = env.reset()
        if lit_1 in obs.literals:
            which_lit[0] += 1
        else:
            which_lit[1] += 1

    for i in range(2):
        assert which_lit[i] / checks == pytest.approx(
            uncertainty[0].probabilities[i], abs=0.1
        )
