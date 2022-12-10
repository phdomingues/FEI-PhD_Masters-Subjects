# Std. lib
import _pickle as pickle
from datetime import datetime
from itertools import product
from typing import List, Tuple
from pathlib import Path

class No:
    def __init__(self,jogo):
        self.jogo = jogo.copy()
        self.filhos = []
        self.score = None
        self.melhor_movimento = None
        self.hash = None

class Arvore:
    def __init__(self, jogo:object) -> None:
        self.raiz = No(jogo)
        self.hashes_referencia = {}
class IA:
    def __init__(self,jogo:object, path_arvore:Path=Path(__file__).parent.absolute()/'IA') -> None:
        self.jogo = jogo
        self.arvore = Arvore(jogo)
        self.mapa_score = {
            jogo.Status.EMPATE: 0,
            jogo.Status.VITORIA_X: 1,
            jogo.Status.VITORIA_O: -1
        }
        self._path_arvore = path_arvore / f'arvore_{self.jogo.tamanho}.pkl'
        try:
            self.carregar(self._path_arvore)
        except FileNotFoundError:
            print('Arvore de decisao não encontrada')
    def salvar(self) -> None:
        self._path_arvore.parent.mkdir(parents=True, exist_ok=True)
        with self._path_arvore.open('wb') as arquivo:
            pickle.dump(self.arvore, arquivo, -1)
    def carregar(self,path:Path) -> Arvore:
        with path.open('rb') as arquivo:
            self.arvore = pickle.load(arquivo)
    def treina(self):
        self.contador = 0
        self.c2 = 0
        start = datetime.now()
        self.arvore.raiz.score = self._constroi_arvore(self.arvore.raiz)
        print(f'Arvore construida em {datetime.now()-start}')
        self.salvar()
    def _hash_no(self, no:No) -> int:
        return hash(tuple(no.jogo.tabuleiro.flatten()))
    def _constroi_arvore(self, no:No) -> None:
        self.contador = (self.contador + 1) % 100000
        if self.contador == 0:
            self.c2 += 1
            print(f"Checkpoint... Salvando arvore [{self.c2}]")
            self.salvar()
        # Constroi a arvore
        for jogada in self._gera_jogadas_validas(no.jogo.tabuleiro):
            try: # Se a jogada ja foi feita antes, simplesmente volte o score dela
                return self.arvore.hashes_referencia[self._hash_no(no)].score
            except KeyError: # Caso contrario precisamos computar
                novo_no = No(no.jogo)
            try:
                novo_no.jogo.jogar(*jogada)
                score = self._constroi_arvore(novo_no)
            except no.jogo.JogoFinalizado as jf:
                score = self.mapa_score[jf.status]
            novo_no.score = score # Salva score do No
            novo_no.hash = self._hash_no(novo_no) # Salva hash do No
            no.filhos.append(novo_no) # Aponta para o No filho no No pai
        # Gera um vetor com os scores dos nos filhos, para facilitar o tratamento
        score_filhos = [filho.score for filho in no.filhos]
        # Descobre se deve maximizar ou minimizar o score
        f = max if no.jogo.celulas[no.jogo.jogador] == 'X' else min
        # Encontra o filho que produz o melhor resultado
        no.melhor_movimento = score_filhos.index(f(score_filhos))
        # Gera e salva a hash desta jogada
        no.hash = hash(tuple(no.jogo.tabuleiro.flatten()))
        # Salva o No na lista de nos conhecidos
        self.arvore.hashes_referencia[novo_no.hash] = novo_no
        # Calcula e retorna o score do No atual (soma dos scores dos filhos)
        return sum(score_filhos)
    def _gera_jogadas_validas(self, tabuleiro) -> List[Tuple[int]]:
        jogadas = []
        for coordenadas in product(range(len(tabuleiro)), repeat=len(tabuleiro)):
            if tabuleiro[coordenadas] < 2:
                continue # Ja tem um X ou O nessa posicao do tabuleiro
            jogadas.append(coordenadas)
        return jogadas
            
