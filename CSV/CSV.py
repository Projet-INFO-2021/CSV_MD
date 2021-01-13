import csv
import os
import shutil

def find(L,x):#renvoie la liste des indices i tels que L[i] == x
	return [i for i in range(len(L)) if L[i] == x]

def CreerTableaux(Module, Structure, Description):#renvoie la liste des csv, chacun sous forme de liste de listes
	f_module = open(Module, "r")
	f_structure = open(Structure,"r")
	f_description = open(Description,"r")#on ouvre les 3 fichiers csv
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

def choix_module(nomModule, readers):#renvoie le numéro correspondant au nom d'un module
	noms_modules = [L[1] for L in readers[0]]
	i_module = find(noms_modules,nomModule)[0]
	numero = readers[0][i_module][0]#le numéro est dans la première colonne
	return numero

def choix_selection(nomModule,readers):#on renvoie les lignes du tableau qui correspondent au module
	num_module = choix_module(nomModule,readers)
	selection = []
	for ligne in readers[1]:
		if num_module in ligne[0]:#si la ligne fait partie du module
			selection.append(ligne)
	return selection

def create_markdown(Module, Structure, Description, Ressources, nomModule):
	global writer
	MDnom = 'MD_' + nomModule
	if os.path.isdir(nomModule):#Si le dossier Markdown existe on le supprime et on le re-crée
		shutil.rmtree(nomModule)
		os.mkdir(nomModule)
	else:						#Sinon on le crée directement
		os.mkdir(nomModule)
	writer=open(nomModule +'/'+'_index.md','w')
	writer.write('---\ntitle: '+ nomModule + '\ndraft: False\nmenu: "main"\n---\n\n<html>\n<h1>'+ nomModule + '</h1>\n</html>\n\n')

	readers=CreerTableaux(Module , Structure , Description)

	select = choix_selection(nomModule, readers)#on récupère toutes les lignes de structure correspondant au module

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

		colonneOA_Copie = colonneOA[:]

		i_chap = find([l[1] for l in select],chap)#liste des indices des lignes de structure correspondant au chapitre
		lignes_chap = [select[i] for i in i_chap]

		while colonneOA_Copie != []:#tant qu'il reste des activités
			i_minOA = find([l[3] for l in lignes_chap],str(min(colonneOA_Copie)))[0]#indice de la ligne de la prochaine activité à gérer
			nom_activite = lignes_chap[i_minOA][2]#nom correspondant
			#écriture dans le markdown
			line=("	- "+nom_activite+"\n")
			writer.writelines(line)
			#création dossier
			path = os.path.join(nomModule + '\\' + chap, nom_activite) 
			os.mkdir(path)

			i_activite = find([l[2] for l in lignes_chap], nom_activite)#indices des lignes correspondant à l'activité
			lignes_activite = [lignes_chap[i] for i in i_activite]

			colonneOSA = [int(ligne[5]) for ligne in lignes_activite]#ordres des sous-activités
			colonneOSA_Copie = colonneOSA[:]
			
			while colonneOSA_Copie != []:#tant qu'il reste des sous-activités
				i_minOSA = find(colonneOSA, min(colonneOSA_Copie))[0]#indice de la ligne de la prochaine sous-activité à gérer
				nom_sous_activite = lignes_activite[i_minOSA][4]#nom correspondant
				
				description = readers[2]
				lignes_SA = [ligne for ligne in description if ligne[1] == nom_activite and ligne[2] == nom_sous_activite]#lignes utiles
				colonneOR = [ligne[4] for ligne in lignes_SA]#ordres utiles
				colonneOR_Copie = colonneOR[:]

				if nom_sous_activite == '':#si pas de sous-activité
					if lignes_SA != []:#s'il y a bien au moins une sous-activité
						if lignes_SA[0][4]=='_':#si ressource isolée
							line=("		- ["+lignes_SA[0][5]+"]("+'/'+nomModule+'/'+chap+'/'+nom_activite+'/'+lignes_SA[0][5]+')\n')
							writer.writelines(line)#écrit dans le md
							shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite)
							#on copie le fichier correspondant
						else:#si plusieurs ressources : calcul de l'ordre d'affichage
							while colonneOR_Copie != []:#tant qu'il reste des ressources
								i_minOR = find(colonneOR,min(colonneOR_Copie))[0]#indice de la prochaine ressource à gérer

								line=("		- ["+lignes_SA[i_minOR][5]+"](/"+nomModule+'/'+chap+'/'+nom_activite+'/'+lignes_SA[i_minOR][5]+')\n')
								writer.writelines(line)#écriture md

								shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite)
								#copie du fichier

								colonneOR_Copie.remove(min(colonneOR_Copie))#on retire l'ordre de la ressource gérée
				else:#si ss-activité
					line=("		- "+nom_sous_activite+"\n")
					writer.writelines(line)#écriture md

					path = os.path.join(nomModule + '\\' + chap +'\\'+ nom_activite,nom_sous_activite) 
					os.mkdir(path)#création dossier

					if lignes_SA[0][4]=='_':#si ressource isolée
						line=("			- ["+lignes_SA[0][5]+"]"+'(/'+nomModule+'/'+chap+'/'+nom_activite+'/'+nom_sous_activite+'/'+lignes_SA[0][5]+')\n')
						writer.writelines(line)#écriture md

						shutil.copy2(Ressources+'\\'+chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[0][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
						#copie fichier
					else:#si plusieurs ressources : calcul de l'ordre d'affichage
						while colonneOR_Copie != []:#tant qu'il reste des ressources
							i_minOR = find(colonneOR,min(colonneOR_Copie))[0]#indice de la prochaine ressource à gérer

							line=("			- ["+lignes_SA[i_minOR][5]+"](/"+nomModule+'/'+chap+'/'+nom_activite+'/'+nom_sous_activite+'/'+lignes_SA[i_minOR][5]+')\n')
							writer.writelines(line)#écriture md

							shutil.copy2(Ressources + '\\' + chap + '\\'+nom_activite+'\\'+nom_sous_activite+'\\'+lignes_SA[i_minOR][5],nomModule+'\\'+chap+'\\'+nom_activite+'\\'+nom_sous_activite)
							#copie fichier
							colonneOR_Copie.remove(min(colonneOR_Copie))#on retire l'ordre de la ressource gérée
				colonneOSA_Copie.remove(min(colonneOSA_Copie))#on retire l'ordre de la ss-activité gérée
			colonneOA_Copie.remove(min(colonneOA_Copie))#on retire l'ordre de l'activité gérée

def CSV(Module, Structure, Description, Dossier, nomModule):
	create_markdown(Module, Structure, Description, Dossier, nomModule)
	writer.close()

Chemin1 = r'C:\Users\jroua\Desktop\Test\Module_csv.csv'
Chemin2 = r'C:\Users\jroua\Desktop\Test\Structure_csv.csv'
Chemin3 = r'C:\Users\jroua\Desktop\Test\Description_csv.csv'
Chemin4 = r'C:/Users/jroua/Desktop/Test/Ressources'
nom_du_module = 'CSI3_Projet_test_2'

CSV(Chemin1, Chemin2, Chemin3, Chemin4, nom_du_module)