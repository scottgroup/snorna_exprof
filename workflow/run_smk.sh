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
    echo "  -m   Mode de séquençage : PE ou SE         [défaut: PE]"
    echo "  -t   Nombre de cores                       [défaut: 4]"
    echo "  -n   Dry-run : affiche les règles sans exécuter"
    echo "  -h   Afficher cette aide"
    echo ""
    exit 1
}

# -------------------
# Default parameters
# -------------------
MODE="PE"
THREADS=4
DRY_RUN=""

# ------------------
# Argument parsing
# ------------------
while getopts "g:f:i:o:m:t:nh" opt; do
    case $opt in
        g) GTF="$OPTARG" ;;
        f) FASTA="$OPTARG" ;;
        i) FASTQ_DIR="$OPTARG" ;;
        o) OUTPUT_DIR="$OPTARG" ;;
        m) MODE="$OPTARG" ;;
        t) THREADS="$OPTARG" ;;
        n) DRY_RUN="--dry-run" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# ------------------
# Argument checking
# ------------------
[[ -z "${GTF:-}"        ]] && echo "[ERREUR] -g (gtf) est obligatoire"        && usage
[[ -z "${FASTA:-}"      ]] && echo "[ERREUR] -f (fasta) est obligatoire"      && usage
[[ -z "${FASTQ_DIR:-}"  ]] && echo "[ERREUR] -i (fastq_dir) est obligatoire"  && usage
[[ -z "${OUTPUT_DIR:-}" ]] && echo "[ERREUR] -o (output_dir) est obligatoire" && usage

[[ ! -f "$GTF"       ]] && echo "[ERREUR] GTF introuvable : $GTF"                 && exit 1
[[ ! -f "$FASTA"     ]] && echo "[ERREUR] FASTA introuvable : $FASTA"             && exit 1
[[ ! -d "$FASTQ_DIR" ]] && echo "[ERREUR] Dossier FASTQ introuvable : $FASTQ_DIR" && exit 1

[[ "$MODE" != "PE" && "$MODE" != "SE" ]] && \
    echo "[ERREUR] Mode invalide : $MODE (PE ou SE)" && exit 1


# =======
# STEP 1 : Download Coco if missing
# =======
COCO_DIR="../tempdir/tools/coco"

if [[ -d "$COCO_DIR" ]]; then
    echo "[INFO] CoCo already exist : $COCO_DIR"
else
    echo "[INFO] Downloads CoCo..."
    mkdir -p "${OUTPUT_DIR}/tools"
    git clone "https://github.com/scottgroup/coco.git" "$COCO_DIR"
    echo "[INFO] CoCo installed : $COCO_DIR"
fi

# =======
# STEP 2 : Generate manifest
# =======
MANIFEST_DIR="${OUTPUT_DIR}/data"
MANIFEST_FILE="${MANIFEST_DIR}/manifest.tsv"
mkdir -p "$MANIFEST_DIR"

echo "[INFO] Generate manifest ($MODE)..."
python3 "$SCRIPT_DIR/scripts/make_manifest.py" \
    -i "$FASTQ_DIR" \
    -o "$MANIFEST_FILE" \
    -m "$MODE"
echo "[INFO] Manifest generated : $MANIFEST_FILE"

# =======
# STEP 3 : Lancer Snakemake
# =======
echo "[INFO] Run pipeline (cores: $THREADS)..."
snakemake --profile "$SCRIPT_DIR/profile/" --config gtf="$GTF" fasta="$FASTA" fastq_dir="$FASTQ_DIR" output_dir="$OUTPUT_DIR" manifest="$MANIFEST_FILE" $DRY_RUN

