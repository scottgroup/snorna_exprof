#!/usr/bin/env python3

import argparse
import logging
import sys
import re

__author__ = "Alphonse Thiaw"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Create a GTF file base on bed file  ", formatter_class=argparse.ArgumentDefaultsHelpFormatter, prefix_chars='-', add_help=True)
    parser.add_argument("-v", "--verbose", action='store_true', default=False, help="""My doc string here""")
    parser.add_argument("-doc", "--documentation", action='store_true', default=False, help="""Print the  documentation of this tool""")
    parser.add_argument("-bed", "--bedfile", default="stdin", help="""path/to_your/bedfile""")
    parser.add_argument("-gtf", "--gtf_out", default="stdin", help="""gtf annotation output file path/name.gtf""")

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s - %(name)s : %(process)d - %(levelname)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('All information message will get logged')

    if args.bedfile == "stdin":
        BEDfile = sys.stdin
    else:
        BEDfile = args.bedfile
        logging.info("Using " + str(BEDfile) + "as input data")

    if args.gtf_out == "stdin":
        outputfile = sys.stdin
    else:
        outputfile = args.gtf_out
        logging.info("Using " + str(outputfile) + "as input data")


    if args.documentation:
        print(str(parse_arguments) + "\n" + str(parse_arguments__doc__))



    sys.stdout = open(outputfile, "w")
    with open(BEDfile, "r") as file:
        for li in file:
            source="prediction"
            biotype="snoRNA"
            gene_feat="gene"
            trans_feat="transcript"
            exon_feat="exon"
            score="."
            frame="."
            cote="\""
            space=" "
            stl="NA"
            pv=";"
            exon_num="1"
            
            li=li.rstrip("/n").split()
            seqname=li[0]; start=li[1]; end=li[2]; strand=li[5]
            gene_id=li[3]; transcript_id=li[3]+".1"; exon_id=li[3]+".1.1"
            gene_attr=[
                str("gene_id"+space+cote+gene_id+cote),
                str("gene_name"+space+cote+gene_id+cote),
                str("gene_biotype"+space+cote+biotype+cote)
            ]
            transcript_attr=gene_attr+[
                str("transcript_id"+space+cote+transcript_id+cote),
                str("transcript_name"+space+cote+transcript_id+cote),
                str("transcript_biotype"+space+cote+transcript_id+cote),
                str("transcript_support_level"+space+cote+stl+cote)
            ]
            exon_attr=transcript_attr+[
                str("exon_number"+space+cote+exon_num+cote),
                str("exon_id"+space+cote+exon_id+cote)
            ]
            gene_attr="; ".join(gene_attr)+pv 
            transcript_attr="; ".join(transcript_attr)+pv
            exon_attr="; ".join(exon_attr)+pv
            print(seqname,source,gene_feat,start,end,score,strand,frame,gene_attr, sep="\t")
            print(seqname,source,trans_feat,start,end,score,strand,frame,transcript_attr, sep="\t")
            print(seqname,source,exon_feat,start,end,score,strand,frame,exon_attr, sep="\t")
    
    sys.stdout.close()
    sys.stdout = open("/dev/stdout", "w")

