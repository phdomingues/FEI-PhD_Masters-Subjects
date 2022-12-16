# Std. lib
import _pickle as pickle
import random
from datetime import datetime
from itertools import product
from typing import List, Tuple
from pathlib import Path
# 3rd. party
import numpy as np
# Local
from jogo import Jogo

class No:
    def __init__(self,tabuleiro):
        self.tabuleiro = tabuleiro.copy()
        self.filhos = []
        self.score = None
        self.melhor_movimento = None
        self.hash = None

class Arvore:
    def __init__(self, tabuleiro:object) -> None:
        self.raiz = No(tabuleiro)
        self.hashes_referencia = {}
class IA:
    def __init__(self,profundidade_maxima:int=3) -> None:
        # self.arvore = Arvore(jogo.tabuleiro)
        self.mapa_score = {
            Jogo.Status.EMPATE: 0,
            Jogo.Status.VITORIA_X: 1,
            Jogo.Status.VITORIA_O: -1
        }
        self.profundidade_maxima = profundidade_maxima
    def jogar(self, jogo):
        arvore = Arvore(jogo.tabuleiro)
        self._constroi_arvore(arvore.raiz,0,arvore.hashes_referencia)
        jogada = self.jogada(arvore.raiz.tabuleiro, arvore.raiz.filhos[arvore.raiz.melhor_movimento].tabuleiro)
        jogo.jogar(*jogada)
    def jogada(self, tab1, tab2):
        tamanho = len(tab1)
        jogada = np.indices((tamanho,tamanho,tamanho))[:,(tab1!=tab2)].flatten()
        return tuple(jogada)
    def _hash_no(self, no:No) -> int:
        return hash(tuple(no.tabuleiro.flatten()))
    def _constroi_arvore(self, no:No, nr:int,hashes_referencia:dict) -> None:
        if nr > self.profundidade_maxima:
            return 0
        # Constroi a arvore
        for jogada in self._gera_jogadas_validas(no.tabuleiro):
            try: # Se a jogada ja foi feita antes, simplesmente volte o score dela
                return hashes_referencia[self._hash_no(no)].score
            except KeyError: # Caso contrario precisamos computar
                novo_no = No(no.tabuleiro)
                novo_no.jogada = jogada
            try:
                novo_no.tabuleiro = Jogo.simular_jogada(*jogada,novo_no.tabuleiro)
                score = self._constroi_arvore(novo_no,nr+1,hashes_referencia)
            except Jogo.JogoFinalizado as jf:
                score = self.mapa_score[jf.status]
            novo_no.score = score # Salva score do No
            novo_no.hash = self._hash_no(novo_no) # Salva hash do No
            no.filhos.append(novo_no) # Aponta para o No filho no No pai
        # Gera um vetor com os scores dos nos filhos, para facilitar o tratamento
        score_filhos = [filho.score for filho in no.filhos]
        # Descobre se deve maximizar ou minimizar o score
        f = max if Jogo.celulas[Jogo.proximo_jogador(no.tabuleiro)] == 'X' else min
        # Encontra o filho que produz o melhor resultado (caso mais de um produzam o mesmo score, sorteia um aleatoriamente)
        no.melhor_movimento = random.sample([i for i, scr in enumerate(score_filhos) if scr==f(score_filhos)], 1)[0]
        # Gera e salva a hash desta jogada
        no.hash = hash(tuple(no.tabuleiro.flatten()))
        # Salva o No na lista de nos conhecidos
        hashes_referencia[no.hash] = no
        # Calcula e retorna o score do No atual (soma dos scores dos filhos)
        return sum(score_filhos)
    def _gera_jogadas_validas(self, tabuleiro) -> List[Tuple[int]]:
        jogadas = []
        for coordenadas in product(range(len(tabuleiro)), repeat=len(tabuleiro)):
            if tabuleiro[coordenadas] < 2:
                continue # Ja tem um X ou O nessa posicao do tabuleiro
            jogadas.append(coordenadas)
        return jogadas
            
