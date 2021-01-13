import csv
import os
import shutil

   
def find(L,x):#renvoie la liste des indices i tels que L[i] == x
	return [i for i in range(len(L)) if L[i] == x]

def CreerTableaux():#renvoie la liste des csv, chacun sous forme de liste de listes
	f_module = open("Module_csv.csv", "r")
	f_structure = open("Structure_csv.csv","r")
	f_description = open("Description_csv.csv","r")#on ouvre les 3 fichiers csv
	fichiers = [f_module,f_structure,f_description]#on crée une liste qui contient en brut les 3 fichiers ouverts

	readers = []#liste qui va contenir les csv arrangés

	for fichier in fichiers: 
		reader = csv.reader(fichier)#reader est une liste de singletons de strings
		reader = [x[0].strip().split(';') for x in reader]#on transforme chaque singleton de longs str (une ligne) en liste de petits str (les cases)
		reader = [x for x in reader if x != ['']*len(reader[0])] #suppression des lignes vides
		readers.append(reader) #on ajoute le csv sous la forme voulue à la liste

	for x in readers[1]:#arrangement de la premiere colonne de structure
		x[0] = x[0].split('.')#on transforme '1.2' en ['1','2']

	return readers

def choix_module(nomModule):#renvoie le numéro correspondant au nom d'un module
	global readers
	noms_modules = [L[1] for L in readers[0]]
	i_module = find(noms_module,nomModule)[0]
	numero = readers[0][i_module][0]#le numéro est dans la première colonne
	return numero

def choix_selection(num_module):#on renvoie les lignes du tableau qui correspondent au module
	global readers
	selection = []
	for ligne in readers[1]:
		if num_module in ligne[0]:#si la ligne fait partie du module
			selection.append(ligne)
	return selection

def liste_SA(nom_activite):#renvoie les lignes de description liées à une activité
	global readers
	selectionSA = []
	for ligne in readers[2]:
		if nom_activite == ligne[1]:
			selectionSA.append(ligne)
	return selectionSA

def create_markdown(nomModule):
	global writer
	MDnom = 'MD_' + nomModule
	if os.path.isdir(nomModule):#Si le dossier Markdown existe on le supprime et on le re-crée
		shutil.rmtree(nomModule)
		os.mkdir(nomModule)
	else:						#Sinon on le crée directement
		os.mkdir(nomModule)
	writer=open(nomModule +'/'+'_index.md','w')
	writer.write('---\ntitle: '+ nomModule + '\ndraft: False\nmenu: "main"\n---\n\n<html>\n<h1>'+ nomModule + '</h1>\n</html>\n\n')

	select = choix_selection(choix_module(nomModule))#on récupère toutes les lignes de structure correspondant au module

	listeChap = []#liste des str des chapitres
	for ligne in select:
		if ligne[1] not in listeChap:
			listeChap.append(ligne[1])
	
	for chap in listeChap:
		line=("- " + chap+ "\n")
		writer.writelines(line)

		path = os.path.join(nomModule, chap) 
		os.mkdir(path)

		colonneOA = []#liste des ordres d'activité
		for ligne in select:		
			if (ligne[3] != '' and ligne[1] == chap): 
				colonneOA.append(int(ligne[3]))

		

		colonneOA_Copie = colonneOA		
	
		lignes_chap = [select[i] for i in find([l[1] for l in select],chap)]

		##faire le fichier md _index.md 
		while colonneOA_Copie != []:
			i_minOA = find([l[3] for l in lignes_chap],str(min(colonneOA_Copie)))[0]
			nom_activite = lignes_chap[i_minOA][2]
			line=("	- "+nom_activite+"\n")
			writer.writelines(line)
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
							line=("		- ["+lignes_SA[0][5]+"]("+'/'+nomModule+'/'+chap+'/'+nom_activite+'/'+lignes_SA[0][5]+')\n')
							writer.writelines(line)#ajoute une ressource
							shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite)
						else:
							while colonneOR_Copie != []:
								i_minOR = find(colonneOR,min(colonneOR_Copie))[0]
								line=("		- ["+lignes_SA[i_minOR][5]+"](/"+nomModule+'/'+chap+'/'+nom_activite+'/'+lignes_SA[i_minOR][5]+')\n')
								writer.writelines(line)#ajoute une ressource
								shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite)
								colonneOR_Copie.remove(min(colonneOR_Copie))
						
					#copier directement + md
				else:
					line=("		- "+nom_sous_activite+"\n")
					writer.writelines(line)
					path = os.path.join(nomModule + '\\' + chap +'\\'+ nom_activite,nom_sous_activite) 
					os.mkdir(path)
					if lignes_SA[0][4]=='_':
						#creer fichier md
						line=("			- ["+lignes_SA[0][5]+"]"+'(/'+nomModule+'/'+chap+'/'+nom_activite+'/'+nom_sous_activite+'/'+lignes_SA[0][5]+')\n')
						writer.writelines(line)#ajoute une ressource
						shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
					else:
						while colonneOR_Copie != []:
							i_minOR = find(colonneOR,min(colonneOR_Copie))[0]
							line=("			- ["+lignes_SA[i_minOR][5]+"](/"+nomModule+'/'+chap+'/'+nom_activite+'/'+nom_sous_activite+'/'+lignes_SA[i_minOR][5]+')\n')
							writer.writelines(line)#ajoute un ressource
							shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
							colonneOR_Copie.remove(min(colonneOR_Copie))
				colonneOSA_Copie.remove(min(colonneOSA_Copie))
			colonneOA_Copie.remove(min(colonneOA_Copie))
			#faire le fichier md _index.md


def CSV(nomModule):
	module = nomModule
	module = 'CSI3_Projet_test_1'
	readers=CreerTableaux()
	select = choix_selection(choix_module(module))
	selectSA = liste_SA('Innovations')
	create_markdown(module)
	writer.close()
