#!/usr/bin/bash


# Use scratch as temp dir

export TMPDIR=/lustre07/scratch/abthiaw/tempdir/tmp
export XDG_CACHE_HOME=/lustre07/scratch/abthiaw/tempdir/.cache
export CONDA_PKGS_DIRS=/lustre07/scratch/abthiaw/tempdir/.conda/pkgs
export CONDA_ENVS_PATH=/lustre07/scratch/abthiaw/tempdir/.conda/envs

mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$CONDA_PKGS_DIRS" "$CONDA_ENVS_PATH"



# Run snakemake

snakemake --profile profile/
