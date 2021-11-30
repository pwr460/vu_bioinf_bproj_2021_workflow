# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:41:38 2020

@author: xugang

"""
import argparse
import os
import time
from inference_utils import read_fasta, make_input, \
    InputReader, get_ensemble_ouput, output_results, get_fasta_files
from inference_models import test_infer_step

if __name__ == '__main__':

    #============================Parameters====================================
    parser = argparse.ArgumentParser()
    parser.add_argument("-fasta", "--fasta", help="Dataset folder")
    parser.add_argument("-pssm", "--pssmpath", help="Psiblast output folder", default="pssm/")
    parser.add_argument("-ur", "--uniref", help="uniref fasta file")
    parser.add_argument("-hhm", "--hhmpath", help="Hhblits output folder", default="hhm/")
    parser.add_argument("-uc", "--uniclust", help="Uniclust folder", default="uniclust/")
    parser.add_argument("-threads", "--numthreads", help="Number of threads", type=int, default=40)

    preparation_config = {}
    preparation_config["tmp_files_path"] = r"./tmp_files"
    preparation_config["output_path"] = r"./predictions"

    args = parser.parse_args()
    fasta_path = args.fasta
    preparation_config["num_threads"] = args.numthreads
    preparation_config["pssm_path"] = args.pssmpath
    preparation_config["uniref90_path"] = args.uniref
    preparation_config["hhm_path"] = args.hhmpath
    preparation_config["uniclust30_path"] = args.uniclust

    batch_size = 8
    #============================Parameters====================================

    #============================Preparation===================================
    start_time = time.time()
    filenames = []
    files = get_fasta_files(fasta_path)
    for file in files:
        filename = file.split('.')[0]
        fasta_content = read_fasta(os.path.join(fasta_path, file))[1]

        pssm_filename = filename + '.pssm'
        hhm_filename = filename + '.hhm'
        make_input(file, fasta_content, preparation_config)
        filenames.append(filename)
    run_time = time.time() - start_time
    print('Preparation done..., time: %3.3f' % (run_time))
    #============================Preparation===================================

    #==================================Model===================================
    start_time = time.time()
    test_reader = InputReader(data_list=filenames,
                              num_batch_size=batch_size,
                              inputs_files_path=preparation_config["tmp_files_path"])

    total_lens = 0
    for step, filenames_batch in enumerate(test_reader.dataset):
        # x (batch, max_len, 76)
        # x_mask (batch, max_len)
        filenames, x, x_mask, inputs_total_len = \
            test_reader.read_file_from_disk(filenames_batch)

        total_lens += inputs_total_len

        ss8_predictions, ss3_predictions, phipsi_predictions = \
            test_infer_step(x, x_mask)

        ss8_outputs, _ = \
            get_ensemble_ouput("SS", ss8_predictions, x_mask, inputs_total_len)

        ss3_outputs, _ = \
            get_ensemble_ouput("SS", ss3_predictions, x_mask, inputs_total_len)

        phi_outputs, psi_outputs, _ = \
            get_ensemble_ouput("PhiPsi", phipsi_predictions, x_mask, inputs_total_len)

        assert len(filenames) == len(ss8_outputs) == len(ss3_outputs) == \
               len(phi_outputs) == len(psi_outputs)

        output_results(filenames, ss8_outputs, ss3_outputs, phi_outputs, psi_outputs, preparation_config)

    run_time = time.time() - start_time
    print('Prediction done..., time: %3.3f' % (run_time))
    #==================================Model===================================


