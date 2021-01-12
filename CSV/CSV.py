import csv
import os
writer=open('Mark.md','w')
writer.write('bonjooour\n')

   
def find(L,x):
	return [i for i in range(len(L)) if L[i] == x]


def CreerTableaux():
	f_module = open("Module_csv.csv", "r")
	f_structure = open("Structure_csv.csv","r")
	f_description = open("Description_csv.csv","r")
	fichiers = [f_module,f_structure,f_description]
	readers = []
	for fichier in fichiers:  #suppression des lignes vides
		reader = csv.reader(fichier)
		reader = [x[0].strip().split(';') for x in reader]
		reader = [x for x in reader if x != ['']*len(reader[0])]
		readers.append(reader) #readers contient des listes contenant les infos des tableaux
	for x in range (0, len(readers[1])):
		readers[1][x][0] = readers[1][x][0].split('.')
	return readers




def affiche_module(ordre):
    for i in range(1,len(readers[0])):
        if(int(readers[0][i][0])==ordre):
            print(readers[0][i][0])
            print(readers[0][i][1])
            #writer.writelines(readers[0][i][0]+"\n")
            writer.writelines(readers[0][i][1]+"\n")
            #affiche_chapitre(1)
            

def affiche_chapitre(selec_module):
		selection = choix_selection(selec_module)
		chapitre=[]
		for i in range(0,len(selection)):
			if selection[x][1] not in chapitre:
				chapitre.append(selection[x][1])
		for x in range (len(chapitre)):
			ligne=("		"+readers[1][i][1]+"\n")
			writer.writelines(ligne)
		return




def choix_module(nomModule):
	global readers
	numero = readers[0][find([L[1] for L in readers[0]],nomModule)[0]][0]
	return int(numero)




def choix_selection(num_module):
	global readers
	selection = []
	for x in range (0, len(readers[1])):		
		if str(num_module) in readers[1][x][0]:
			selection.append(readers[1][x])
	return selection


	



readers=CreerTableaux()
affiche_module(1)
print(readers[0])


select = choix_selection(choix_module('CSI3_Projet_test_1'))

for x in select:
	print(x)

affiche_chapitre(1)
writer.close()