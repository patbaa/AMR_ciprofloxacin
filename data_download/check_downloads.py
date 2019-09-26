#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# imports

import hashlib
import argparse
import pandas as pd
from pathlib import Path

################################################################################
# parsing args

parser = argparse.ArgumentParser()
parser.add_argument("--meta_file", type=Path, help="Path of the provided TSV \
                    file containing the links and IDs", required=True)

parser.add_argument("--mic_dir", type=Path, help="Path where the separated \
                    MIC/disk diffusion datafiles will be saved", required=True)

parser.add_argument("--fastq_dir", type=Path, help="Path where the \
                    ciproflixacin MIC/disk diffusion datatables will be saved", 
                    required=True)

args = parser.parse_args()

################################################################################
# helper funcs

def md5sum(file):
    with open(file, 'rb') as f:
        data = f.read()
        md5hash = hashlib.md5(data).hexdigest()
    return md5hash

################################################################################
# loading meta

meta = pd.read_csv(args.meta_file, sep='\t')
print('''Verification of the MD5SUMs for the downloaded files, 
Mismatches will be printed. If everything is OK, nothing will be printed.''')

################################################################################
# MIC files
md5 = []
print('Checking MIC files...')
for name, server_hash in zip(meta.sample_alias.values, 
                             meta.submitted_md5.values):
    mic_fname = args.mic_dir.joinpath(name + '.tsv')  
    local_hash = md5sum(mic_fname.as_posix())
    
    if server_hash != local_hash:
        print('MIC file for ', name, ' is corrupted.')
        print(server_hash, local_hash)

################################################################################
# FASTQ files

print('Checking FASTQ files...')#

for idx, (name, server_hash) in enumerate(zip(meta.sample_alias.values, 
                                              meta.fastq_md5.values)):
    print(f"{'%'*50} {idx+1} / {len(meta)} {'%'*50}")
    
    fq1_fname = args.fastq_dir.joinpath(name + '_1.fastq.gz')
    fq2_fname = args.fastq_dir.joinpath(name + '_2.fastq.gz')
    
    server_hash_fq1 = server_hash.split(';')[0]
    server_hash_fq2 = server_hash.split(';')[1]
    
    local_hash_fq1 = md5sum(fq1_fname.as_posix())
    local_hash_fq2 = md5sum(fq2_fname.as_posix())
    
    if server_hash_fq1 != local_hash_fq1:
        print('FASTQ_1 file for ', name, ' is corrupted.')
        print(server_hash_fq1, local_hash_fq1)
    
    if server_hash_fq2 != local_hash_fq2:
        print('FASTQ_2 file for ', name, ' is corrupted.')
        print(server_hash_fq2, local_hash_fq2)

################################################################################
# we are ready

print('Data download & checking is ready.')
