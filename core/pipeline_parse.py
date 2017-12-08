import yaml


def pipeline_parse(file):
    """
    Parses a YAML file
    :param file: path to the YAML file
    :return: parsed file
    """
    pipeline_desc = None

    with open(file, 'r') as f:
        pipeline_desc = yaml.load(f)

    branch = pipeline_desc.get('branch', 'master')

    tasks = {}
    for t in pipeline_desc['tasks']:
        for task_name, task_cmd in t.items():
            tasks[task_name] = task_cmd['cmd']

    pipelines = {}
    for p in pipeline_desc['pipelines']:
        for job_name, job_tasks in p.items():
            pipelines[job_name] = job_tasks

    return branch, tasks, pipelines
