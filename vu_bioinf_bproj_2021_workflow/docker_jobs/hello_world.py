import os
import traceback
import logging

import util


class HelloWorld:
    __config = None
    __singularity_service = None

    def __init__(self, config, singularity_service):
        self.__config = config
        self.__singularity_service = singularity_service

    def run(self):
        try:
            container_name = "hello_world_container"
            image = "images/hello_world.simg"
            in_file_container = os.path.abspath("input/test.txt")

            logging.info("Running docker job /'Hello World/'; image: " + image)

            commands = ["python", "/main.py", in_file_container]
            output = self.__singularity_service.exec_container(image, commands, container_name)
            print(output)

            util.move_folder_content("temp/hello_world/out", "output/hello_world")
            util.clear_temp_folders("temp/hello_world")
        except:
            print(traceback.format_exc())
