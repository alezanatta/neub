import requests
from time import sleep
from bs4 import BeautifulSoup as bs

csv_novo = open("fig3-patogeno-kegg.csv", "w")
csv = open("8-uniprot-baceria.csv", "r")

organismos = csv.readlines()

listaOrganismos = {}

for organismo in organismos:
    organismo = organismo.split(";")
    listaOrganismos[organismo[0]] = {'entry':organismo[0], 'especie':organismo[1], 'filo':organismo[2], 'taxonID':organismo[3], 'saf': int(organismo[4])}

csv.close()
csv_novo.close()

for organismo in listaOrganismos:
    try:
        taxonID = listaOrganismos[organismo]['taxonID']

        print("Iniciando busca por: %s" % taxonID)

        page = requests.get("""https://www.genome.jp/dbget-bin/www_bfind_sub?mode=bfind&max_hit=1000&locale=en&serv=gn&dbkey=genome&keywords=%s&page=1""" % taxonID)
        soup = bs(page.content, features="html.parser")

        go = soup.find_all("div")

        for g in go:
            if g.find_all("a"):
                for a in g.find_all("a"):
                    gn = a.get_text()
                    sleep(1)
                    bicho = requests.get("""https://www.genome.jp/dbget-bin/www_bget?gn:%s""" % gn)
                    
                    listaOrganismos[organismo]["existe"] = 1
                    listaOrganismos[organismo]["patogeno"] = ""
                    listaOrganismos[organismo]["keywords"] = ""
                    listaOrganismos[organismo]["comment"] = ""
                    listaOrganismos[organismo]["title"] = ""
                    listaOrganismos[organismo]["keggtaxon"] = ""

                    if bicho.status_code == 200:
                        soup = bs(bicho.content, features="html.parser")
                        doenca = soup.find_all("tr")

                        for d in doenca:

                            if d.find_all("th"):
                                conteudo = d.find_all("th")[0].get_text().strip()
                                if conteudo == "Taxonomy":
                                    listaOrganismos[organismo]["keggtaxon"] = d.find_all("td")[0].get_text().strip().replace("TAX:", "")
                                if conteudo == "Keywords":
                                    listaOrganismos[organismo]["keywords"] = d.find_all("td")[0].get_text().strip()
                                if conteudo == "Disease":
                                    listaOrganismos[organismo]["patogeno"] = d.find_all("td")[0].get_text().strip()
                                if conteudo == "Comment":
                                    listaOrganismos[organismo]["comment"] = d.find_all("td")[0].get_text().strip()
                                if conteudo == "Title":
                                    listaOrganismos[organismo]["title"] = d.find_all("td")[0].get_text().strip()
                    
                    csv_novo = open("fig3-patogeno-kegg.csv", "a")
                    csv_novo.write(str(listaOrganismos[organismo]['entry']) + ";" + str(listaOrganismos[organismo]["taxonID"]) + ";" + str(listaOrganismos[organismo]["especie"]) + ";" + str(listaOrganismos[organismo]["filo"]) + ";" + str(listaOrganismos[organismo]["patogeno"]) + ";" + str(listaOrganismos[organismo]["saf"]) + ";" + str(listaOrganismos[organismo]["comment"]) + ";" + str(listaOrganismos[organismo]["title"]) + ";" + str(listaOrganismos[organismo]["existe"]) + ";" + str(listaOrganismos[organismo]["keywords"]) + ";"  + str(listaOrganismos[organismo]["keggtaxon"]) + ";")
                    csv_novo.write("\n")
                    csv_novo.close()
    except:
        pass