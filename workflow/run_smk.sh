#!/usr/bin/bash

set -euo pipefail

#===========================================
# CLI Wrapper snoRNA Expression profiling
# ==========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


usage() {
    echo ""
    echo "Usage: $0 -g <genome.gtf> -f <annotation.fasta> -i <fastq_dir> -o <output_dir> [options]"
    echo ""
    echo "Arguments obligatoires:"
    echo "  -g   Fichier GTF de référence"
    echo "  -f   Fichier FASTA de référence"
    echo "  -i   Répertoire contenant les fichiers FASTQ"
    echo "  -o   Répertoire de sortie"
    echo ""
    echo "Options:"
    echo "  -m   Mode de séquençage : PE (paired-end) ou SE (single-end)  [défaut: PE]"
    echo "  -n   Dry-run : affiche les règles sans exécuter"
    echo "  -h   Afficher cette aide"
    echo ""
    exit 1
}

#-------------------
# Default parameters
#-------------------

MODE="PE"
DRY_RUN=""

#------------------
# Argument parsing
# -----------------

while getopts "g:f:i:o:m:nh" opt; do
    case $opt in
        g) GTF="$OPTARG" ;;
        f) FASTA="$OPTARG" ;;
        i) FASTQ_DIR="$OPTARG" ;;
        o) OUTPUT_DIR="$OPTARG" ;;
        m) MODE="$OPTARG" ;;
        n) DRY_RUN="--dry-run" ;;
        h) usage ;;
        *) usage ;;
    esac
done

#------------------
# Argument checking
# -----------------

[[ -z "${GTF:-}"        ]] && echo "[ERREUR] -g (gtf) est obligatoire"       && usage
[[ -z "${FASTA:-}"      ]] && echo "[ERREUR] -f (fasta) est obligatoire"     && usage
[[ -z "${FASTQ_DIR:-}"  ]] && echo "[ERREUR] -i (fastq_dir) est obligatoire" && usage
[[ -z "${OUTPUT_DIR:-}" ]] && echo "[ERREUR] -o (output_dir) est obligatoire" && usage

[[ ! -f "$GTF"       ]] && echo "[ERREUR] GTF introuvable : $GTF"                  && exit 1
[[ ! -f "$FASTA"     ]] && echo "[ERREUR] FASTA introuvable : $FASTA"              && exit 1
[[ ! -d "$FASTQ_DIR" ]] && echo "[ERREUR] Dossier FASTQ introuvable : $FASTQ_DIR"  && exit 1

[[ "$MODE" != "PE" && "$MODE" != "SE" ]] && echo "[ERREUR] Mode invalide : $MODE (PE ou SE)" && exit 1

# ------------------
# Résolution des chemins absolus
# ------------------


#=======
# STEP1: GENERATE MANIFEST
#=======

MANIFEST_PATH="${OUTPUT_DIR}/data"
mkdir -p "$MANIFEST_PATH"
MANIFEST_FILE="$MANIFEST_PATH/manifest.tsv"


echo "[INFO] Generate manifest ($MODE)..."
python3 "$SCRIPT_DIR/scripts/make_manifest.py" \
    -i "$FASTQ_DIR" \
    -o "$MANIFEST_FILE" \
    -m "$MODE"

echo "[INFO] Manifest is generated : $MANIFEST_PATH"

#=======
# STEP2: RUN SNAKEMAKE
#=======
echo "[INFO] Run the pipeline (profil SLURM)..."
snakemake \
    --profile "$SCRIPT_DIR/profile/" \
    --config \
        gtf="$GTF" \
	fasta="$FASTA" \
	fastq_dir="$FASTQ_DIR" \
	output_dir="$OUTPUT_DIR" \
	manifest="$MANIFEST_FILE" \
    $DRY_RUN
