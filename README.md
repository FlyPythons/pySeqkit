# pySeqkit
Toolkit for processing sequences in FASTA/Q formats
## 1. Introduction
pySeqkit is a toolkit for processing sequences in FASTA or FASTQ formats, it is writen in python and still under development. To install it, you can  
```commandline
git clone https://github.com/FlyPythons/pySeqkit.git

export PATH=/your install path/pySeqkit/:$PATH
chmod 755 *.py
```
* This toolkit has been tested in **python2.7** and **python3.5**
* To test the toolkit, you can
```commandline
cd test
python test.py
```
if the error is raised, install is ok.
## 2. Example
* Get sequences distribution in FASTA/Q format:

for one FASTA/Q file
```commandline
fastaStat.py in.fa > in.fa.stat
fastqStat.py in.fq > in.fq.stat
```
for multi FASTA/Q files
```commandline
fastaStat.py 1.fa 2.fa *.fa > in.fa.stat
fastqStat.py 1.fq 2.fq *.fq > in.fq.stat
```
use '-c' to speed up the process
```commandline
fastaStat.py -c 10 1.fa 2.fa *.fa > in.fa.stat
fastqStat.py -c 10 1.fq 2.fq *.fq > in.fq.stat
```
for one file contains FASTA/Q file paths
```commandline
fastaStat.py -f in.fofn > in.fa.stat
fastqStat.py -f in.fofn > in.fq.stat
```
* Split large sequences file in FASTA/Q format into small files:

split by sequences number == {max number} per file  
output files in 'split' directory
```commandline
fastaSplit.py -m number -n {max number} -o split in.fa
fastqStat.py -m number -n {max number} -o split in.fq
```
split by sequences length ~= {max length} per file  
output files in 'split' directory
for multi FASTA/Q files
```commandline
fastaSplit.py -m length -n {max length} -o split in.fa
fastqStat.py -m length -n {max length} -o split in.fq
```