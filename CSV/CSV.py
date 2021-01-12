import csv
import os
import shutil
writer=open('Mark.md','w')
writer.write('bonjooour\n')

   
def find(L,x):
	return [i for i in range(len(L)) if L[i] == x]

def CreerTableaux():
	f_module = open("Module_csv.csv", "r")
	f_structure = open("Structure_csv.csv","r")
	f_description = open("Description_csv.csv","r")#on ouvre les 3 fichiers csv
	fichiers = [f_module,f_structure,f_description]#on cr�e une liste qui contient en brut les 3 fichiers ouverts
	readers = []
	for fichier in fichiers: 
		reader = csv.reader(fichier)
		reader = [x[0].strip().split(';') for x in reader]
		reader = [x for x in reader if x != ['']*len(reader[0])] #suppression des lignes vides
		readers.append(reader) #readers contient des listes contenant les infos des tableaux
	for x in range (0, len(readers[1])):#on divise la colonne de s�lection du structure
		readers[1][x][0] = readers[1][x][0].split('.')#pour l'afficher � chaque fois qu'il est d�lection�
	return readers




def affiche_module(ordre):#
    for i in range(1,len(readers[0])):
        if(int(readers[0][i][0])==ordre):
            #print(readers[0][i][0])
            #print(readers[0][i][1])
            #writer.writelines(readers[0][i][0]+"\n")
            writer.writelines(readers[0][i][1]+"\n")
            #affiche_chapitre(1)
            

def affiche_chapitre(selec_module):
		selection = choix_selection(selec_module)
		chapitre=[]
		for i in range(1,len(selection)-1):
			if selection[i][1] not in chapitre:
				chapitre.append(selection[i][1])
		for x in range (len(chapitre)):
			ligne=("		"+chapitre[x]+"\n")
			writer.writelines(ligne)
		return


def affiche_activite(selec_module,chap):
		selection = choix_selection(selec_module)
		activite=[]
		for i in range(0,len(selection)-1):
			if selection[i][2] not in activite and selection[i][1]==chap:
				activite.append(selection[i][2])
		for x in range (len(activite)):
					ligne=("			"+activite[x]+"\n")

					writer.writelines(ligne)
		return
	



def choix_module(nomModule):
	global readers
	numero = readers[0][find([L[1] for L in readers[0]],nomModule)[0]][0]
	return int(numero)




def choix_selection(num_module):#on récupère certaines lignes du tableau en fonction du module
	global readers
	selection = []
	for x in range (0, len(readers[1])):		
		if str(num_module) in readers[1][x][0]:
			selection.append(readers[1][x])
	return selection

def create_markdown(nomModule):
	if os.path.isdir(nomModule):#Si le dossier Markdown existe on le supprime et on le re-crée
		shutil.rmtree(nomModule)
		os.mkdir(nomModule)
	else:						#Sinon on le crée directement
		os.mkdir(nomModule)
	global select
	colonneOA = []
	listeChap = []
	for i in range(len(select)):
		if select[i][1] not in listeChap:
			#print(select[i][1])
			listeChap.append(select[i][1])

	for chap in listeChap:
		for y in range(len(select)):
			if select[y][3] != '' and select[y][1] == chap: 
				colonneOA.append(int(select[i][3]))
		#print(listeChap)
		path = os.path.join(nomModule, chap) 
		os.mkdir(path)
		colonneOA_Copie = colonneOA
		
		##faire le fdp fichier md _index.md 
		while colonneOA_Copie != []:
			lignes_chap = [select[i] for i in find([select[j][1] for j in range(len(select))],chap)]
			i_min = find([l[3] for l in lignes_chap],str(min(colonneOA_Copie)))[0]
			print(colonneOA_Copie)
			nom_activite = lignes_chap[i_min][2]
			path = os.path.join(nomModule + '\\' + chap, nom_activite) 
			os.mkdir(path)
			del colonneOA_Copie[i_min]

							


	




readers=CreerTableaux()
#affiche_module(1)


select = choix_selection(choix_module('CSI3_Projet_test_2'))


#affiche_chapitre(1)
writer.close()

create_markdown('CSI3_Projet_test_2')