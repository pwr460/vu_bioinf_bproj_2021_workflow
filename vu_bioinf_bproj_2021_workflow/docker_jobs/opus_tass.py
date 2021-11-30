import os
import traceback
import logging

import util


class OpusTass:
    __config = None
    __singularity_service = None
    __simage = "images/opus_tass.simg"
    __simage_train = "images/opus_tass_train.simg"

    def __init__(self, config, singularity_service):
        self.__config = config
        self.__singularity_service = singularity_service

    def run(self, dataset):
        try:
            config_section = self.__config["opus_tass"]
            container_name = config_section["container_name"]

            commands = self.__get_command(config_section, dataset)
            output = self.__singularity_service.exec_container(self.__simage, commands, container_name)
            print(output)

            local_out_folder = os.path.join(config_section["output_folder"], dataset)
            util.move_folder_content("temp/opus_tass/predictions", local_out_folder)
            util.clear_temp_folders("temp/opus_tass")
        except:
            print(traceback.format_exc())

    def __get_command(self, config_section, dataset):
        return ["python", "/inference.py",
                "-pb", os.path.join(config_section["psi_blast_folder"], dataset),
                "-hhb", os.path.join(config_section["hhblits_folder"], dataset),
                "-uc", config_section["uniclust_folder"],
                "-ur", config_section["unire_location"],
                "-threads", config_section["num_threads"],
                ]

    def train(self):
        try:
            config_section = self.__config["opus_tass"]["training"]
            container_name = config_section["container_name"]
            logging.info("Running docker job /'OPUS TASS train models/'; image: " + self.__simage_train)

            commands = self.__get_training_command(config_section)
            out = self.__singularity_service.exec_container(self.__simage_train, commands, container_name)
            print(out)

            util.move_folder_content("temp/opus_tass/models", "models")
            util.clear_temp_folders("temp/opus_tass")
        except:
            print(traceback.format_exc())

    def __get_training_command(self, training_config_section):
        train_folder = util.get_folder_full_path(
            training_config_section["train_input_folder"]
        )

        return ["python", "/train.py",
                "-train", os.path.join(train_folder, training_config_section["train_list"]),
                "-val", os.path.join(train_folder, training_config_section["val_list"]),
                "-test", os.path.join(train_folder, training_config_section["test_list"]),
                "-in", os.path.join(train_folder, training_config_section["inputs_folder"]),
                "-labels", os.path.join(train_folder, training_config_section["labels_folder"])
                ]
