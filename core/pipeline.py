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
        subprocess.call(['cd', self.curr_build_dir, '&&', 'git', 'checkout', '--verbose', self.branch])

    def run_job(self):
        if self.pipeline_name not in self.tasks.keys():
            print(self.pipeline_name + ' failed! Invalid task.')
            exit(1)

        for task in self.pipelines[self.pipeline_name]:
            if task not in self.tasks.keys():
                print(task + ' failed! Invalid task.')
                exit(1)

            cmd = self.tasks[self.pipeline_name].split()

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, cwd=self.curr_build_dir)
            for line in iter(p.stdout.readline, b''):
                print(line)
            p.stdout.close()
