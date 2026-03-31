#!/usr/bin/env python3

import os
import glob
import argparse

def find_samples_pe(fq_dir):
    r1_files = glob.glob(os.path.join(fq_dir, "*_R1.fastq.gz"))
    samples = {}
    for r1 in r1_files:
        base = os.path.basename(r1)
        sample_id = base.replace("_R1.fastq.gz", "")
        r2 = os.path.join(fq_dir, f"{sample_id}_R2.fastq.gz")
        if os.path.exists(r2):
            samples[sample_id] = (r1, r2)
        else:
            print(f"[WARNING] R2 file missing for sample: {sample_id}")
    return samples

def find_samples_se(fq_dir):
    r1_files = glob.glob(os.path.join(fq_dir, "*_R1.fastq.gz"))
    samples = {os.path.basename(f).replace("_R1.fastq.gz", ""): f for f in r1_files}
    return samples

def write_manifest(samples, output_path, mode):
    with open(output_path, "w") as out:
        for sample_id in sorted(samples):
            if mode == "PE":
                r1, r2 = samples[sample_id]
                out.write(f"{sample_id}\t{r1}\t{r2}\n")
            else:  # SE
                r1 = samples[sample_id]
                out.write(f"{sample_id}\t{r1}\n")
    print(f"[INFO] Manifest written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate manifest.tsv for FASTQ files.")
    parser.add_argument("-i", "--input", required=True, help="Input folder containing FASTQ files.")
    parser.add_argument("-o", "--output", default="manifest.tsv", help="Output manifest file path.")
    parser.add_argument("-m", "--mode", choices=["PE", "SE"], default="PE", help="Sequencing mode: PE (paired-end) or SE (single-end).")
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        raise NotADirectoryError(f"{args.input} is not a valid directory.")

    if args.mode == "PE":
        samples = find_samples_pe(args.input)
    else:
        samples = find_samples_se(args.input)

    if not samples:
        raise RuntimeError("No valid samples found.")
    
    write_manifest(samples, args.output, args.mode)

if __name__ == "__main__":
    main()

