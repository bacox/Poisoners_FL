def generate_experiment_ids(start_idx, num_exp, exp_prefix: str = ''):
    """
    Generate the filenames for all experiment IDs.

    :param start_idx: start index for experiments
    :type start_idx: int
    :param num_exp: number of experiments to run
    :type num_exp: int
    """
    log_files = []
    results_files = []
    models_folders = []
    worker_selections_files = []

    for i in range(num_exp):
        idx = start_idx + i
        exp_name = f'{exp_prefix}_{idx}'

        log_files.append(f'logs/{exp_name}.log')
        results_files.append(f'{exp_name}_results.csv')
        models_folders.append(f'{exp_name}_models')
        worker_selections_files.append(f'{exp_name}_workers_selected.csv')

    return log_files, results_files, models_folders, worker_selections_files
