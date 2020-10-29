#!/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7
import os
import argparse
import subprocess

def main(args):
    folder_input = args.f # ex.ligands_0
    config = args.c # ex. /project/GP1/chialang1220/autodock/protein/3pe3/3pe3.conf
    # protein_id = args.p # ex.3pe3
    # center_x = args.cx 
    # center_y = args.cy 
    # center_z = args.cz 
    # size_x = args.sx 
    # size_y = args.sy 
    # size_z = args.sz 

    root = "/project/GP1/chialang1220/autodock/"
    folder_path = os.path.join(root, "drugbank", "ligands", folder_input)
    ligands = os.listdir(folder_path)
    
    for l in ligands:
        l_path = os.path.join(folder_path, l)
        out_path = os.path.join(root, "output", l.split(".pdbqt")[0] + "_out.pdbqt")
        command = f"""/project/GP1/chialang1220/autodock/vina/autodock_vina_1_1_2_linux_x86/bin/vina \
        --ligand {l_path} \
        --out {out_path} \
        --config {config}"""
        subprocess.call(command, shell = True)


if __name__ == "__main__":
    description = ""
    epilog = ""
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter, usage='%(prog)s [options]', add_help=False)
    parser.add_argument("-f", required=True, help="ligand folder")
    parser.add_argument("-c", required=True, help="protein config")
    # parser.add_argument("-p", required=True, help="protein pdb id")
    # parser.add_argument("-cx", required=True, help="center x")
    # parser.add_argument("-cy", required=True, help="center y")
    # parser.add_argument("-cz", required=True, help="center z")
    # parser.add_argument("-sx", required=True, help="size x")
    # parser.add_argument("-sy", required=True, help="size y")
    # parser.add_argument("-sz", required=True, help="size z")

    args = parser.parse_args()
    main(args)
