#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# imports

import os
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

################################################################################
# parsing args

parser = argparse.ArgumentParser()

parser.add_argument("--vcf_dir", type=Path, help="Path where the VCF \
                    files are stored", required=True)

parser.add_argument("--project_dir", type=Path, help="Path where the \
                    merged VCF matrix will be saved", 
                    required=True)

args = parser.parse_args()

################################################################################
# helper function

def read_vcf(fname):
    cols = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 
            'FORMAT', 'sample']
    vcfDF = pd.read_csv(fname, names = cols, sep = '\t', comment = '#')
    vcfDF['CHROM_POS'] = vcfDF['CHROM'] + '_' + vcfDF.POS.astype(str)
    return vcfDF

################################################################################
# First find all the positions that appear in any of the VCF files

print('Checking VCF files for the positions...')
positions = []
vcf_files = [i for i in args.vcf_dir.glob('*vcf')]

for file in vcf_files:
    tmpDF = read_vcf(file)
    positions = list(set(positions + tmpDF.CHROM_POS.tolist()))

positions.sort()
print(f'{len(positions)} mutated positions were found in the samples.')
    
     
################################################################################
# Merging VCF files into a single matrix

print('Merging the VCF files into a single matrix...')
resultDF = pd.DataFrame()

for idx, file in enumerate(vcf_files): 
    print(f"{'%'*50} {idx+1} / {len(vcf_files)} {'%'*50}")
    vcfDF = read_vcf(file)
    # if there are more ALT allels, keep only the first one
    vcfDF = vcfDF.groupby('CHROM_POS').first().reset_index()
    vcfDF = vcfDF.sort_values('CHROM_POS')
    
    # if both ref and alt is a single basepair the it is an SNP
    # otherwise it is an INDEL
    mutation_type = (vcfDF.REF.apply(len) == 1) & (vcfDF.ALT.apply(len) == 1)
    mutation_type = mutation_type.replace(True, 1).replace(False, 5).astype(int)
    mutation_type = mutation_type.values
          
    # this list will be filled with 0 (reference), 1 (SNP), 5 (INDEL) values        
    sample_data = [0] * len(positions)  
    
    # indicies which the right corresponds to the left
    positions_idxs = np.searchsorted(positions, vcfDF.CHROM_POS, side='left')
    if(len(positions_idxs) != len(pd.unique(positions_idxs))): print('ERROR')
        
    # local means the actual sample, global refers to the 'positions' variable
    for local_idx, position_idx in enumerate(positions_idxs):
        sample_data[position_idx] = mutation_type[local_idx] 
        # 5 for indels, 1 for SNP, else leave it 0
     
    
    # speedup when the dataframe is long, not wide
    tmpDF = pd.DataFrame(sample_data).T 
    tmpDF.columns = positions
    tmpDF['sample_alias'] = file.stem # last col
    # apped the results to the matrix
    resultDF = resultDF.append(tmpDF)


resultDF.to_csv(args.project_dir.joinpath('SNP_matrix.tsv'), sep='\t', index=False)        
        
print('VCF merging finished.')