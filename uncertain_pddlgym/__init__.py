import os

from gym.envs.registration import register
from pddlgym import sokoban_render


def register_pddl_env(name, is_test_env, other_args):
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pddl")
    domain_file = os.path.join(dir_path, "{}.pddl".format(name.lower()))
    gym_name = name.capitalize()
    problem_dirname = name.lower()
    if is_test_env:
        gym_name += "Test"
        problem_dirname += "_test"
    problem_dir = os.path.join(dir_path, problem_dirname)

    register(
        id="UncertainPDDLEnv{}-v0".format(gym_name),
        entry_point="uncertain_pddlgym.core:UncertainPDDLEnv",
        kwargs=dict(
            {"domain_file": domain_file, "problem_dir": problem_dir, **other_args}
        ),
    )


for env_name, kwargs in [
    ("uncertain_sokoban", {"render": sokoban_render}),
]:
    other_args = {
        "raise_error_on_invalid_action": True,
    }
    kwargs.update(other_args)
    for is_test in [False, True]:
        register_pddl_env(env_name, is_test, kwargs)
