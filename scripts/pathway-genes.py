# -*- coding: utf-8 -*-
# pathway_genes.py

#import urllib2
from bs4 import BeautifulSoup as bs
import sys
#import psycopg2
import requests


def main():
    args = sys.argv
    if len(args) != 2:
        print('Usage: ./pathway_genes.py PATHWAY')
        sys.exit(1)

    pathway_id = str(args[1])
    # pathway_id = 'map04068'
    

    

    orthology_ids = get_orthology_ids(pathway_id)

    print('Found {} orthology ids for pathway "{}"'\
            .format(len(orthology_ids), pathway_id))

    if not orthology_ids:
        sys.exit(1)

    for orthology_id in orthology_ids:
	#K05304 - NANS
	#K01654 - NEUB
        if orthology_id == "K18430":
            gene_ids = get_gene_ids(orthology_id)

            print('Writing {} FASTA gene sequences to "{}.fa"'\
                    .format(len(gene_ids), orthology_id))

            with open(orthology_id + '-1.fa', 'w') as out:
                for i, gene_id in enumerate(gene_ids, 1):

                    ###Inicio da firula
                    #sys.stdout.write('.')
                    #if not i % 5:
                    #    sys.stdout.write(' ')
                    #if not i % 50:
                    #    sys.stdout.write('\n')
                    #sys.stdout.flush()
                    ###fim da firula

                    fasta = get_fasta(gene_id, i)
                    out.write(fasta)

            print()

def get_ids(url):
    response = requests.get(url)
    html = response.content
    b = bs(html)
    links = b.find_all('a')
    valid_link = lambda x: 'www_bget' in x.get('href')
    links = filter(valid_link, links)
    return [link.text for link in links]

def get_orthology_ids(pathway_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+orthology+path:'
    return get_ids(URL + FUN + pathway_id)

def get_gene_ids(orthology_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+genes+ko:'
    return get_ids(URL + FUN + orthology_id)

def get_fasta(gene_id, indice):
    URL = 'http://www.genome.jp'
    #?-f+-n+n+ para dna
    #?-f+-n+a+ para prot
    FUN = '/dbget-bin/www_bget?-f+-n+a+'
    response = requests.get(URL + FUN + gene_id)
    html = bs(response.content)
    #return html.pre.text
    #### Modificado ####
    gene_id = gene_id.split(":")
    page = requests.get("http://www.genome.jp/kegg-bin/show_organism?org=" + gene_id[0])
    soup = bs(page.content)
    bla = soup.find_all("tr")
    
    ##### Altera o nome no arquivo fasta #####
    html = html.pre.text
    biru = bla[9].get_text().replace("Definition", "")
    batman = bla[6].get_text().replace("Org code", "")
    robin = bla[11].get_text().replace("Taxonomy", "")
    robin = robin.replace("TAX: ", "NCBI:txid")
    acc.write(biru+";"+batman+";"+gene_id[1]+";"+robin+"; \n")
    html = html.replace(gene_id[1], biru)
    html = html.replace("K15898", gene_id[1])
    html = html.replace("K01654", gene_id[1])
    html = html.replace("K18430", gene_id[1])
    
    ##### Fim da alteração de nome

    ##### Remover indicação do gene #####
    texto = html.split("\n")
    titulo = texto[1].split(" | ")
    titulo = titulo[0].replace(" N-acetylneuraminate synthase [EC:2.5.1.56]", "")
    titulo = titulo.replace(" sialic acid synthase [EC:2.5.1.56 2.5.1.57 2.5.1.132]", "")
    titulo = titulo.replace(""" pseudaminic acid synthase [EC:2.5.1.97]""", "")
    titulo = titulo.replace(""" N,N'-diacetyllegionaminate synthase [EC:2.5.1.101]""", "")
    titulo = titulo.replace("(", "- ")
    titulo = titulo.replace(")", "")
    titulo = titulo.replace("/", "")
    titulo = titulo.replace(gene_id[1], "| " + gene_id[1])
    titulo = titulo.replace(gene_id[0], str(indice))
    i = 0
    html = ""
    for tex in texto:
        if i == 1:
            html += titulo
        elif i != 0:
            html += "\n" + tex
        i += 1
    print(titulo)

    return html

if __name__ == '__main__':
    acc = open('accc-K15898-1.csv', 'w')
    acc.write("nm_organismo;cd_org_kegg;cd_kegg;id_taxon;\n")
    main()
    #conecta_bd()
