from Bio import SeqIO

arquivo = SeqIO.parse("figura1/kegg-bacteria.fasta", "fasta")

tamanho = 0
cont = 0

for a in arquivo:
    tamanho = tamanho + len(str(a.seq))
    cont+=1

print(tamanho/cont)
print(cont)