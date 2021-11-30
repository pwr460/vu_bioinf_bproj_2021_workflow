### PIPELINE BASH

#!/bin/bash

#SBATCH --job-name=
#SBATCH --partition=binf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=

# SLURM_OUT=$SLURM_SUBMITDIR/$1$SLURM_JOB_ID.out

# load conda environment
# module load conda

super_dir=/scistor/informatica/...
dataset=...

source /cm/shared/package/miniconda3/etc/profile.d/conda.sh
conda activate base

cd /scistor/informatica/.../vu_bioinf_bproj_2021_workflow

source ./venv/bin/activate

# execute script
do_computation() {
        pwd
    python3 program.py -dsf $super_dir -ds [$dataset]
}

do_computation &
wait
