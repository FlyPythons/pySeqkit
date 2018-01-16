# pySeqkit
Toolkit for processing sequences in FASTA/Q formats
## 1. Introduction
pySeqkit is a toolkit for processing sequences in FASTA or FASTQ formats, it is writen in python and still under development. To install it, you can  
```commandline
git clone https://github.com/FlyPythons/pySeqkit.git

export PATH=/your install path/pySeqkit/:$PATH
chmod 755 *
```
To run this toolkit, python 2.5 or higher is needed.
## 2. Example
* Get sequences distribution in FASTA/Q format:

for one FASTA/Q file
```commandline
fastaStat.py in.fa > in.fa.stat
fastqStat.py in.fq > in.fq.stat
```
for multi FASTA/Q files
```commandline
fastaStat.py *.fa > in.fa.stat
fastqStat.py *.fq > in.fq.stat
```
use '-c' to speed up the process
```commandline
fastaStat.py -c 10 *.fa > in.fa.stat
fastqStat.py -c 10 *.fq > in.fq.stat
```
for one file contains FASTA/Q file paths
```commandline
fastaStat.py -f in.fofn > in.fa.stat
fastqStat.py -f in.fofn > in.fq.stat
```
* Split large sequences file in FASTA/Q format into small files:

split by max number of sequences in one file
output files in 'split' directory
```commandline
fastaSplit.py -m number -n {max number} -o split in.fa
fastqStat.py -m number -n {max number} -o split in.fq
```
split by max length of sequences summed in one file
output files in 'split' directory
for multi FASTA/Q files
```commandline
fastaSplit.py -m length -n {max length} -o split in.fa
fastqStat.py -m length -n {max length} -o split in.fq
```