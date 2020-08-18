from Bio import SeqIO

fasta = SeqIO.parse("figura4/fig4-all.fasta", "fasta")

seqs = {}


for f in fasta:
    seqs[str(f.description)] = str(f.seq)


saida = open("figura4/fig4-all-unique.fasta", "w")

for s in seqs:
    saida.write( f">{s}\n{seqs[s]}\n" )

saida.close()