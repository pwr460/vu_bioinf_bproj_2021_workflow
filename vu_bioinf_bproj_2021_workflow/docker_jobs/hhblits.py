import os
import time
import traceback
import logging

import util


class Hhblits:
    __config_section = None
    __singularity_service = None
    __simage = "images/hhblits.simg"

    def __init__(self, config, singularity_service):
        self.__config_section = config["hhblits"]
        self.__singularity_service = singularity_service

    def get_commands(self, config_section, dataset_location, protein_name):
        in_file_path = os.path.join(dataset_location, protein_name) + ".fasta"
        dataset_name = os.path.basename(os.path.normpath(dataset_location))
        out_file_path = os.path.join(config_section["output_folder"], dataset_name, protein_name) + ".hhr"

        return ["hhblits",
                "-i", os.path.abspath(in_file_path),
                "-o", os.path.abspath(out_file_path),
                "-n", "1",
                "-d", os.path.abspath(config_section["database"])
                ]

    def run(self, dataset_location):
        try:
            logging.info("Running docker job /'Hello World/'; image: " + self.__simage)

            dataset_proteins = [f.split('.')[0] for f in os.listdir(dataset_location) if f.endswith('.fasta')]

            logging.info("Running HHBlitz for {} proteins.".format(len(dataset_proteins)))
            for protein in dataset_proteins:
                commands = self.get_commands(self.__config_section, dataset_location, protein)
                name = "{}-{}".format(self.__config_section["container_prefix"], protein)
                self.__singularity_service.exec_container(self.__simage, commands, name)

                util.clear_temp_folders("temp/hhblits")
        except:
            print(traceback.format_exc())
