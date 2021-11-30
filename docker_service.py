import tarfile
import io
import ntpath
import time
#import docker
import re
import logging


def get_file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class DockerService:
    client = None

    def __init__(self, waiting_interval=10):
        #self.client = docker.from_env()
        self.waiting_interval = waiting_interval

    def get_container_status(self, container_name):
        return self.client.containers.get(container_name).status

    # by remove every container
    def remove_containers(self, matching_regex=".*"):
        logging.info("Removing containers matching regex " + matching_regex)
        containers = self.client.containers.list(all=True)
        containers_to_close = list(filter(lambda x: re.search(matching_regex, x.name), containers))
        logging.info("Found {} containers to close".format(len(containers_to_close)))
        for container in containers_to_close:
            container.remove(v=True)

    def run_container(self, image, commands, name=None, volumes=None, wait=True):
        if name is not None:
            logging.info("Starting container {} using image {}".format(name, image))
        else:
            logging.info("Starting container using image {}".format(image))

        container = self.client.containers.run(image, commands, name=name, volumes=volumes, detach=True)
        if wait:
            self.wait_for_container_to_finish(container)
        return container

    def wait_for_container_to_finish(self, container):
        logging.info("Waiting for container {} (id: {})".format(container.name, container.id))
        container_status = self.client.containers.get(container.id).status
        while container_status == 'created' or container_status == 'running':
            time.sleep(self.waiting_interval)
            container_status = self.client.containers.get(container.id).status

    def read_container_archive(self, container, container_file_path):
        logging.info(
            "Reading archive {} from container {} (id: {})".format(container_file_path, container.name, container.id))
        tar_stream, stat = container.get_archive(container_file_path)
        file_obj = io.BytesIO()
        for i in tar_stream:
            file_obj.write(i)
        file_obj.seek(0)
        tar = tarfile.open(mode='r', fileobj=file_obj)
        file_name = get_file_name(container_file_path)
        text = tar.extractfile(file_name)
        return text.read()

    def transfer_container_archive(self, container, archive_path_container, local_transfer_path):
        container_archive_content = self.read_container_archive(container, archive_path_container)
        logging.info("Saving container archive as {}".format(local_transfer_path))
        out_file = open(local_transfer_path, "w")
        out_file.write(container_archive_content.decode("utf-8"))
        out_file.close()
