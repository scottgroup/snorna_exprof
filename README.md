# ncRNA Expression Profiling Pipeline

A Snakemake-based pipeline for ncRNA (snoRNA, tRNA, snRNA ...) expression profiling from RNA-seq data (paired-end or single-end). The pipeline performs quality control, read trimming, alignment, and quantification using CoCo.

---

## Pipeline Overview

```
FASTQ files
    │
    ├──► fastp            — Quality control & adapter trimming
    │        │
    │        └──► MultiQC report
    │
    ├──► STAR index       — Genome index generation
    ├──► STAR align       — Read alignment
    │        │
    │        └──► MultiQC report
    │
    └──► CoCo ca          — GTF annotation correction
         CoCo cc          — Read counting
         CoCo merge       — Sample merging (TPM + counts)
```

### Output files

| File | Description |
|------|-------------|
| `results/report/multiqc/qc_multiqc_report.html` | FastP QC report |
| `results/report/star/star_multiqc_report.html` | STAR alignment report |
| `results/coco_merge/samples_merged_coco_tpm.tsv` | Merged TPM expression table |
| `results/coco_merge/samples_merged_coco_count.tsv` | Merged raw count table |

---

## Requirements

- [Snakemake](https://snakemake.readthedocs.io) == 7.26.0
- [Conda](https://docs.conda.io) / [Mamba](https://mamba.readthedocs.io)
- SLURM cluster environment

All other dependencies (fastp, STAR, CoCo, MultiQC, etc.) are automatically installed via Conda environments defined in `workflow/envs/`.

---

## Installation

```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake=7.26.0
conda activate snakemake
git clone https://github.com/scottgroup/snorna_exprof.git
cd ./workflow
```

---

## Usage

```bash
./snakemake.sh -g <genome.gtf> -f <genome.fasta> -i <fastq_dir> -o <output_dir> [options]
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `-g` | Reference GTF file | ✅ |
| `-f` | Reference FASTA file | ✅ |
| `-i` | Directory containing FASTQ files | ✅ |
| `-o` | Output directory | ✅ |
| `-m` | Sequencing mode: `PE` (paired-end) or `SE` (single-end) | default: `PE` |
| `-n` | Dry-run: show rules without executing | optional |
| `-h` | Show help message | optional |

### Example

```bash
./run.sh \
  -g /data/references/genome.gtf \
  -f /data/references/genome.fasta \
  -i /data/fastq/ \
  -o /scratch/results/ \
  -m PE
```

### Dry-run (recommended before first execution)

```bash
./run.sh \
  -g /data/references/genome.gtf \
  -f /data/references/genome.fasta \
  -i /data/fastq/ \
  -o /scratch/results/ \
  -n
```

---

## Input FASTQ format

FASTQ files must follow this naming convention:

```
{sample_id}_R1.fastq.gz
{sample_id}_R2.fastq.gz   # paired-end only
```

All FASTQ files must be located in the same directory, passed with `-i`.

---

## Project Structure

```
.
├── workflow/
│   ├── run.sh                  # CLI wrapper — entry point
│   ├── Snakefile
│   ├── config/
│   │   └── resources.yaml      # Default configuration
│   ├── profile/
│   │   ├── config.yaml         # Snakemake SLURM profile
│   │   └── slurmSubmitJob.py   # SLURM job submission script
│   ├── envs/
│   │   ├── fastp.yaml
│   │   ├── star.yaml
│   │   ├── coco.yaml
│   │   ├── multiqc.yaml
│   │   └── ...
│   └── scripts/
│       ├── make_manifest.py    # Manifest generation
│       ├── manifest_utils.py   # Manifest loading utilities
│       └── cocoCount_merged.py # CoCo count merging
└── README.md
```

---

## Configuration

Default parameters are defined in `workflow/config/resources.yaml`. All values are overridden at runtime by the CLI wrapper — **you do not need to edit this file**.

SLURM parameters (memory, time limits, partitions) are configured in `workflow/profile/config.yaml`.

---

## Tested on

- Snakemake **7.26**
- SLURM cluster (Beluga / Narval — Digital Research Alliance of Canada)
