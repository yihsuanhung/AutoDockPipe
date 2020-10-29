#!/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7
import os
import argparse
import subprocess

def main(args):
    protein_id = args.p # ex. 3pe3

    root = "/project/GP1/chialang1220/autodock/"
    project_id = os.environ['PROJECTID']
    run_vina_script = os.path.join(root, "script", "run_vina.py")
    config_file = os.path.join(root, "protein", protein_id, protein_id + ".conf")
    ligand_groups = os.path.join(root, "drugbank", "ligands") 

    for group in [g[1] for g in os.walk(ligand_groups)][0]:
        command = f"""qsub \
        -P {project_id} \
        -q ngs48G \
        -W group_list={project_id} \
        -N AutoDock \
        -l select=1:ncpus=10 \
        -l place=pack \
        -o /project/GP1/chialang1220/autodock/output/{group}.out \
        -e /project/GP1/chialang1220/autodock/output/{group}.err \
        -m e \
        -- /home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7 {run_vina_script} \
        -f {group}\
        -c {config_file}"""

        subprocess.call(command, shell = True)


if __name__ == "__main__":
    description = "AutoDock Vina Docking Pipeline"
    epilog = "AutoDock Vina Docking Pipeline"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter, usage='%(prog)s [options]', add_help=False)
    parser.add_argument("-p", required=True, help="protein id (same as the folder name)")

    args = parser.parse_args()
    main(args)



# VERSION2
# for group in [g[1] for g in os.walk(ligand_groups)][0]:
#     group_path = os.path.join(ligand_groups, group)
#     ligands = os.listdir(group_path)


#     for l in ligands:

#         ligand = os.path.join(group_path, l)
#         out = os.path.join(root, "output", l.split(".pdbqt")[0] + "_out.pdbqt")

#         command = f"""qsub \
#         -P {project_id} \
#         -q ngs48G \
#         -W group_list={project_id} \
#         -N test \
#         -l select=1:ncpus=10 \
#         -l place=pack \
#         -o /project/GP1/chialang1220/autodock/output/{l}.out \
#         -e /project/GP1/chialang1220/autodock/output/{l}.err \
#         -m e \
#         -- /project/GP1/chialang1220/autodock/vina/autodock_vina_1_1_2_linux_x86/bin/vina \
#         --receptor /project/GP1/chialang1220/autodock/protein/{protein_pdbid}/{protein_pdbid}.pdbqt \
#         --ligand {ligand} \
#         --out {out} \
#         --center_x {str(center_x)} \
#         --center_y {str(center_y)} \
#         --center_z {str(center_z)} \
#         --size_x {str(size_x)} \
#         --size_y {str(size_y)} \
#         --size_z {str(size_z)} """

#         subprocess.call(command, shell = True)



#VERSION1
# ligands_path = os.path.join(root, "drugbank", "test")
# ligands = os.listdir(ligands_path)
# print(ligands)

# for l in ligands:
#     print(l)
    
#     command = f"""qsub \
#     -P {project_id} \
#     -q ngs48G \
#     -W group_list={project_id} \
#     -N test \
#     -l select=1:ncpus=10 \
#     -l place=pack \
#     -o /project/GP1/chialang1220/autodock/output/{l}.out \
#     -e /project/GP1/chialang1220/autodock/output/{l}.err \
#     -m e \
#     -- /project/GP1/chialang1220/autodock/vina/autodock_vina_1_1_2_linux_x86/bin/vina \
#     --receptor /project/GP1/chialang1220/autodock/protein/3pe3/3pe3.pdbqt \
#     --ligand {os.path.join(ligands_path, l)} \
#     --out {os.path.join(root, "output", l.split(".pdbqt")[0] + "_out.pdbqt")} \
#     --center_x {str(center_x)} \
#     --center_y {str(center_y)} \
#     --center_z {str(center_z)} \
#     --size_x {str(size_x)} \
#     --size_y {str(size_y)} \
#     --size_z {str(size_z)} """

#     subprocess.call(command, shell = True)
