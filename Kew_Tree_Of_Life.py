import pandas as pd
import numpy as np
import treelib as tl



class TreeOfLife:
    def __init__(self):
        self.tree = tl.Tree()
        self.tree.create_node('ROOT', 'ROOT')
        self.taxonTerm = {'Order': [], 'Family': [], 'Genus': []}
        self.hierarchy = ['ROOT', 'Order', 'Family', 'Genus']


    #arguments:
    #Data: path to species .tree file from kew tree of life explorer
    def loadData(self, Data):
        with open(Data) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(')', '')
                line = line.replace('(', '')
                groups = line.split(',')
                for group in groups:
                    taxon = group.split('_')
                    for i, taxa in enumerate(taxon):
                        if taxa not in self.tree.all_nodes():
                            try:
                                if i == 0:
                                    self.tree.create_node(taxa, taxa, parent='ROOT')
                                    self.taxonTerm.get('Order').append(taxa)
                                else:
                                    self.tree.create_node(taxa, taxa, parent=taxon[i - 1])
                                    if i == 1:
                                        self.taxonTerm.get('Family').append(taxa)
                                    elif i == 2:
                                        self.taxonTerm.get('Genus').append(taxa)
                            except:
                                continue


    #arguments:
    #taxa: taxa you want to get broader term for i.e. 'Brassica'
    #term: (optional), default is next term up i.e. if taxa is 'Genus', then term='Family' if term is unspecified. Can be specified to be higher than next level up i.e. term='Order'
    def getBroaderTerm(self, taxa, term=''):
        if len(taxa.split(' ')) > 1:
            taxa = taxa.split(' ')[0]
        taxa = taxa.lower()
        taxa = taxa.capitalize()

        if term == '':
            for key in self.taxonTerm:
                if taxa in self.taxonTerm.get(key): 
                    term = self.hierarchy[self.hierarchy.index(key) - 1]


        term = term.capitalize()
        currTaxa = self.tree.parent(taxa).tag
        while (True):
            if currTaxa in self.taxonTerm.get(term):
                return currTaxa
            currTaxa = self.tree.parent(currTaxa).tag


    def getNarrowerTerms(self, taxa):
        if len(taxa.split(' ')) > 1:
            taxa = taxa.split(' ')[0]
        taxa = taxa.lower()
        taxa = taxa.capitalize()

        output = []

        for i in self.tree.children(taxa):
            output.append(i.tag)
        
        return output


def demo():
    X = TreeOfLife()
    X.loadData('treeoflife.3.0.tree')
    while(True):
        print('taxa:')
        taxa = input()
        print('term:')
        term = input()
        print(X.getBroaderTerm(taxa, term))

X = TreeOfLife()
X.loadData('treeoflife.3.0.tree')
print(X.getNarrowerTerms('cyclanthaceae'))