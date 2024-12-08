import pandas as pd
import numpy as np
import treelib as tl
import functools
import operator


class TreeOfLife:
    def __init__(self):
        self.tree = tl.Tree()
        self.taxonTerm = {'Kingdom': [], 'Phylum': [], 'Class': [], 'Order': [], 'Family': [], 'Genus': []}
        self.hierarchy = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus']
        self.ignore = ['KINGDOM', 'SUBKINGDOM', 'INFRAKINGDOM', 'Subphylum', 'Subclass', 'Superorder', 'Superclass']

        self.tree.create_node('Plantae', 'Plantae')
        self.taxonTerm.get('Kingdom').append('Plantae')


    #arguments:
    #Data: path to species .tree file from kew tree of life explorer
    def loadData(self, Kew_Data, Orders_File=''):
        with open(Orders_File, encoding="utf8") as O:
            lines = O.readlines()

            currOn = [None, None, None, None]
            for line in lines:
                line = line.replace('\t', '')
                line = line.replace('"', '')
                line = line.split(' ')

                if line[0] in self.ignore:
                    continue

                currTaxa = line[1].strip()
                try:
                    if line[0] == self.hierarchy[1]:
                        self.tree.create_node(currTaxa, currTaxa, parent='Plantae')
                        self.taxonTerm.get(line[0]).append(currTaxa)
                        currOn[1] = currTaxa
                    elif line[0] == self.hierarchy[2]:
                        self.tree.create_node(currTaxa, currTaxa, parent=currOn[1])
                        self.taxonTerm.get(line[0]).append(currTaxa)
                        currOn[2] = currTaxa
                    elif line[0] == self.hierarchy[3]:
                        self.tree.create_node(currTaxa, currTaxa, parent=currOn[2])
                        self.taxonTerm.get(line[0]).append(currTaxa)
                        currOn[3] = currTaxa
                    elif line[0] == self.hierarchy[4]:
                        self.tree.create_node(currTaxa, currTaxa, parent=currOn[3])
                        self.taxonTerm.get(line[0]).append(currTaxa)

                except:
                    continue

        with open(Kew_Data, encoding="utf8") as f:
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
                                    self.tree.create_node(taxa, taxa, parent='Plantae')
                                    self.taxonTerm.get('Order').append(taxa)
                                else:
                                    self.tree.create_node(taxa, taxa, parent=taxon[i - 1])
                                    if i == 1:
                                        self.taxonTerm.get('Family').append(taxa)
                                    elif i == 2:
                                        self.taxonTerm.get('Genus').append(taxa)
                            except:
                                continue


    # arguments:
    # taxa: taxa you want to get broader term for i.e. 'Brassica'
    # term: (optional), default is next term up i.e. if taxa is 'Genus', then term='Family' if term is unspecified. Can be specified to be higher than next level up i.e. term='Order'
    # returns a string
    def getBroaderTerm(self, taxa, term=''):
        if len(taxa.split(' ')) > 1:
            taxa = taxa.split(' ')[0]
        taxa = taxa.lower()
        taxa = taxa.capitalize()

        if taxa in functools.reduce(operator.iconcat, self.taxonTerm.values(), []):
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


    # arguments:
    # taxa: taxa you want to get narrower terms for i.e. 'Cyclanthaceae'
    # returns a list of strings
    def getNarrowerTerms(self, taxa):
        if len(taxa.split(' ')) > 1:
            taxa = taxa.split(' ')[0]
        taxa = taxa.lower()
        taxa = taxa.capitalize()

        if taxa in functools.reduce(operator.iconcat, self.taxonTerm.values(), []):
            output = []

            for i in self.tree.children(taxa):
                output.append(i.tag)
            
            return output


def demo():
    X = TreeOfLife()
    X.loadData('treeoflife.3.0.tree', 'HigherTaxa.txt')
    while(True):
        taxa = input("taxa: ")
        term = input("term: ")
        print(X.getBroaderTerm(taxa, term))

demo()