import gym

import uncertain_pddlgym


def test_make_uncertain_env():
    env = gym.make("UncertainPDDLEnvUncertain_sokoban-v0", uncertainty=[])

def test_make_3x3_env():
    env = gym.make("UncertainPDDLEnvUncertain_sokoban-v0", uncertainty=[])
    env.fix_problem_index(0)
    env.reset()
