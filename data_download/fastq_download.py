#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# imports

import wget 
import argparse
import pandas as pd
from pathlib import Path

################################################################################
# parsing args

parser = argparse.ArgumentParser()
parser.add_argument("--meta_file", type=Path, help="Path of the provided TSV \
                    file containing the links and IDs", required=True)

parser.add_argument("--fastq_dir", type=Path, help="Path where the FASTQ \
                    files will be saved", required=True)


args = parser.parse_args()

################################################################################
# downloading FASTQ files

meta = pd.read_csv(args.meta_file, sep='\t')

print('Downloading FASTQ files. This might take a few hours...')

# we have 2 fastq files for each sample
for idx, (links, name) in enumerate(zip(meta.fastq_ftp.values, 
                                        meta.sample_alias.values)):
    print(f"{'%'*50} {idx+1} / {len(meta)} {'%'*50}")
    
    fq1_file = args.fastq_dir.joinpath(name + '_1.fastq.gz')
    fq2_file = args.fastq_dir.joinpath(name + '_2.fastq.gz')
    
    wget.download('ftp://' + links.split(';')[0], fq1_file.as_posix(), bar=None)
    wget.download('ftp://' + links.split(';')[1], fq2_file.as_posix(), bar=None)          
     
################################################################################

# we are ready

print('Finished downloading the FASTQ files.')
