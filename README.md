# pySeqkit
Toolkit for processing sequences in FASTA/Q formats
## 1. Introduction
pySeqkit is a toolkit for processing sequences in FASTA or FASTQ formats, it is writen in python and still under development. To install it, you can  
```commandline
git clone https://github.com/FlyPythons/pySeqkit.git
```
* This toolkit has been tested in **python2.7** 
## 2. Example
pySeqkit has two sub commands(stat, split) now.
### stat-Statistics on sequence files(fastA/Q)

* for FASTA/Q files, different formatted files can be stat together

```commandline
python pySeqkit.py stat 1.fq *.fa > in.stat
```

* use '-c' to speed up the process
```commandline
python pySeqkit.py stat -c 10 1.fq *.fa > in.stat
```

* for one file contains FASTA/Q file paths
```commandline
python pySeqkit.py stat -f -c 10 in.fofn > in.stat
```

* for *NGS short reads*, you'd better turn on *'-ngs'* to avoid meaningless stat
```commandline
python pySeqkit.py stat -ngs -c 10 *.R1.fq *.R2.fq
```

### split-Split sequence files(fastA/Q)

* split by sequences number == {max number} per file  
```commandline
python pySeqkit.py split -m number -n {max number} -o split in.fa
python pySeqkit.py split -m number -n {max number} -o split in.fq
```
* split by sequences length ~= {max length} per file  
```commandline
python pySeqkit.py split -m length -n {max length} -o split in.fa
python pySeqkit.py split -m length -n {max length} -o split in.fq
```