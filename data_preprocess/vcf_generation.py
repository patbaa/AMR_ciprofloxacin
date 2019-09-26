#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# imports

import os
import argparse
import pandas as pd
from pathlib import Path

################################################################################
# parsing args

parser = argparse.ArgumentParser()
parser.add_argument("--meta_file", type=Path, help="Path of the provided TSV \
                    file containing the links and IDs", required=True)

parser.add_argument("--fastq_dir", type=Path, help="Path where the FASTQ \
                    files are", required=True)

parser.add_argument("--sam_dir", type=Path, help="Path where the SAM \
                    files will be saved", required=True)

parser.add_argument("--bam_dir", type=Path, help="Path where the BAM \
                    files will be saved", required=True)

parser.add_argument("--pileup_dir", type=Path, help="Path where the pileup \
                    files will be saved", required=True)

parser.add_argument("--bcf_dir", type=Path, help="Path where the BCF \
                    files will be saved", required=True)

parser.add_argument("--vcf_dir", type=Path, help="Path where the VCF \
                    files will be saved", required=True)

parser.add_argument("--ref", type=Path, help="Reference genome file", 
                    required=True)

parser.add_argument("--bwa", type=Path, help="BWA executable", 
                    required=True)

parser.add_argument("--samtools", type=Path, help="Samtools executable", 
                    required=True)

parser.add_argument("--bcftools", type=Path, help="Bcftools executable", 
                    required=True)

parser.add_argument("--n_threads", type=int, help="Number of CPU threads", 
                    required=True)


args = parser.parse_args()

bwa = args.bwa.as_posix()
ref = args.ref.as_posix()
samtools = args.samtools.as_posix()
bcftools = args.bcftools.as_posix()

################################################################################
# Indexing reference file

print('Indexing the reference genome')
os.system(f'{bwa} index -a bwtsw {ref}')
os.system(f'{samtools} faidx {ref}') 
     
################################################################################
# Generating VCF files

meta = pd.read_csv(args.meta_file, sep='\t')

print('Generating VCF files...')

for idx, name in enumerate(meta.sample_alias.values):
    print(f"{'%'*50} {idx+1} / {len(meta)} {'%'*50}")
    
    # setting up proper filenames
    fq1 = args.fastq_dir.joinpath(name + '_1.fastq.gz').as_posix()
    fq2 = args.fastq_dir.joinpath(name + '_2.fastq.gz').as_posix()
    samfile = args.sam_dir.joinpath(name + '.sam').as_posix()
    bamfile = args.bam_dir.joinpath(name + '.bam').as_posix()
    sortedbamfile = args.bam_dir.joinpath(name + '_sorted.bam').as_posix()
    pileupfile = args.pileup_dir.joinpath(name + '.pileup').as_posix()
    bcffile = args.bcf_dir.joinpath(name + '.raw.bcf').as_posix()
    vcffile = args.vcf_dir.joinpath(name + '.vcf').as_posix()
    
    # mapping & variant calling
    os.system(f'{bwa} mem -t {args.n_threads} {ref} {fq1} {fq2} > {samfile}')
    os.system(f'{samtools} view -@ {args.n_threads} -Sb {samfile} > {bamfile}')
    os.system(f'{samtools} sort -@ {args.n_threads} {bamfile} -o {sortedbamfile}')
    os.system(f'{samtools} index -@ {args.n_threads} {sortedbamfile}')
    
    os.system((f'{bcftools} mpileup --min-MQ 50 --threads {args.n_threads} '
               f'-O u --fasta-ref {ref} {sortedbamfile} -o {pileupfile}'))    
    os.system(f'{bcftools} call --ploidy 1 -mv -Ob {pileupfile} -o {bcffile}')
    
    os.system(f'{bcftools} index -f {bcffile}')
    os.system(f"{bcftools} view -i '%QUAL>=50 & DP>=20' {bcffile} -o {vcffile}")
    
print('VCF generation finished.')