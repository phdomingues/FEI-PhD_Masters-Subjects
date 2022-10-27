import os
import time
from copy import deepcopy
from typing import List
# 3rd Party
import numpy as np
# Local
import celulas
import virus
from render import Color

class Cabeca:
    LARGURA = 60
    ALTURA = 30

    def __init__(self) -> None:
        self.mapa = [[Color.WHITE for _ in range(Cabeca.LARGURA)] for _ in range(Cabeca.ALTURA)]
        self._celulas:List[celulas.Celulas] = []
        self._leucocitos:List[celulas.Leucocitos] = []
        self._virus:List[virus.Virus] = []
        self._inicializa_celulas()
        self._inicializa_virus()
        self._atualiza()

    def _atualiza(self) -> None:
        novo_mapa = deepcopy(self.mapa)
        self._atualiza_celulas()
        self._atualiza_virus()
        self._atualiza_leucocitos()
    
    def _atualiza_celulas(self) -> None:
        for celula in self._celulas:
            self.mapa[celula.y][celula.x] = celula.cor
    def _atualiza_virus(self) -> None:
        for virus in self._virus:
            virus.mover()
            self.mapa[virus.y][virus.x] = virus.cor
    def _atualiza_leucocitos(self) -> None:
        for leucocito in self._leucocitos:
            leucocito.mover()
            self.mapa[leucocito.y][leucocito.x] = leucocito.cor

    def desenhaCabeca(self) -> None:
        os.system('cls') # Clear output
        map2colors = np.vectorize(Color.color2ascii)
        mapa_cores = map2colors(self.mapa)
        for row in mapa_cores:
            for value in row:
                print(value+' ', end='')
            print(Color.color2ascii(Color.END_COLOR))
            time.sleep(1e-5)

    def _inicializa_celulas(self) -> None:
        self._cria_olho()
        self._cria_boca()
        self._cria_nariz()
        self._gera_leucocitos()
    
    def _inicializa_virus(self) -> None:
        xmin = 0; xmax = Cabeca.LARGURA
        ymin = 0; ymax = Cabeca.ALTURA
        n_virus = 5
        for _ in range(n_virus):
            self._virus.append(
                virus.Influenza(
                    np.random.randint(xmin, xmax),
                    np.random.randint(ymin, ymax)
                )
            )
    
    def _cria_olho(self) -> None:
        xmin = 7; xmax = 12
        ymin = 2; ymax = 6
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self._celulas.append(celulas.CelulasOculares(x, y))
                self._celulas.append(celulas.CelulasOculares(Cabeca.LARGURA-x, y))
    def _cria_boca(self) -> None:
        xmin = 20; xmax = 40
        ymin = 22; ymax = 24
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self._celulas.append(celulas.CelulasBoca(x, y))
    def _cria_nariz(self) -> None:
        xmin = 28; xmax = 32
        ymin = 12; ymax = 15
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self._celulas.append(celulas.CelulasNasais(x, y))
    def _gera_leucocitos(self) -> None:
        xmin = 0; xmax = Cabeca.LARGURA
        ymin = 0; ymax = Cabeca.ALTURA
        n_leucocitos = 10
        for _ in range(n_leucocitos):
            self._leucocitos.append(
                celulas.Leucocitos(
                    np.random.randint(xmin, xmax),
                    np.random.randint(ymin, ymax)
                )
            )
            