#!/usr/bin/python3

# Guilherme Moreira de Carvalho, 2022.1
# Transformação de uma gramática G em uma GLC G' equivalente na forma normal de Greibach

import sys
import re
import json
import string as alfabeto_pt

# Função Diferecenca - retorna elementos que pertencem a lst1
# mas nao pertecem a lst2
def Diff(lst1, lst2):
    return list(set(lst1) - set(lst2))

# Função Intersecção - retorna os elementos comuns a lst1 e a lst2
def intersection(lst1, lst2):
	return list(set(lst1) & set(lst2))

# Funcao Proxima Variavel - retorna um simbolo maiusculo disponivel do alfabeto
def getNextVAR(lst):
    lst = Diff(alfabeto_pt.ascii_uppercase, lst)
    lst.sort()
    return lst[0]
    
if __name__ == "__main__":
	# verifica a passagem de um parametro valido
	n = len(sys.argv)
	if (n != 2 or not(re.match(".*json", sys.argv[1]))):
		print("Use:", sys.argv[0], "[JSON]")
		sys.exit(1)

	# abertura do json
	with open(sys.argv[1], 'r') as G:
		glc = json.load(G)
	G.close()
	
	VAR = glc["glc"][0]		# Variaveis iniciais
	sym = glc["glc"][1]		# Terminais iniciais
	REGRAS = glc["glc"][2]		# Regras iniciais
	PARTIDA = glc["glc"][3]	# Variavel de partida
	
	if (Diff(VAR, alfabeto_pt.ascii_uppercase) != []):
		raise Exception("CADA VARIAVEL DEVE SER UMA UNICA LETRA MAIUSCULA")
		
	if (intersection(sym, alfabeto_pt.ascii_uppercase) != []):
		raise Exception("O ALFABETO DE SIMBOLOS NAO PODE CONTER LETRAS MAIUSCULAS")
	
	# para cada regra, substitui Terminais a partir da segunda posição por novas Variaveis
	# gerando novas regras ou aproveitando uma já existente
	for RE_VAR in REGRAS:
		for i, x in enumerate(RE_VAR[1][1:], 1):
			if (x in sym):
				new = True # supõe que gerou nova regra
				for RE_sym in reversed(REGRAS):
					if (RE_sym[1] == x):
						aux = list(RE_VAR[1])
						aux[i] = RE_sym[0]
						RE_VAR[1] = ''.join(aux)
						new = False # regra já existia
						break
				if (new):
					V = getNextVAR(VAR)
					VAR.append(V)
					REGRAS.append([V, x])
					aux = list(RE_VAR[1])
					aux[i] = V
					RE_VAR[1] = ''.join(aux)

	# coloca a Variavel de Partida no topo
	VAR.remove(PARTIDA[0])
	VAR.insert(0, PARTIDA[0])
	
	n = len(VAR) # quantidade instantânea de Variaveis
	
	while(True): # enquanto houver trocas do tipo #A > #B
		# resolve recursões à esquerda
		for i, RE_VAR in enumerate(REGRAS):
			if (RE_VAR[0] == RE_VAR[1][0]):
				V = getNextVAR(VAR)
				VAR.append(V)
				skip = False # regra seguinte é inicial
				for j, RE_sym in enumerate(REGRAS):
					if (RE_sym[0] == RE_VAR[0]):
						if (RE_sym[1][0] == RE_VAR[0] or skip):
							skip = False
							continue
						else:
							REGRAS.insert(j+1, [RE_VAR[0], RE_sym[1]+V])
							skip = True # regra seguinte é uma correção
				REGRAS.append([V, RE_VAR[1][1:]])
				REGRAS.append([V, RE_VAR[1][1:]+V])
				REGRAS.remove(RE_VAR)
		done = True # supõe que não ha mais trocas do tipo #A > #B
		while(True): # enquanto não realiza uma troca do tipo #A > #B
			alt = False # supõe que não houve uma troca
			# resolve #A > #B
			for i, RE_VAR in enumerate(REGRAS):
				if (VAR.index(RE_VAR[0]) < n):
					if (RE_VAR[1][0] in VAR and VAR.index(RE_VAR[0]) > VAR.index(RE_VAR[1][0])):
						for RE_sym in REGRAS:
							if (RE_sym[0] == RE_VAR[1][0]):
								aux = list(RE_VAR[1][1:])
								aux.insert(0, RE_sym[1])
								aux = ''.join(aux)
								REGRAS.insert(i+1, [RE_VAR[0], aux])
						REGRAS.pop(i)
						alt = True
						done = False # pode criar recursão à esquerda
			if (not(alt)):
				break
		if (done):
			break

	while(True): # analogo ao anterior, porem ordem das regras é invertida
		alt = False
		# resolve #A > #B
		for i, RE_VAR in enumerate(reversed(REGRAS)):
			if (VAR.index(RE_VAR[0]) < n): # ignora regras criadas pela recursão à esquerda
				if (RE_VAR[1][0] in VAR):
					for RE_sym in reversed(REGRAS):
						if (RE_sym[0] == RE_VAR[1][0]):
							aux = list(RE_VAR[1][1:])
							aux.insert(0, RE_sym[1])
							aux = ''.join(aux)
							REGRAS.insert(i, [RE_VAR[0], aux])
					REGRAS.remove(RE_VAR)
					alt = True
		if (not(alt)):
			break
			
	while(True): # analogo ao anterior, porem para regras novas
		alt = False
		# resolve #A > #B
		for i, RE_VAR in enumerate(REGRAS):
			if (VAR.index(RE_VAR[0]) >= n):
				if (RE_VAR[1][0] in VAR):
					for RE_sym in REGRAS:
						if (RE_sym[0] == RE_VAR[1][0]):
							aux = list(RE_VAR[1][1:])
							aux.insert(0, RE_sym[1])
							aux = ''.join(aux)
							REGRAS.insert(i, [RE_VAR[0], aux])
					REGRAS.remove(RE_VAR)
					alt = True
		if (not(alt)):
			break

	# organiza as regras por ordem alfabética das Variaveis
	# coloca regras da Variavel de Partida no topo
	REGRAS.sort()
	if (PARTIDA[0] != 'A'):
		for RE in REGRAS:
			if (RE[0] == PARTIDA[0]):
				aux = RE
				REGRAS.remove(RE)
				REGRAS.insert(0, aux)
	
	G = {"glc" : [VAR, sym, REGRAS, PARTIDA]}
	glc = json.dumps(G)
	print(glc)
