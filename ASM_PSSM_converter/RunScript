#!/bin/bash

#SBATCH --job-name=asm-pssm-converting
#SBATCH --partition=binf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00

# SLURM_OUT=\$SLURM_SUBMIT_DIR/$1_\$SLURM_JOB_ID.out

exec_dir=/scistor/informatica/...
input_dir=/scistor/informatica/...
output_dir=/scistor/informatica/...

do_computation() {
        pwd
        python3 main.py -i $input_dir -o $output_dir -fe .pssm
}

cd $exec_dir
do_computation &
wait
