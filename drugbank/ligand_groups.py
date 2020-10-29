#!/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7

import os
import math

root = "/project/GP1/chialang1220/autodock/"
ligands_dir = os.path.join(root, "drugbank", "ligands")
# total_ligands = len(os.listdir(ligands_dir))
total_ligands = len([x[2] for x in os.walk(ligands_dir)][0])
total_dirs = math.ceil(total_ligands / 100)
ligands = [x[2] for x in os.walk(ligands_dir)][0]
ligands_path = [os.path.join(ligands_dir, l) for l in ligands]

print("[ligands_dir]\t",ligands_dir)
print("[total_ligands]\t",total_ligands)
print("[total_dirs]\t",total_dirs)
print("[ligands]\t", ligands[0])
print("[ligands_path]\t", ligands_path[0])

# make dirs
for i in range(total_dirs):
    if not os.path.exists(os.path.join(ligands_dir, "ligands" + "_" + str(i))):
        os.makedirs(os.path.join(ligands_dir, "ligands" + "_" + str(i)))

separation_dirs = [x[1] for x in os.walk(ligands_dir)][0]
# print(len(separation_dirs))


for d in separation_dirs:
    full_d = os.path.join(ligands_dir, d)
    for _ in range(100):
        ligands = [x[2] for x in os.walk(ligands_dir)][0]
        ligands_path = [os.path.join(ligands_dir, l) for l in ligands]
        if len(ligands_path) != 0:
            os.rename(ligands_path[0], os.path.join(full_d,ligands[0]))