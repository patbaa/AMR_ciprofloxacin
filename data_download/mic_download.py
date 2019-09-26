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

parser.add_argument("--mic_dir", type=Path, help="Path where the separated \
                    MIC/disk diffusion datafiles will be saved", required=True)

parser.add_argument("--project_dir", type=Path, help="Path where the \
                    ciproflixacin MIC/disk diffusion datatables will be saved", 
                    required=True)

args = parser.parse_args()

################################################################################
# downloading MIC files

meta = pd.read_csv(args.meta_file, sep='\t')

print('Downloading MIC files. Might take a few minutes...')

for idx, (link, name) in enumerate(zip(meta.submitted_ftp.values, 
                                meta.sample_alias.values)):
    print(f"{'%'*50} {idx+1} / {len(meta)} {'%'*50}")
    
    mic_fname = args.mic_dir.joinpath(name + '.tsv')
    wget.download('ftp://' + link, mic_fname.as_posix(), bar=None)
    
################################################################################
# saving files

mic_df = pd.DataFrame()
for name in meta.sample_alias.values:
    mic_fname = args.mic_dir.joinpath(name + '.tsv')
    tmp = pd.read_csv(mic_fname, sep='\t')
    tmp['sample_alias'] = name
    for c in tmp.columns.tolist(): 
        if 'Unnamed' in c: tmp.pop(c)
    mic_df = mic_df.append(tmp, sort=True)

mic_df.to_csv(args.project_dir.joinpath('all_MIC.tsv'), sep='\t', index=False)


mic_df = mic_df[mic_df.antibiotic_name.str.lower() == 'ciprofloxacin']
mic_df[mic_df.measurement_units == 'mm'].to_csv(
    args.project_dir.joinpath('ciprofloxacin_zone_diameters.csv'), index=False)

mic_df[mic_df.measurement_units == 'mg/L'].to_csv(
    args.project_dir.joinpath('ciprofloxacin_MICs.csv'), index=False)

################################################################################
# we are ready

print('Finished downloading and saving all MIC metadata.')
