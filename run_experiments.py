import argparse
import yaml
from typing import Optional
import itertools
import copy
import federated_learning.utils as futil
import federated_learning.worker_selection as selection_strategy
from server import run_exp

parser = argparse.ArgumentParser(description='Execute multiple experiments at once')
parser.add_argument('config', metavar='config-file', type=str,
                    help='an integer for the accumulator')



def read_yaml(file: str) -> Optional[dict]:
    try:
        with open(args.config, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(f'Error while parsing yaml: {exc}')
    except FileNotFoundError:                    # <- with doesn't have an except clause.
        print(f'Cannot find file {args.config}')

def create_exp_variations(config: dict):
    variables: dict = config['variables']

    keys, values = zip(*variables.items())
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
    experiments = []
    for permutation in permutations_dicts:
        experiment = copy.deepcopy(config)
        exp_name = f'{experiment["exp_name"]}_d-{permutation["datasets"]}_n-{permutation["networks"]}_p-{permutation["percentages"]}_e-{permutation["effort"]}_m-{permutation["measurements"]}'
        experiment["exp_name"] = exp_name
        del experiment['variables']
        experiment.update(permutation)
        experiments.append(experiment)
    return experiments

def main(exp: dict):
    # for key in exp:
    #     print(f'key={key},\t value={exp[key]}')

    exp['replacement_method'] = getattr(futil, exp['replacement_method'])
    exp['client_selection_strategy'] = getattr(selection_strategy, exp['client_selection_strategy'])()

    for experiment_id in range(exp['start_exp_id'], exp['start_exp_id'] + exp['num_exp']):
        run_exp(**exp, idx=experiment_id)


if __name__ == '__main__':

    args = parser.parse_args()
    yaml_obj = read_yaml(args.config)
    if yaml_obj is None:
        exit(1)

    # Continue with normal execution
    print('File is read')
    print(yaml_obj)
    exps = create_exp_variations(yaml_obj)

    for exp in exps:
        main(exp)