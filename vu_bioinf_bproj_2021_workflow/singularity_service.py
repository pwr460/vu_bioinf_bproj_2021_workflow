import logging
import ntpath
import util

from spython.main import Client


def get_file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class SingularityService:
    __client = None
    __container_options = None

    def __init__(self, container_wd):
        self.__client = Client

        container_wd_full_path = util.get_folder_full_path(container_wd)
        self.__container_options = ["--pwd", container_wd_full_path]

    def exec_container(self, image, commands, name=None):
        if name is not None:
            logging.info("Starting container {} using image {}".format(name, image))
        else:
            logging.info("Starting container using image {}".format(image))

        container = self.__client.instance(image, name=name)
        output = self.__client.execute(container, commands, options=self.__container_options)
        logging.info(output)
        print(output)

        container_err_logs = container.error_logs()
        if container_err_logs:
            logging.error("Error logs of container {}: {}".format(name, container_err_logs))

        container.stop()
        return output
