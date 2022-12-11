from __future__ import annotations
# Std. lib
from enum import Enum, auto
from typing import Tuple
# 3rd. party
import numpy as np
# Local
import inteligencia_artificial


class Jogo:
    celulas = ['X', 'O', '-']
    class Status(Enum):
        EM_ANDAMENTO = 0
        EMPATE = 1
        VITORIA_X = 2
        VITORIA_O = 3
    class JogoFinalizado(RuntimeError):
        def __init__(self, status: Jogo.Status, *args: object) -> None:
            self.status = status
            super().__init__(*args)
    
    @staticmethod
    def proximo_jogador(tabuleiro) -> int:
        return 1 if sum((tabuleiro == 0).flatten()) > sum((tabuleiro == 1).flatten()) else 0

    def __init__(self, tamanho:int=3):
        self.jogador = 0
        if tamanho < 3:
            ValueError(f"Tamanho do tabuleiro deve ser >= 3, valor {tamanho} invalido")
        self.tamanho = tamanho
        self.reinicia_tabuleiro()

    def copy(self) -> Jogo:
        copia_jogo = Jogo(self.tamanho)
        copia_jogo.tabuleiro = self.tabuleiro.copy()
        copia_jogo.jogador = self.jogador
        return copia_jogo
    
        
    def reinicia_tabuleiro(self):
        self.tabuleiro = np.ones((self.tamanho,self.tamanho,self.tamanho), dtype=int)*2

    @staticmethod
    def exibir_tabuleiro(tabuleiro) -> None:
        tamanho = len(tabuleiro)
        for plano in tabuleiro:
            for i, linha in enumerate(plano):
                celulas = [Jogo.celulas[celula] for celula in linha]
                print('|'.join(celulas))
                if i < tamanho-1:
                    print('+'.join(['-' for _ in range(tamanho)]))
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
        status = self.verifica_status_jogo((plano,linha,coluna),self.tabuleiro)
        if status in [self.Status.EMPATE, self.Status.VITORIA_O, self.Status.VITORIA_X]:
            raise self.JogoFinalizado(status)
        else:
            # Alterna o jogador
            self.jogador = (self.jogador+1)%2
    
    @staticmethod
    def simular_jogada(plano, linha, coluna, tabuleiro):
        if any([value >= len(tabuleiro) or value < 0 for value in [plano,linha,coluna]]):
            raise ValueError('A celula selecionada é invalida')
        if tabuleiro[plano][linha][coluna] != 2:
            raise RuntimeError(
                f"Jogada invalida, celula {plano}|{linha}|{coluna} já ocupada pelo jogador '{Jogo.celulas[tabuleiro[plano][linha][coluna]]}'")
        # Aplica a jogada
        tabuleiro[plano][linha][coluna] = Jogo.proximo_jogador(tabuleiro)
        # Verifica vitoria
        status = Jogo.verifica_status_jogo((plano,linha,coluna),tabuleiro)
        if status in [Jogo.Status.EMPATE, Jogo.Status.VITORIA_O, Jogo.Status.VITORIA_X]:
            raise Jogo.JogoFinalizado(status)
        return tabuleiro
    
    @staticmethod
    def verifica_status_jogo(ultima_jogada:Tuple[int], tabuleiro) -> Jogo.Status:
        # Vitoria na ultima jogada
        if Jogo.verifica_vitoria(ultima_jogada, tabuleiro):
            return Jogo.Status.VITORIA_X if Jogo.proximo_jogador(tabuleiro) == 1 else Jogo.Status.VITORIA_O
        # Jogo finalizado (nenhum espaco livre para jogadas)
        if len(np.where(tabuleiro.flatten()==2)[0]) == 0:
            return Jogo.Status.EMPATE
        # Jogo ainda tem jogadas para serem feitas
        return Jogo.Status.EM_ANDAMENTO
    
    @staticmethod
    def verifica_vitoria(jogada:Tuple[int], tabuleiro) -> bool:
        tamanho = len(tabuleiro)
        jp, jl, jc = jogada
        jogador = tabuleiro[jp][jl][jc]
        # Vitoria no mesmo plano
        vitoria = False
        # Variavel auxiliar (Matriz de indices)
        # indice indexado como: [<indice Linha/indice Coluna da matriz>, <linha da matriz>, <coluna da matriz>]
        superficie_idxs = np.indices((tamanho,tamanho)) # Matriz com os indices (i,j) de todos os elementos
        superficie_idxs_3d = np.indices((tamanho,tamanho,tamanho)) # Matriz com os indices (i,j,k) de todos os elementos
        # Funcao que verifica se houve pontuacao
        pontuou = lambda jogador, superficie, filtro: sum(superficie[filtro] == jogador) == tamanho
        # [1] Superficie do mesmo plano
        superficie = tabuleiro[jp,:,:]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:] == superficie_idxs[0,:,:][jl,jc]) # Mesma linha na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[1,:,:] == superficie_idxs[1,:,:][jl,jc]) # Mesma coluna na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jl,jc]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jl,jc]) # Mesma diagonal (direita p/ esquerda) na superficie
        # [2] Superficie da mesma linha (nao precisa confirmar a linha, coincide com a linha no plano)
        superficie = tabuleiro[:,jl,:]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[1,:,:] == superficie_idxs[1,:,:][jp,jc]) # Mesma coluna na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp,jc]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp,jc]) # Mesma diagonal (direita p/ esquerda) na superficie
        # [3] Superficie de mesma coluna (nao precisa confirmar coluna, coincide com coluna do [2]) (nao precisa confirmar a linha, coincide com linha do [1]) 
        superficie = tabuleiro[:,:,jc]
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp,jl]) # Mesma diagonal (esquerda p/ direita) na superficie
        vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp,jl]) # Mesma diagonal (direita p/ esquerda) na superficie
        # [4] Corte Diagonal 1 do cubo
        filtro = (superficie_idxs_3d[1,:,:,:] + superficie_idxs_3d[2,:,:,:]) == (superficie_idxs_3d[1,:,:,:] + superficie_idxs_3d[2,:,:,:])[jp,jl,jc] # Extrai o plano diagonal
        try:
            superficie = tabuleiro[filtro].reshape((tamanho,tamanho)) # Tenta gerar o semi-plano NxN
            vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp, jl]) # Mesma diagonal (esquerda p/ direita) na superficie
            vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp, jl]) # Mesma diagonal (direita p/ esquerda) na superficie
        except ValueError: # Caso o plano seja menor do que self.tamanho x self.tamanho
            pass # Não há possibilidade de ter feito ponto, apenas ignore
        # [5] Corte Diagonal 2 do cubo
        filtro = (superficie_idxs_3d[1,:,:,:] - superficie_idxs_3d[2,:,:,:]) == (superficie_idxs_3d[1,:,:,:] - superficie_idxs_3d[2,:,:,:])[jp,jl,jc]
        try:
            superficie = tabuleiro[filtro].reshape((tamanho,tamanho))
            vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]-superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]-superficie_idxs[1,:,:])[jp, int((jl+jc)/2)]) # Mesma diagonal (esquerda p/ direita) na superficie
            vitoria |= pontuou(jogador, superficie, superficie_idxs[0,:,:]+superficie_idxs[1,:,:] == (superficie_idxs[0,:,:]+superficie_idxs[1,:,:])[jp, int((jl+jc)/2)]) # Mesma diagonal (direita p/ esquerda) na superficie
        except ValueError:
            pass
        return vitoria

if __name__ == '__main__':
    jogo = Jogo(tamanho=3)
    ia = inteligencia_artificial.IA(profundidade_maxima = 3)
    while True:
        try:
            if jogo.jogador:
                jogada = tuple(map(int,input('Plano,linha,coluna (separado por virgula): ').split(',')))
                jogo.jogar(*jogada)
            else:
                ia.jogar(jogo)
        except Jogo.JogoFinalizado as jf:
            print(jf.status)
            break
        finally:
            jogo.exibir_tabuleiro(jogo.tabuleiro)