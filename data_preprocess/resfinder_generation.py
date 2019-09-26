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

parser.add_argument("--resfinder_db", type=Path, help="Path where the \
                    resfinder database is located", required=True)

parser.add_argument("--resfinder_db_KMA", type=Path, help="Path where the \
                    resfinder KMA database is located", required=True)

parser.add_argument("--resfinder_results", type=Path, help="Path where the \
                    resfinder results will be stored", required=True)

parser.add_argument("--resfinder", type=Path, help="Resfinder executable", 
                    required=True)

parser.add_argument("--project_dir", type=Path, help="Path where the \
                    resfinder processed datatable will be saved", 
                    required=True)


args = parser.parse_args()

resfinder = args.resfinder.as_posix()
resfinder_db = args.resfinder_db.as_posix()
resfinder_db_KMA = args.resfinder_db_KMA.as_posix()

################################################################################
# Running resfinder

meta = pd.read_csv(args.meta_file, sep='\t')

print('Running resfinder')

anibio_types = ('aminoglycoside,beta-lactam,colistin,fosfomycin,fusidicacid,'
                'glycopeptide,macrolide,nitroimidazole,oxazolidinone,phenicol,'
                'quinolone,rifampicin,sulphonamide,tetracycline,trimethoprim')

for idx, name in enumerate(meta.sample_alias.values):
    # running resfinder for all samples
    print(f"{'%'*50} {idx+1} / {len(meta)} {'%'*50}")
    fq1 = args.fastq_dir.joinpath(name + '_1.fastq.gz').as_posix()
    fq2 = args.fastq_dir.joinpath(name + '_2.fastq.gz').as_posix()
    resultdir = args.resfinder_results.joinpath(name)
    resultdir.mkdir(parents=True, exist_ok=True)
    resultdir = resultdir.as_posix()
    
    os.system((f'{resfinder} --fastq1 {fq1} --fastq2 {fq2} -o {resultdir} '
               f'-p {resfinder_db} -d {anibio_types} -t 90.00 -l 0.60 '
               f'-q {resfinder_db_KMA}'))
    
    
    
print('Finished resfinder')    
################################################################################
# Post-processing results: merging the antibiotic-level files to sample-level

print('Running results post processing')

all_res_genes = []

for name in meta.sample_alias.values:
    # concatenating the results into one file for each sample
    resgenesDF = pd.DataFrame()
    
    resultdir = args.resfinder_results.joinpath(name)
    results = [i.as_posix() for i in resultdir.glob('*res')]
    for fname in results:
        resgenesDF = resgenesDF.append(pd.read_csv(fname, sep='\t'))
    
    # saving all genes that appears in our data
    all_res_genes = all_res_genes + resgenesDF['#Template'].tolist()
    resgenesDF.to_csv(resultdir.joinpath('summary.tsv'), sep='\t', index=False)

    
all_res_genes = list(set(all_res_genes))  
all_res_genes.sort()

print(f'We found {len(all_res_genes)} different entries in the resfinder '
       'database, that appeared at least in one of our samples')

################################################################################
# Post-processing results: merging the sample-level files into one single table

resultDF = pd.DataFrame()
for name in meta.sample_alias.values:
    # creating a single file from all samples
    resultdir = args.resfinder_results.joinpath(name)
    tmp = pd.read_csv(resultdir.joinpath('summary.tsv'), sep='\t')
    sample_resfinderDF = pd.DataFrame({'sample_alias': [name]})

    for g in all_res_genes:
        # 1 if that resistant gene appears, 0 else
        sample_resfinderDF[g] = int(g in tmp['#Template'].tolist())
        
    resultDF = resultDF.append(sample_resfinderDF)
    
resultDF.to_csv(args.project_dir.joinpath('resfinder_results.csv'), index=False)

print('Finished results post processing')

