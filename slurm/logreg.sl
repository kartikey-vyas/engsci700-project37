#!/bin/bash -e
#SBATCH --job-name=LogRegGrid       # job name (shows up in the queue)
#SBATCH --time=60:00:00             # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB               # Memory
#SBATCH --cpus-per-task=18
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err

source activate /home/kvya817/.conda/envs/ts
cd ..
python logreg_grid.py
