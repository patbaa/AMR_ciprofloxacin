#!/bin/sh
# you may need to set the installed python interpreter and the directories

META_FILE=/media/patbaa/hdd1/AMR_data_avail/20190510.tsv
PROJECT_DIR=/media/patbaa/hdd1/AMR_data_avail/
MIC_DIR=/media/patbaa/hdd1/AMR_data_avail/MICs/
FASTQ_DIR=/media/patbaa/hdd1/AMR_data_avail/FASTQs/

./mic_download.py     --meta_file $META_FILE --mic_dir $MIC_DIR --project_dir $PROJECT_DIR
./fastq_download.py   --meta_file $META_FILE --fastq_dir $FASTQ_DIR
./check_downloads.py  --meta_file $META_FILE --fastq_dir $FASTQ_DIR --mic_dir $MIC_DIR