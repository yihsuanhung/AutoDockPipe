#!/home/u1/chialang1220/miniconda3/envs/NGS/bin/python3.7

import sys
import os
import subprocess
import argparse
import string

home = os.environ['HOME']
projectId = os.environ['PROJECTID']

star_script = os.path.join(home, "pipe", "rnaseq_pipe", "run_STAR.sh")

cmd = """qsub -q ngs96G -P %s -W group_list=%s \
-N STAR \
-l select=1:ncpus=20 -l place=pack \
-o ${outpath} -e ${errpath} -V \
-- %s --fq1=${fq1} --build=${build} --sample-id=${sid} --outdir=${outdir} \
""" % (projectId, projectId, star_script)

def _check_and_create_dir(d):
	if not os.path.exists(d):
		os.makedirs(d)

def _check_file(f):
	if not os.path.exists(f):
		print("Error: %s dose not exist" % (f))
		sys.exit(1)

def _main(args):
	infile = args.f
	fqdir  = os.path.abspath(args.d)
	outdir = os.path.abspath(args.o)
	build = args.build
	#readmode = args.readmode

	## check directory
	_check_and_create_dir(outdir)

	params = []
	## check fastq file
	with open(infile) as f:
		next(f)
		for line in f:
			data = line.strip().split("\t")
			sid = data[0]
			fqs= data[1].split(";")
			infq1 = os.path.join(fqdir, fqs[0])
			_check_file(infq1)
			infq2 = ""

			## Check sequencing mode
			readmode = "SE"
			if len(fqs) == 2:
				readmode = "PE"
				infq2 = os.path.join(fqdir, fqs[1])
				_check_file(infq2)

			outLogPath = os.path.join(outdir, sid + "_out.txt")
			errLogPath = os.path.join(outdir, sid + "_err.txt")
			params.append((sid, infq1, infq2, outLogPath, errLogPath))

	for p in params:
		qsub_cmd = string.Template(cmd).safe_substitute({
			"fq1"     : p[1],
			"sid"     : p[0],
			"outdir"  : outdir,
			"outpath" : p[3],
			"errpath" : p[4],
			"build"   : build
 			})

		if readmode == "PE":
			qsub_cmd = qsub_cmd + " --fq2=%s" % (p[2])

		print(qsub_cmd)
		subprocess.check_call(qsub_cmd, shell = True)

if __name__ == '__main__':
	# build option parser:
	description = """RNA-seq pipeline: STAR alignment and fusion detection"""
	epilog = """RNA-seq pipeline: STAR alignment and fusion detection"""

	parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter, usage='%(prog)s [options]', add_help=False)
	parser.add_argument("-f", required=True, help="file list for analysis")
	parser.add_argument("-d", required=True, help="Path to fastq directory")
	parser.add_argument("-o", required=True, help="Path to output directory")
	parser.add_argument("-build", required=True, help="Reference version [GRCm38.p6, GRCh38.p12, GRCz11 or index path]")
	#parser.add_argument("-readmode", required=True, help="Read mode (single-end or pair-end)", choices=["SE", "PE"])
	
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(0)

	args = parser.parse_args()

	## Check star_index
	if args.build not in ["GRCm38.p6", "GRCh38.p12", "GRCz11"] and not os.path.exists(args.build):
		print("Error: the build %s dose not exist" % (args.build))
		sys.exit(1)

	_main(args)
