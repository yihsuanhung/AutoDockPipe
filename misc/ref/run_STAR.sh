#!/bin/bash

source $HOME/.bashrc
conda activate NGS

function usage()
{
	echo "if this was a real script you would see something useful here"
	echo "./run_star.sh --fq1=fq1 [--fq2=fq2] --build=build --sample-id=sid --outdir=outdir"
	echo "\t-h --help"
}

fq1=""
fq2=""
while [ "$1" != "" ]; do
	PARAM=`echo $1 | awk -F= '{print $1}'`
	VALUE=`echo $1 | awk -F= '{print $2}'`
	case $PARAM in
		-h | --help)
			usage
			exit
			;;
		--fq1)
			fq1=$VALUE
			;;
		--fq2)
			fq2=$VALUE
			;;
		--build)
			build=$VALUE
			;;
		--sample-id)
			sampleID=$VALUE
			;;
		--outdir)
			outDir=$VALUE
			;;
		*)
			echo "ERROR: unknown parameter \"$PARAM\""
			usage
			exit
			;;
	esac
	shift
done

### Check files
### Single end reads
if [ -z $fq1 ]; then
	echo -e -n "Error: --fq1 is required\n"
	exit
else
	if [ ! -f $fq1 ]; then
		echo -e -n "Error: $fq1 does not exist\n"
		exit
	fi
fi

### Pair end reads
if [ ! -z $fq2 ] && [ ! -f $fq2 ]; then
	echo -e -n "Error: $fq1 or $fq2 does not exist\n"
	exit
fi

refDir=$RefDir/$build/star_index

if [ $build == "GRCh38.p12" ]; then
	#ref=$refDir/GRCh37_v19_CTAT_lib_Feb092018/ctat_genome_lib_build_dir/ref_genome.fa.star.idx
	gtf=$RefDir/$build/gencode.v28.annotation.gtf
	#catLibDir=$refDir/GRCh37_v19_CTAT_lib_Feb092018/ctat_genome_lib_build_dir
elif [ $build == "GRCm38.p6" ]; then
	gtf=$RefDir/$build/gencode.vM19.annotation.gtf
elif [ $build == "GRCz11" ]; then
	gtf=$refDir/annotation.gtf
elif [ -e $build ]; then
	refDir=$build/star_index
	gtf=$refDir/annotation.gtf
else
	echo -e -n "$build is not avaiable. (GRCh38.p12, GRCm38.p6, GRCz11, or directory to star_index)\n"
	exit
fi

prefix=$outDir/$sampleID

if [ ! -e $prefix ]; then
	mkdir -p $prefix
fi

fq="$fq1 $fq2"

STAR \
--runMode alignReads \
--genomeDir $refDir \
--readFilesIn $fq \
--runThreadN 16 \
--twopassMode Basic \
--outFilterMultimapScoreRange 1 \
--outFilterMultimapNmax 20 \
--outFilterMismatchNmax 20 \
--alignIntronMax 500000 \
--alignMatesGapMax 1000000 \
--sjdbScore 2 \
--alignSJDBoverhangMin 10 \
--genomeLoad NoSharedMemory \
--chimSegmentMin 12 \
--chimJunctionOverhangMin 12 \
--chimSegmentReadGapMax 3 \
--alignSJstitchMismatchNmax 5 -1 5 5 \
--limitBAMsortRAM 0 \
--readFilesCommand zcat \
--outFilterMatchNminOverLread 0.33 \
--outFilterScoreMinOverLread 0.33 \
--sjdbOverhang 100 \
--outSAMstrandField intronMotif \
--sjdbGTFfile $gtf \
--outSAMattributes NH HI NM MD AS XS \
--outSAMunmapped Within \
--outSAMtype BAM SortedByCoordinate \
--outSAMheaderHD @HD VN:1.4 \
--outSAMattrRGline ID:$sampleID SM:$sampleID PL:illumina \
--quantMode GeneCounts \
--outFileNamePrefix $prefix/${sampleID}.

rm -rf $prefix/${sampleID}._STARpass1
rm -rf $prefix/${sampleID}._STARgenome

samtools index $prefix/${sampleID}.Aligned.sortedByCoord.out.bam

#STAR-Fusion \
#--genome_lib_dir $catLibDir \
#--chimeric_junction $prefix/Chimeric.out.junction  \
#--output_dir $prefix/ \
#--CPU 8 

#rm -rf $prefix/_starF_checkpoints
#rm -rf $prefix/star-fusion.preliminary

#rm -rf $prefix/Log.progress.out
