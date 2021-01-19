# AMR_ciprofloxacin
Code sharing for the ciprofloxacin prediction research 

Understanding and predicting ciprofloxacin minimum inhibitory concentration in Escherichia coli with machine learning
Published paper: https://www.nature.com/articles/s41598-020-71693-5

Used reference genome: 

``` bash
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/743/255/GCA_000743255.1_ASM74325v1/GCA_000743255.1_ASM74325v1_genomic.fna.gz
```

Running the whole project requires ~ 3 TB storage and a machine with 64 GB RAM.

Code and data downloading details

1. run data_download/wrapper_download.sh
 - also set the bash variables in that file according to your local folder system (folders must exist)
 - this script will download the MIC metadata, the FASTQ files and check the md5sum of the downloaded files
 
2. run data_preprocess/wrapper_preprocess.sh
 - also set the bash variables in that file according to your local folder system (folders must exist)
 - this script will generate VCF files and an SNP matric from the samples and run the resfinder on the samples
 
3. run the jupyter notebooks in the machine_learning_and_stats folder

Version:
 - python 3.6.5
 - samtools 1.9
 - bcftools 1.9
 - bwa 0.7.17
 - resfinder 3.1.0
 - KMA 1.1.4
 
Python package versions can be found in the requirements.txt file. 
