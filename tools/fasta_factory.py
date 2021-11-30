import os
from pathlib import Path
import pandas as pd

__aminoAcidCodesByAbriv = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                           'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
                           'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
                           'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}


def get_amino_acid_code_from_abrv(amino_acid_abrv):
    return __aminoAcidCodesByAbriv[amino_acid_abrv]


def generate_fasta_content_from_csv(csv_file, file_name):
    fasta_contentString = "> Amino acid {}.\n".format(file_name)
    csv_content = pd.read_csv(csv_file, header=None, usecols=[4], delimiter=',', dtype=str)
    for index, row in csv_content.iterrows():
        amino_acid = row[4]
        if amino_acid != "NO":
            fasta_contentString += get_amino_acid_code_from_abrv(amino_acid)

    return fasta_contentString


def get_csv_files(dir_path, suffix=".csv"):
    file_names = os.listdir(dir_path)
    return [file for file in file_names if file.endswith(suffix)]


datasets_folder = "./datasets/csv_files"
fasta_folder = "./datasets"

datasets_list = os.listdir(datasets_folder)
for data_set in datasets_list:
    dataset_location = datasets_folder + '/' + data_set  # os.path.join(datasetsFolder, dataSet)

    dataset_fasta_files_location = fasta_folder + '/' + data_set  # os.path.join(fastaFolder, dataSet)
    Path(dataset_fasta_files_location).mkdir(parents=True, exist_ok=True)

    dataset_csv_files = get_csv_files(dataset_location)
    for csv_file in dataset_csv_files:
        file_name_without_extension = os.path.splitext(csv_file)[0]
        fasta_filePath = dataset_fasta_files_location + '/' + file_name_without_extension + ".fasta"
        csv_filePath = dataset_location + '/' + csv_file  # os.path.join(datasetFastaFilesLocation, csvFile)

        fasta_content = generate_fasta_content_from_csv(csv_filePath, file_name_without_extension)
        fasta_file = open(fasta_filePath, "w")
        fasta_file.write(fasta_content)
        fasta_file.close()

print("done")
