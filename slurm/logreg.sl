#!/bin/bash -e
#SBATCH --job-name=LogRegGrid       # job name (shows up in the queue)
#SBATCH --time=60:00:00             # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB               # Memory
#SBATCH --cpus-per-task=20
#SBATCH --array=0-6                # Array jobs
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user=kvya817@aucklanduni.ac.nz
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80

source activate /home/kvya817/.conda/envs/ts
cd ..
python logreg_grid_binary.py $SLURM_ARRAY_TASK_ID
