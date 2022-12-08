from __future__ import annotations
from enum import Enum, auto
from typing import Tuple
import numpy as np

class Status(Enum):
    EM_ANDAMENTO = auto()
    EMPATE = auto()
    FINALIZADO = auto()

class Jogo:
    def __init__(self, tamanho:int=3):
        self.celulas = ['X', 'O', '-']
        self.jogador = 0
        self.tamanho = tamanho
        self.reinicia_tabuleiro()
        
    def reinicia_tabuleiro(self):
        self.tabuleiro = np.ones((self.tamanho,self.tamanho,self.tamanho), dtype=int)*2
        self.tabuleiro[0][0][0] = 2
        
    def exibir_tabuleiro(self) -> None:
        for plano in self.tabuleiro:
            for i, linha in enumerate(plano):
                celulas = [self.celulas[celula] for celula in linha]
                print('|'.join(celulas))
                if i < self.tamanho-1:
                    print('+'.join(['-' for _ in range(self.tamanho)]))
            print()
    
    def jogar(self, plano, linha, coluna):
        if any([value >= self.tamanho or value < 0 for value in [plano,linha,coluna]]):
            raise ValueError('A celula selecionada é invalida')
        if self.tabuleiro[plano][linha][coluna] != 2:
            raise RuntimeError(
                f"Jogada invalida, celula {plano}|{linha}|{coluna} já ocupada pelo jogador '{self.celulas[self.tabuleiro[plano][linha][coluna]]}'")
        # Aplica a jogada
        self.tabuleiro[plano][linha][coluna] = self.jogador
        # Verifica vitoria
        status = self.verifica_status_jogo((plano,linha,coluna))
        if status == Status.EMPATE:
            print(f"Jogo finalizado... Empate")
        elif status == Status.FINALIZADO:
            print(f"Jogo finalizado... Vitoria do jogador '{self.celulas[self.jogador]}'!")
        # else:
        #     # Alterna o jogador
        #     self.jogador = (self.jogador+1)%2
    
    def verifica_status_jogo(self, ultima_jogada:Tuple[int]) -> Status:
        # Vitoria na ultima jogada
        if self.verifica_vitoria(ultima_jogada):
            return Status.FINALIZADO
        # Jogo finalizado (nenhum espaco livre para jogadas)
        if len(np.where(self.tabuleiro.flatten()==2)[0]) == 0:
            return Status.EMPATE
        # Jogo ainda tem jogadas para serem feitas
        return Status.EM_ANDAMENTO
    
    def verifica_vitoria(self, jogada:Tuple[int]) -> bool:
        jp, jl, jc = jogada
        jogador = self.tabuleiro[jp][jl][jc]
        # Vitoria no mesmo plano
        vitoria = False
        # Variavel auxiliar (Matriz de indices)
        # indice indexado como: [<indice Linha/indice Coluna da matriz>, <linha da matriz>, <coluna da matriz>]
        superficie_idxs = np.indices((self.tamanho,self.tamanho)) # Matriz com os indices (i,j) de todos os elementos
        # Funcao que verifica se houve pontuacao
        pontuou = lambda jogador, superficie, filtro: sum(superficie[filtro] == jogador) == self.tamanho
        # [1] Superficie do mesmo plano
        superficie = self.tabuleiro[jp,:,:]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:] == superficie_idxs[0,:,:][jl,jc]) # Mesma linha na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[1,:,:] == superficie_idxs[1,:,:][jl,jc]) # Mesma coluna na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jl,jc]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jl,jc]) # Mesma diagonal (direita p/ esquerda) na superficie
        # [2] Superficie da mesma linha (nao precisa confirmar a linha, coincide com a linha no plano)
        superficie = self.tabuleiro[:,jl,:]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[1,:,:] == superficie_idxs[1,:,:][jp,jc]) # Mesma coluna na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp,jc]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp,jc]) # Mesma diagonal (direita p/ esquerda) na superficie
        # [3] Superficie de mesma coluna (nao precisa confirmar coluna, coincide com coluna do [2]) (nao precisa confirmar a linha, coincide com linha do [1]) 
        superficie = self.tabuleiro[:,:,jc]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp,jl]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp,jl]) # Mesma diagonal (direita p/ esquerda) na superficie
        # Corte Diagonal do cubo
        superficie_idxs = np.indices((self.tamanho,self.tamanho, self.tamanho))
        filtro = (superficie_idxs[1,:,:,:] + superficie_idxs[2,:,:,:]) == (superficie_idxs[1,:,:,:]+superficie_idxs[2,:,:,:])[jp,jl,jc]
        return vitoria
        
jogo = Jogo(tamanho=3)
jogo.jogar(0,2,0)
jogo.jogar(1,2,1)
jogo.jogar(2,2,2)
jogo.exibir_tabuleiro()