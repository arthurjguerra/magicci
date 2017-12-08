from os import path, mkdir
from core.pipeline_parse import pipeline_parse
from datetime import datetime
from core.which import which
import subprocess


class Pipeline:
    def __init__(self, root_dir, pipeline_name, repository):
        self.pipeline_name = pipeline_name
        self.repo = repository

        self.curr_build_dir = path.join(root_dir, 'builds', 'build_' + datetime.now().isoformat())

        self.check_build_requirements()
        self.clone_repository()

        pipeline_file = path.join(self.curr_build_dir, 'pipeline.yml')
        self.branch, self.tasks, self.pipelines = pipeline_parse(pipeline_file)

        self.checkout()

    def check_build_requirements(self):
        for exe in ['git', 'mvn', 'unzip', 'java']:
            if not path.exists(which(exe)):
                print('Could not find ' + exe)
                exit(1)

    def clone_repository(self):
        mkdir(self.curr_build_dir)
        subprocess.call(['git', 'clone', '--progress', '--verbose', self.repo, self.curr_build_dir])

    def checkout(self):
        subprocess.call(['git', 'checkout', self.branch], cwd=self.curr_build_dir)

    def run_job(self):
        for task in self.pipelines[self.pipeline_name]:
            if task not in self.tasks.keys():
                print(task + ' failed! Invalid task.')
                exit(1)

            cmd = self.tasks[task].split()

            if subprocess.call(cmd, cwd=self.curr_build_dir) > 0:
                print('\n --------- Build Failed -------- \n')
                exit(1)
