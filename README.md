This program parses and loads a Kew Botanic Garden Tree of Life .tree file into a TreeOfLife object.
Updated/revised .tree files from Kew can be found below in the "Access Data" tab: 
https://treeoflife.kew.org/


Taxonomic terms higher than order are taken from this publication(https://pmc.ncbi.nlm.nih.gov/articles/PMC4418965/#sec015)
and stored in a .txt file. Revisions made at the level of Order or Above must be made to the .txt file


The example code below creates a new TreeOfLife object, X.
Using the loadData method, we can load the .txt file containing higher taxa, as well as the Kew .tree file
the loadData method takes a long time (about a minute and a half) because parsing the .tree file is slow

  X = TreeOfLife()
  X.loadTreeFile('treeoflife.3.0.tree', 'HigherTaxa.txt')
  X.getBroaderTerm(cyclanthaceae)
        ***Returns "Pandanales"
  
  X.getBroaderTerm(cyclanthaceae, Kingdom)
        ***Returns "Plantae"

  X.getNarrowerTerms(cyclanthaceae)
        ***Returns ['Cyclanthus', 'Schultesiophytum', 'Stelestylis', 'Sphaeradenia', 'Chorigyne', 'Dicranopygium', 'Evodianthus', 'Ludovia', 'Carludovica']
