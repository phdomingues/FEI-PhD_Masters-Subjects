# Std. lib
from itertools import product
from typing import List, Tuple

class No:
    def __init__(self,jogo):
        self.jogo = jogo.copy()
        self.nos_filhos = []

class Arvore:
    def __init__(self, jogo:object) -> None:
        self.raiz = No(jogo)
        self.nota = None
class IA:
    def __init__(self,jogo:object) -> None:
        self.jogo = jogo
        self.arvore = Arvore(jogo)
    def treina(self):
        self._constroi_arvore(self.arvore.raiz)
    def _constroi_arvore(self, no:No) -> None:
        # Constroi a arvore
        for jogada in self._gera_jogadas_validas(no.jogo.tabuleiro):
            novo_no = No(no.jogo)
            novo_no.jogo.jogar(*jogada)
            no.nos_filhos.append(novo_no)
            self._constroi_arvore(novo_no)
        pass
    def _gera_jogadas_validas(self, tabuleiro) -> List[Tuple[int]]:
        jogadas = []
        for coordenadas in product(range(len(tabuleiro)), repeat=len(tabuleiro)):
            if tabuleiro[coordenadas] < 2:
                continue # Ja tem um X ou O nessa posicao do tabuleiro
            jogadas.append(coordenadas)
        return jogadas
            
