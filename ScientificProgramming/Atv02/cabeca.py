import os
import time
from copy import deepcopy
from typing import List
# 3rd Party
import numpy as np
# Local
import celulas
from render import Color
from virus import Virus

class Cabeca:
    LARGURA = 60
    ALTURA = 30

    def __init__(self) -> None:
        self.mapa = [[Color.WHITE for _ in range(Cabeca.LARGURA)] for _ in range(Cabeca.ALTURA)]
        self._celulas:List[celulas.Celulas] = []
        self._leucocitos:List[celulas.Leucocitos] = []
        self._virus:List[Virus] = []
        self._inicializa_celulas()
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
    
    def _cria_olho(self) -> None:
        xmin = 7; xmax = 12
        ymin = 2; ymax = 6
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self._celulas.append(celulas.CelulasOculares(x, y))
                self._celulas.append(celulas.CelulasOculares(Cabeca.LARGURA-x, y))
    def _cria_boca(self) -> None:
        pass
    def _cria_nariz(self) -> None:
        xmin = 7; xmax = 12
        ymin = 2; ymax = 6
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self._celulas.append(celulas.CelulasNasais(x, y))
    def _gera_leucocitos(self) -> None:
        pass