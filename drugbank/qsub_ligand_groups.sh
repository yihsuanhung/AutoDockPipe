#!/bin/bash
#PBS -P MST109178
#PBS -W group_list=MST109178 
#PBS -N l_group
#PBS -l select=1:ncpus=10
#PBS -l place=pack
#PBS -q ngs48G
#PBS -V

/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7 /project/GP1/chialang1220/autodock/drugbank/ligand_groups.py