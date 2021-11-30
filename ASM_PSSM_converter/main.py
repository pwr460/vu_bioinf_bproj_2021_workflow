import argparse
import csv
import os

import asm_reader

asm_amino_acid_prediction_order = [
    '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
    'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', 'U', '*',
    'O', 'J']
pssm_amino_acid_prediction_order = [
    'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'K', 'L', 'M',
    'F', 'P', 'S', 'T', 'W', 'Y', 'V']

pssm_headers = ['P', 'Query'] + pssm_amino_acid_prediction_order


def create_pssm(file_path, out_dir):
    asm_scores = asm_reader.get_final_scores(file_path)

    ordered_scores = []
    prediction_column_num = 0
    score_predictions = {}
    for score in asm_scores:
        predicted_amino_acid = asm_amino_acid_prediction_order[prediction_column_num]
        score_predictions[predicted_amino_acid] = score

        if prediction_column_num == 27:
            ordered_scores.append(score_predictions)
            score_predictions = {}
            prediction_column_num = 0
        else:
            prediction_column_num += 1

    pssm_content = [pssm_headers]
    for amino_acid in ordered_scores:
        position = len(pssm_content)
        query = '[not implemented]'
        prediction_scores = []
        for predicted_amino_acid in pssm_amino_acid_prediction_order:
            prediction_scores.append(amino_acid[predicted_amino_acid])
        pssm_content.append([position, query] + prediction_scores)

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    out_file = out_dir + '/' + file_name + '.pssm'
    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(pssm_content)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indir", help="Directory containing ASM.1 formatted files to convert.")
parser.add_argument("-o", "--outdir", help="Output directory for the correctly formatted PSSM files.")
parser.add_argument("-fe", "--fileextenstion", help="File extension of the ASM.1 files", default='.pssm')

args = parser.parse_args()
in_dir = os.path.abspath(args.indir)
out_dir = os.path.abspath(args.outdir)
in_file_extension = args.fileextenstion

print("Input directory: {}".format(in_dir))
print("Output directory: {}".format(out_dir))
print("Converting files with extenstion {}".format(in_file_extension))

file_count = 0
for file in os.listdir(in_dir):
    if file.endswith(in_file_extension):
        file_count += 1
        create_pssm(in_dir + '/' + file, out_dir)

print("Done")
print("Converted {} files.".format(file_count))


