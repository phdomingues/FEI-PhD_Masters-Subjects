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
        self._celulas:List[celulas.Celulas] = []
        self._leucocitos:List[celulas.Leucocitos] = []
        self._virus:List[virus.Virus] = []
        self.mapa = self._reinicia_mapa()
        self._inicializa_celulas()
        self._inicializa_virus()
        self.atualiza()
        
    def _reinicia_mapa(self):
        self.mapa = [[Color.WHITE for _ in range(Cabeca.LARGURA)] for _ in range(Cabeca.ALTURA)]

    def atualiza(self) -> None:
        self._reinicia_mapa()
        self._atualiza_celulas()
        self._atualiza_virus()
        self._atualiza_leucocitos()
        self._trata_colisao()
    
    def _atualiza_celulas(self) -> None:
        for celula in self._celulas:
            self.mapa[celula.y][celula.x] = celula.cor
    def _atualiza_virus(self) -> None:
        for virus in self._virus:
            # Move o virus
            virus.mover()
            # Atualiza a cor no mapa
            self.mapa[virus.y][virus.x] = virus.cor
            
    def _atualiza_leucocitos(self) -> None:
        for leucocito in self._leucocitos:
            # Move o leucocito
            leucocito.mover()
            # Atualiza a cor no mapa
            self.mapa[leucocito.y][leucocito.x] = leucocito.cor

    def desenhaCabeca(self) -> None:
        self._imprime_dados()
        map2colors = np.vectorize(Color.color2ascii)
        mapa_cores = map2colors(self.mapa)
        for row in mapa_cores:
            for value in row:
                print(value+' ', end='')
            print(Color.color2ascii(Color.END_COLOR))

    def infectada(self):
        return len(self._virus) > 0

    def _imprime_dados(self) -> None:
        end_color = Color.color2ascii(Color.END_COLOR)
        # === Leucocitos
        l_cor = Color.color2ascii(celulas.Leucocitos.cor)
        l_vivos = len(self._leucocitos)
        l_string = f"{l_cor} {end_color} Leucocitos {l_vivos:>4}"
        # === Virus
        v_cor = Color.color2ascii(virus.Influenza.cor)
        v_vivos = len(self._virus)
        v_string = f"{v_cor} {end_color} Influenza {v_vivos:>4}"
        print(f"Status: {l_string} | {v_string}\n")

    def _inicializa_celulas(self) -> None:
        self._cria_olho()
        self._cria_boca()
        self._cria_nariz()
        self._gera_leucocitos()
    
    def _inicializa_virus(self, n_virus:int=5) -> None:
        for _ in range(n_virus):
            self._cria_influenza()

    def _cria_influenza(self) -> virus.Influenza:
        xmin = 0; xmax = Cabeca.LARGURA
        ymin = 0; ymax = Cabeca.ALTURA
        novo_virus = virus.Influenza(
            np.random.randint(xmin, xmax),
            np.random.randint(ymin, ymax)
        )
        self._virus.append(novo_virus)
        return novo_virus
    
    def _cria_leucocito(self) -> celulas.Leucocitos:
        xmin = 0; xmax = Cabeca.LARGURA
        ymin = 0; ymax = Cabeca.ALTURA
        self._leucocitos.append(
            celulas.Leucocitos(
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
    def _gera_leucocitos(self, n_leucocitos:int=10) -> None:
        for _ in range(n_leucocitos):
            self._cria_leucocito()
    
    def _trata_colisao(self) -> None:
        agora = time.time()
        for l_idx in range(len(self._leucocitos)-1,-1,-1):
            if len(self._leucocitos) > 10 and agora - self._leucocitos[l_idx].nascimento > 7:
                del self._leucocitos[l_idx]
        for v_idx in range(len(self._virus)-1,-1,-1):
            virus = self._virus[v_idx]
            virus_na_celula = any([(virus.x, virus.y) == (c.x, c.y) for c in self._celulas])
            leucocito_no_virus = any([(virus.x, virus.y) == (l.x, l.y) for l in self._leucocitos])
            if leucocito_no_virus:
                del self._virus[v_idx]
                self._cria_leucocito()
                continue
            if not virus.duplicado and virus_na_celula:
                self._cria_influenza()
            virus.duplicado = virus_na_celula