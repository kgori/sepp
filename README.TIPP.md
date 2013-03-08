------------------------------------
Summary
------------------------------------

TIPP stands for "Taxon Identification using Phylogenetic Placement". TIPP classifies unknown fragmentary sequences into a given taxonomy. TIPP uses phylogenetic placement on a reference alignment/tree for classification. It requires that input fragments come from the same gene as the full length sequences in the reference alignment. 

Input: a reference tree T and alignment A for a set of full-length sequences corresponding to a (marker) gene, a taxonomy T', a mapping M between sequence names and species labels in the taxonomy, and finally set X of fragmentary sequences for the same gene

Output: classification of each fragment in X according to taxonomy T'.

Therefore, TIPP requires that the set of input fragments actually belong to the reference (marker) gene. TIPP operates by first using SEPP to align and place fragments to the reference alignment and on the reference tree in multiple ways (to account for uncertainty) with estimates of support for each placement, then mapping each placement into the taxonomy T' and calculating a total support for classification of the fragment at every node in the taxonomy. The support values can then be used to find the classification with highest support at every level. 

SEPP operates by using a divide-and-conquer strategy adopted from SATe [Liu et. al., Science, 2009 (http://www.sciencemag.org/content/324/5934/1561.abstract)] to improve the alignment produced by running HMMER (code by Sean Eddy). It then places each fragment into the user-provided tree using pplacer (code by Erick Matsen), or EPA. Our study shows that SEPP provides improved accuracy for quickly evolving genes as compared to other methods.

Developers: Tandy Warnow, Nam Nguyen, and Siavash Mirarab

Publication:
TBA

Note and Acknowledgment: TIPP bundles the following two programs into its distribution:
1- pplacer: http://matsen.fhcrc.org/pplacer/
2- hmmer: http://hmmer.janelia.org/
3- epa: http://sco.h-its.org/exelixis/software.html

-------------------------------------
Installation
-------------------------------------
This section details steps for installing and running SEPP. We have run SEPP on Linux and MAC. If you experience difficulty installing or running the software, please contact one of us (Tandy Warnow, Nam Nguyen, or Siavash Mirarab).

Requirements:
-------------------
Before installing the software you need to make sure the following programs are installed on your machine.

1. Python: Version > 2.6. 
2. Java: Version > 1.5

Installation Steps:
-------------------
TIPP is distributed as Python source code. Once you have the above required software installed, do the following. 

1. Obtain the latest TIPP distribution from the paper submission page. Uncompress the archive file into your favorite location.
2. Go to the distribution directory
3. Install: run "sudo python setup.py install". 
4. Configure: run "sudo python setup.py config". 

The last step creates a ~/.sepp/ directory and put the default config file under ~/.sepp/main.config. Since this is specific to a user, each user that runs TIPP needs to execute the last step. 

Common Problems:
-------------------
1. The last step by default requires root access to the system. If you do not have root access, invoke the setup script as follows: "python setup.py install --prefix=/some/path/on/your/system", where "/some/path/on/your/system" is the path to a directory on your system to which you do have read and write access. If you use the "--prefix" option, you must ensure that the "lib/python2.x/site-packages" subdirectory (where "x" denotes the minor version number of your Python install) of the directory you specify following "--prefix=" is on Python's search path. To add a directory to Python's search path, modify your PYTHONPATH environment variable.

2. TIPP relies on pplacer or EPA and HMMER for alignment and placement steps. These tools are packaged with TIPP. If for some reason the packaged version of HMMER, EPA, or pplacer do not run in your environment, you need to download and build those programs for your system (see below for links), and point TIPP to them. To point TIPP to your installation of epa, hmmer and pllacer modify ~/.sepp/main.config. 
   pplacer: http://matsen.fhcrc.org/pplacer/
   hmmer://hmmer.janelia.org/
   epa: http://sco.h-its.org/exelixis/software.html


---------------------------------------------
Running TIPP
---------------------------------------------
To run TIPP, invoke the "run_tipp.py" script from the "bin" sub-directory of the location in which you installed the Python packages (it should be automatically added to your path). To see options for running the script, use the command:

"python <bin>/run_tipp.py -h"

or simply:

``run_tipp.py -h''

The general command for running TIPP is:

"python <bin>/run_tipp.py -t <placement_tree_file> -a <ref_alignment_file> -f <fragment_file> -r <raxml_info_file> -tx <taxonomy_file> -txm <mapping_taxonomy_to_gene_file> [-adt reference_tree_file>] [-A <alignment_set_size>] [-P <placement_set_size>] [-at <alignment_support>] [-pt placement_support]"

To learn more about the input options refer to TIPP help (``run_tipp.py -h''). 

All the input parameters, except for fragment file are specific to a marker gene. We have put together reference packages for 30 marker genes, and have made those marker datasets available as part of our submission web-site at http://www.cs.utexas.edu/~phylo/software/sepp/tipp-submission/. 

To run TIPP-def, i.e. (95%,95%,100), on rspB marker genes for fragmentary reads in fragments.fas, you can use the following command:

run_tipp.py -t rpsB.refpkg/sate.taxonomy -a rpsB.refpkg/sate.fasta -r rpsB.refpkg/sate.taxonomy.RAxML_info -at 0.95 -pt 0.95 -tx rpsB.refpkg/all_taxon.taxonomy -txm rpsB.refpkg/species.mapping -adt rpsB.refpkg/sate.tree.ml -A 100 -f fragments.fas -o rpsB_run 

To run TIPP-large on 16S bacteria, you can use the following command:

run_tipp.py -t 16S_bacteria.refpkg/sate.taxonomy -a 16S_bacteria.refpkg/sate.fasta -r 16S_bacteria.refpkg/sate.taxonomy.RAxML_info -at 0.95  -pt 0.95 -tx  16S_bacteria.refpkg/all_taxon.taxonomy -txm 16S_bacteria.refpkg/species.mapping -adt 16S_bacteria.refpkg/sate.tree.ml -A 100 -P 1000 -f fragments.fas -o 16S_bacteria_run

TIPP can also be run using a configuration file. Sample configuration files and input files can be found under TODO. Change to that directory to run TIPP on the sample files. To run using command options, run

"python <bin>/run_tipp.py TODO fill this"

and to run using a configuration file, run

"python <bin>/run_tipp.py -c sample.config"

The main output of TIPP is a file called <name_of_your_run>_classification.txt. In this file, each line shows a potential classification of a fragment and its probability. Each line is a comma-separated list of values. The first value is the fragment name, the second value is the taxonid (according to input taxonomy) for the classification, the third value is the name of the OTU, the fourth value is the taxonomic rank, and the last value is the TIPP-estimated probability that the fragment belongs to that OTU. For example,

``EAS25_26_1_75_674_1432_0_2,28890,Euryarchaeota,phylum,.6141''

means TIPP estimates that there is a 61% chance that fragment EAS25_26_1_75_674_1432_0_2 belong to phylum Euryarchaeota from NCBI taxonomy (which has taxon id 28890). 


Hence TIPP is based on running SEPP, it also produces extended alignments and placements of the fragments on the placement tree. These outputs are generated in the same directory as the main output. Extended alignments are in Fasta format. Placement results are in json format. Please refer to pplacer website (currently http://matsen.github.com/pplacer/generated_rst/pplacer.html#json-format-specification) for more information on the format of the josn file. Also note that pplacer package provides a program called guppy that can read .json files and perform downstream steps such as visualization.

By setting TIPP_DEBUG environmental variable to "True", you can instruct TIPP to output more information that can be helpful for debugging.  

---------------------------------------------
Bugs and Errors
---------------------------------------------
TIPP is under active research development at UTCS by the Warnow Lab (and especially with her PhD students Siavash Mirarab and Nam Nguyen). Please report any errors to Siavash Mirarab (smirarab@gmail.com) and Nam Nguyen (namphuon@cs.utexas.edu).
