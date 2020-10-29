#!/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7
import re
import glob
import os
import csv

root = "/project/GP1/chialang1220/autodock/"
project_id = os.environ['PROJECTID']
output_dir = os.path.join(root, "output")
result_dir = os.path.join(root, "result")

# print("[output_dir]", output_dir)
# print("[result_dir]", result_dir)

file_names = glob.glob(output_dir+'/*.pdbqt')
# print(file_names)

score = {}
for file_name in file_names:
    with open(file_name) as file:
        l_name = re.findall(".+(structures_ligand_\d+_.+pdbqt)", file_name)[0]
        score[l_name] = 0
        lines = file.readlines()
        # for line in lines:
        #     name = re.findall("REMARK.+(DB[0-9]+)", line)
        #     if len(name) != 0:
        #         name = name[0]
        #         score[name] = 0
        #         break

        result_list = []
        for line in lines:
            v_result = re.findall("(REMARK VINA RESULT:.+)", line)
            if len(v_result) != 0:
                v_result = v_result[0]
                result = re.findall(".+(-\d+.\d+).+", v_result)
                result_list.append(result)
                score[l_name] = float(result_list[0][0])

score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1])}

with open(os.path.join(result_dir, "result.csv"), 'w') as f:
    for key in score.keys():
        f.write("%s,%s\n"%(key,score[key]))

print("DONE!")