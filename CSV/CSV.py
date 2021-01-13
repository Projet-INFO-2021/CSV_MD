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

def affiche_module(ordre):
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
	for ligne in readers[1]:	
		if str(num_module) in ligne[0]:
			selection.append(ligne)
	return selection

def liste_SA(nom_activite):
	global readers
	selectionSA = []
	for ligne in readers[2]:		
		if nom_activite == ligne[1]:
			selectionSA.append(ligne)
	return selectionSA

def create_markdown(nomModule):
	MDnom = 'MD_' + nomModule
	if os.path.isdir(nomModule):#Si le dossier Markdown existe on le supprime et on le re-crée
		shutil.rmtree(nomModule)
		os.mkdir(nomModule)
	else:						#Sinon on le crée directement
		os.mkdir(nomModule)

	global select
	listeChap = []
	for ligne in select: 
		if ligne[1] not in listeChap:
			listeChap.append(ligne[1])

	colonneOA = []	
	for chap in listeChap:
		for ligne in select:
			if (ligne[3] != '' and ligne[1] == chap): 
				colonneOA.append(int(ligne[3]))

		path = os.path.join(nomModule, chap) 
		os.mkdir(path)
		colonneOA_Copie = colonneOA		
	
		lignes_chap = [select[i] for i in find([l[1] for l in select],chap)]

		##faire le fichier md _index.md 
		while colonneOA_Copie != []:
			i_minOA = find([l[3] for l in lignes_chap],str(min(colonneOA_Copie)))[0]
			nom_activite = lignes_chap[i_minOA][2]
			path = os.path.join(nomModule + '\\' + chap, nom_activite) 
			os.mkdir(path)
			lignes_activite = [lignes_chap[i] for i in find([l[2] for l in lignes_chap],nom_activite)]
			colonneOSA = [int(ligne[5]) for ligne in lignes_activite]
			colonneOSA_Copie = colonneOSA[:]
			
			#faire le fichier md _index.md
			while colonneOSA_Copie != []:
				i_minOSA = find(colonneOSA, min(colonneOSA_Copie))[0]
				nom_sous_activite = lignes_activite[i_minOSA][4]
				
				description = readers[2]
				lignes_SA = [ligne for ligne in description if ligne[1] == nom_activite and ligne[2] == nom_sous_activite]
				colonneOR = [ligne[4] for ligne in lignes_SA]
				colonneOR_Copie = colonneOR[:]

				if nom_sous_activite == '':
					if lignes_SA != []:
						if lignes_SA[0][4]=='_':
						#creer fichier md
							shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite)
						else:
							while colonneOR_Copie != []:
								i_minOR = find(colonneOR,min(colonneOR_Copie))[0]
								shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite)
								colonneOR_Copie.remove(min(colonneOR_Copie))
						
					#copier directement + md
				else:
					path = os.path.join(nomModule + '\\' + chap +'\\'+ nom_activite,nom_sous_activite) 
					os.mkdir(path)
					if lignes_SA[0][4]=='_':
						#creer fichier md
						shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
					else:
						while colonneOR_Copie != []:
							i_minOR = find(colonneOR,min(colonneOR_Copie))[0]
							shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
							colonneOR_Copie.remove(min(colonneOR_Copie))
				colonneOSA_Copie.remove(min(colonneOSA_Copie))
			colonneOA_Copie.remove(min(colonneOA_Copie))
			#faire le fichier md _index.md

Ressources = 'Ressources'

module = 'CSI3_Projet_test_2'
readers=CreerTableaux()
#affiche_module(1)

select = choix_selection(choix_module(module))
selectSA = liste_SA('Innovations')

#affiche_chapitre(1)
writer.close()

create_markdown(module)

print('done')