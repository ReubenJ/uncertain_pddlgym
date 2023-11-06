import gym
import uncertain_pddlgym


def test_make_uncertain_env():
    env = gym.make("UncertainPDDLEnvUncertain_sokoban-v0")
