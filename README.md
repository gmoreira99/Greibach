Forma Normal de Greibach

Guilherme Moreira de Carvalho;
Linguagens Formais e Autômatos - T01 (2022.1);
Prof. Andrei Rimsa Álvares, DECOM - CEFET MG.

Transforma a gramática G para uma linguagem L -
- sem regras # (lambda), exceto quanto # pertence à L,
sem regras unitárias e sem variáveis inúteis -
em uma GLC G' equivalente na forma normal de Greibach.

Cada variável é formada por uma letra maiúscula -
o alfabeto de símbolos não pode conter letras maiúsculas -
A grámatica G deve ser passada como parâmetro
em uma representação em formato JSON.

A -> CB		{ "glc": [
B -> BBD | b		  ["A","B", "C", "D"],
C -> BBC | Dc		  ["b", "c", "d"],
D -> AD | d		  [
	G		    ["A", "CB"]
			    ["B", "BBD"]
			    ["B", "b"]
			    ["C", "BBC"]
			    ["C", "Dc"]
			    ["D", "AD"]
			    ["D", "d"]
			  ],
			  "A"
			]}
				G.json
				
USE: $ ./greibach.py G.json
