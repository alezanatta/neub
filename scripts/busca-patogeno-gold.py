import requests
from bs4 import BeautifulSoup as bs

csv_novo = open("fig3-patogeno.csv", "w")
csv = open("8-uniprot-baceria.csv", "r")

organismos = csv.readlines()

listaOrganismos = {}

for organismo in organismos:
	organismo = organismo.split(";")
	listaOrganismos[organismo[0]] = {'entry':organismo[0], 'especie':organismo[1], 'filo':organismo[2], 'taxonID':organismo[3], 'saf': int(organismo[4])}

csv.close()
csv_novo.close()

for organismo in listaOrganismos:

	csv_novo = open("fig3-patogeno.csv", "a")

	taxonID = listaOrganismos[organismo]['taxonID']
	listaOrganismos[organismo]["existe"] = 1
	listaOrganismos[organismo]["patogeno"] = ""
	listaOrganismos[organismo]["str_patogeno"] = ""
	listaOrganismos[organismo]["fenotipo"] = ""

	print("Iniciando busca por: %s" % taxonID)

	try:

		page = requests.get("""https://gold.jgi.doe.gov/organisms?setColumns=yes&Organism.NCBI+Taxonomy+ID=%s""" % (taxonID))
		soup = bs(page.content, features="html.parser")

		print("Analisando: %s" % taxonID)

		go = soup.find_all("tbody")[-1].find_all("a")[0].get_text()

		print("GOLD id: %s" % go)

		org = requests.get("""https://gold.jgi.doe.gov/organisms?id=%s""" % (str(go)))
		soup = bs(org.content, features="html.parser")

		doenca = soup.find_all("tr")
		for d in doenca:
			if d.find_all("td"):
				if "Diseases" in d.find_all("td")[0].get_text().strip():
					if d.find_all("td")[-1].get_text().strip() != "":
						print("Diseases", end=":")
						print(listaOrganismos[organismo]['especie'], end=":")
						print(listaOrganismos[organismo]['taxonID'], end=":")
						print(d.find_all("td")[-1].get_text().strip())
						print(40*"--")
						if (d.find_all("td")[-1].get_text().strip()) != None:
							listaOrganismos[organismo]["patogeno"] = 1
							listaOrganismos[organismo]["str_patogeno"] = str(d.find_all("td")[-1].get_text().strip())
						else:
							listaOrganismos[organismo]["patogeno"] = 0
							listaOrganismos[organismo]["str_patogeno"] = ""
				if "Phenotypes" in d.find_all("td")[0].get_text().strip():
					if d.find_all("td")[-1].get_text().strip() != "":
						print("Phenotypes", end=":")
						print(listaOrganismos[organismo]['especie'], end=":")
						print(listaOrganismos[organismo]['taxonID'], end=":")
						print(d.find_all("td")[-1].get_text().strip())
						print(40*"--")
						listaOrganismos[organismo]["fenotipo"] = str(d.find_all("td")[-1].get_text().strip())

		csv_novo.write(str(listaOrganismos[organismo]['entry']) + ";" + str(listaOrganismos[organismo]["taxonID"]) + ";" + str(listaOrganismos[organismo]["especie"]) + ";" + str(listaOrganismos[organismo]["filo"]) + ";" + str(listaOrganismos[organismo]["patogeno"]) + ";" + str(listaOrganismos[organismo]["saf"]) + ";" + str(listaOrganismos[organismo]["str_patogeno"]) + ";" + str(listaOrganismos[organismo]["fenotipo"]) + ";" + str(listaOrganismos[organismo]["existe"]) + ";")
		csv_novo.write("\n")
		csv_novo.close()

	except:
		listaOrganismos[organismo]["patogeno"] = -1
		listaOrganismos[organismo]["str_patogeno"] = ""
		listaOrganismos[organismo]["fenotipo"] = -1

		
		csv_novo.write(str(listaOrganismos[organismo]['entry']) + ";" +str(listaOrganismos[organismo]["taxonID"]) + ";" + str(listaOrganismos[organismo]["especie"]) + ";" + str(listaOrganismos[organismo]["filo"]) + ";" + str(listaOrganismos[organismo]["patogeno"]) + ";" + str(listaOrganismos[organismo]["saf"]) + ";" + str(listaOrganismos[organismo]["str_patogeno"]) + ";" + str(listaOrganismos[organismo]["fenotipo"]) + ";" + str(listaOrganismos[organismo]["existe"]) + ";")
		csv_novo.write("\n")
		csv_novo.close()
	
	
csv_novo.close()