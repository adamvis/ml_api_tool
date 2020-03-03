from __future__ import print_function, unicode_literals

from os import system, popen
from pyfiglet import Figlet
from PyInquirer import prompt
import pandas as pd

import io

from src.menu import *


##################################################################################
# Wrappers

def not_implemented(func):
    """ Print not implemente image instead of running the function. """
    def func_wrapper(obj, *args, **kwargs):
        print(" ------------------------------")
        print("| Feature not implemented yet! |")
        print(" ------------------------------")
        system("sleep 1")
    return func_wrapper

def log_error(func):
    """ Exit program as error appears, allowing to exit main loop and see tracebacks. """
    def func_wrapper(obj, *args, **kwargs):
        try:
            func(obj, *args)
            exit()
        except Exception as e:
            print(e)
            exit()
    return func_wrapper

def warm_farewell(func):
    """ State if command has been executed correctly """
    def func_wrapper(obj, *args, **kwargs):
        func(obj, *args, **kwargs)
        print(f"{func.__name__} executed correctly!")
        system("sleep 3")
    return func_wrapper

def click_off(attr=None):
    """ Avoids exiting mainloop when clicking with mouse over the terminal """
    def decorator(func):
        def func_wrapper(obj):
            try:
                func(obj)
            except KeyError as e:
                if attr == "usage":
                    exec(f"obj.{attr}=None")
                else:
                    return None
        return func_wrapper
    return decorator

##################################################################################
# APP

class Main:
    def __init__(self):
        """ Get tool workdir """
        self.program_path = "/".join(__file__.split("/")[:-1])
        self.intro()

    def intro(self):
        """ Print introduction """
        f = Figlet(font='slant')
        print(f.renderText('ML-API Tool'))
        print("Hi, welcome to ML-API managing tool")

    def ask_model_name(self):
        """ 
        Asks for model name.
        This name will be used to mount the directory build_<model_name> in the specified path.
        """
        res = prompt(model_name_q, style=style)
        self.model_name = res["model_name"]

    def ask_tag(self):
        """ Asks for tag for image repository"""
        res = prompt(in_path_q, style=style)
        return res["tag"]

    def ask_paths(self):
        """ 
        Asks for:
            - model directory (must contain):
                - __init__.py: where object "Model" is located;
                - requirements.txt: requirements to the model;
                - hyperparmeters.json: dictionary containing model parameters in a way that can be passed to it as Model(**trainingParms)
                - other scripts and dependecies of the model.
            - build directory: where to locate the staffered directory for deploying.
        """
        res = prompt(in_path_q, style=style)
        self.model_path = os.path.abspath(res["in_path"])
        res = prompt(out_path_q, style=style)  
        self.build_path = f"{os.path.abspath(res['out_path'])}/build_{self.model_name}"

    def ask_payload(self):
        res = prompt(pay_path_q, style=style)
        return os.path.abspath(res["payload_path"])

    @click_off(attr='usage')
    def ask_usage(self):        
        """ Main Menu """
        res = prompt(main_menu, style=style)
        self.usage = res["usage"]
    
    @warm_farewell
    def build(self):
        """ 
        Launch src/{cloud_provider}/build.sh with:
            -m : model path (asked after intro)
            -b : build path (asked after intro)
            -n : model name (asked after intro)
        """
        system(f"sh {self.program_path}/src/aws/build.sh -m {self.model_path} -b {self.build_path} -n {self.model_name}")

    # @click_off()
    def test_menu(self):
        """ Test menu """
        res = prompt(test_menu, style=style)
        return res["test"]
    
    # @click_off()
    def dm_menu(self):
        """ Docker Manager menu """
        res = prompt(dm_menu, style=style)
        return res["dm"]
    
    # @click_off()
    def deploy_menu(self):
        """ Docker Manager menu """
        res = prompt(deploy_menu, style=style)
        return res["deploy_usage"]

    @warm_farewell
    def launch_image(self):
        """ Build Docker image locally from build folder (defined after intro) """
        system(f"docker image build -t {app.model_name}_image {self.build_path}")
        system(f"docker container run --publish 8000:8080 --detach --name {app.model_name}_container {app.model_name}_image")

    @warm_farewell
    def train(self):
        """ Launch train on <local_image>:opt/program/ """
        system(f"sh {self.program_path}/src/aws/test/train_local.sh {app.model_name}_image {self.build_path}")

    @warm_farewell
    def serve(self):
        """ Launch serve on <local_image>:opt/program/ """
        system(f"sh {self.program_path}/src/aws/test/serve_local.sh {app.model_name}_image {self.build_path} {self.model_name}_inference")

    @warm_farewell
    def inference(self, path_to_data):
        """ Launch predict.py on <local_image>:opt/program/ with external payload"""
        payload = io.StringIO()
        pd.read_csv(path_to_data).to_csv(payload, index=None)
        system(f"sh {self.program_path}/src/aws/test/predict.sh {payload.getvalue()}")
        system(f"docker logs {self.model_name}_inference >> {self.build_path}/local_test/test_dir/output/logs.txt")

    
    @log_error
    def push_to_ecr(self, tag):
        """ Push image to ECR """
        system(f"sh {self.program_path}/src/aws/push.sh -b {self.build_dir} -n {self.model_name} -t {tag}")

    @not_implemented
    def mantain(self):
        """ T.B.D. will allow testing production model performance and fast retraining """
        system(f"sh {self.program_path}/src/aws/test/train_local.sh")

    @warm_farewell
    def clear_all_images(self):
        """ Clear all images from local docker """
        system(f"docker image rm -f $(docker image ls)")
    
    @warm_farewell
    def prune_docker(self):
        """ Prune local docker system """
        p = popen(f"docker system prune", "w")
        p.write("y\n")

    @warm_farewell
    def stop_containers(self):
        """ Stop running containers """
        system("docker container stop $(docker container ls -q)")
    
##################################################################################
# Flow

if __name__=="__main__":
    system("clear")
    app = Main() 
    app.ask_model_name()
    app.ask_paths()
    while True:
        system("clear")
        app.intro()
        app.ask_usage()
        if app.usage ==  "build":
            app.build()
            continue
        if app.usage == "docker manager":
            while True:
                system("clear")
                app.intro()
                _dm = app.dm_menu()
                if _dm == "launch image":
                    app.launch_image()
                    continue
                elif _dm == "clear all images":
                    app.clear_all_images()
                    continue
                elif _dm == "prune system":
                    app.prune_docker()
                    continue
                elif _dm == "stop containers":
                    app.stop_containers()
                    continue
                elif _dm == "<- back":
                    break
                elif _dm == None:
                    continue
        if app.usage == "test":
            while True:
                system("clear")
                app.intro()
                _test = app.test_menu()
                if _test == "train":
                    app.train()
                    continue
                elif _test == "serve":
                    app.serve()
                    continue
                elif _test == "inference":
                    payload_path = app.ask_payload()
                    app.inference(payload_path)
                    continue
                elif _test == "<- back":
                    break
        if app.usage == "deploy":
            while True:
                system("clear")
                app.intro()
                _depl = app.deploy_menu()
                if _depl == 'push to ecr':
                    _tag = ask_tag()
                    app.push_to_ecr(_tag)
                    continue
                if _depl == 'training job':
                    continue
                if _depl == 'endpoint deployement':
                    continue
                if _depl == '<- back':
                    break
                
        if app.usage == "mantain":
            app.mantain()
            continue
        if app.usage == "exit":
            break
        if app.usage == None:
            continue