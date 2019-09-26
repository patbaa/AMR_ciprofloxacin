#!/bin/sh
# you may need to set the installed python interpreter and the directories

THREADS=40 # with different number of threads bwa-mem yields in slightly different results

META_FILE=/media/patbaa/hdd1/AMR_data_avail/20190510.tsv
REFERENCE=/media/patbaa/hdd1/AMR_data_avail/reference/GCA_000743255.1_ASM74325v1_genomic.fna

FASTQ_DIR=/media/patbaa/hdd1/AMR_data_avail/FASTQs/
BAM_DIR=/media/patbaa/hdd1/AMR_data_avail/BAMs/
SAM_DIR=/media/patbaa/hdd1/AMR_data_avail/SAMs/
PILEUP_DIR=/media/patbaa/hdd1/AMR_data_avail/PILEUPs/
BCF_DIR=/media/patbaa/hdd1/AMR_data_avail/BCFs/
VCF_DIR=/media/patbaa/hdd1/AMR_data_avail/VCFs/
RESFINDER_DIR=/media/patbaa/hdd1/AMR_data_avail/RESFINDERs/
RESFINDER_DB=/home/patbaa/resfinder_db/
RESFINDER_DB_KMA=/home/patbaa/resfinder_db/KMA/
PROJECT_DIR=/media/patbaa/hdd1/AMR_data_avail/

BWA=/home/patbaa/bwa-0.7.17/bwa
SAMTOOLS=/home/patbaa/samtools-1.9/samtools
BCFTOOLS=/home/patbaa/bcftools-1.9/bcftools
RESFINDER=/home/patbaa/resfinder/resfinder.py


./vcf_generation.py --meta_file $META_FILE --fastq_dir $FASTQ_DIR --bam_dir $BAM_DIR --sam_dir $SAM_DIR --pileup_dir $PILEUP_DIR --bcf_dir $BCF_DIR --vcf_dir $VCF_DIR --bwa $BWA --samtools $SAMTOOLS --bcftools $BCFTOOLS --ref $REFERENCE --n_threads $THREADS

./process_vcfs.py --vcf_dir $VCF_DIR --project_dir $PROJECT_DIR

./resfinder_generation.py --meta_file $META_FILE --fastq_dir $FASTQ_DIR --resfinder $RESFINDER --resfinder_db $RESFINDER_DB --resfinder_db_KMA $RESFINDER_DB_KMA --resfinder_results $RESFINDER_DIR --project_dir $PROJECT_DIR