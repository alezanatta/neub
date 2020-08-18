from Bio import SeqIO

csv = open("figura4/K18430-hitdata.tsv", "r")
linhas = csv.readlines()
csv.close()

fasta = SeqIO.parse("figura4/K18430-bacteria.fasta", "fasta")

seq = {}
rep = []

for f in fasta:
	seq[str(f.description)] = str(f.seq)

del fasta

arquivo = open("figura4/K18430-cdsearch.fasta", "w")
acc = open("figura4/K18430-acession.txt", "w")

for linha in linhas:
	linha = linha.split("\t")
	
	if (linha[1] == "pfam03102") and (linha[2] == " - ") and str(linha[0]) not in rep:
		arquivo.write(">" + str(linha[0]) + "\n")
		arquivo.write( str( seq[str(linha[0])] )[int(linha[3])+1:int(linha[4])+1] + "\n")
		acc.write(str(linha[0]) + "\n")
		rep.append(str(linha[0]))
	

arquivo.close()
acc.close()