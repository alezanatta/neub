

entrada = open("figura3/fig3-patogeno-kegg.csv", "r")
linhas = entrada.readlines()
entrada.close()

saida = open("figura3/fig3-patogeno-kegg-limpo.csv", "w")

for linha in linhas:
    l = linha.split(";")
    if l[1] == l[-2]:
        saida.write(str(linha))

saida.close()
