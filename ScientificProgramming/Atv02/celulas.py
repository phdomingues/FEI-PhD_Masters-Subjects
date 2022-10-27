# Std Lib
from datetime import datetime
from random import sample,randint
# Local
import cabeca
from render import Color

class Celulas:
    def __init__(self, x:int, y:int, cor:int) -> None:
        # Aproveitamos os setters para atribuir os valores, ja criando os 
        # atributos privados (_ na frente) e fazer as validacoes necessarias
        self.x = x
        self.y = y
        self._cor = cor
    # === GETTERS === #
    @property
    def x(self) -> int:
        return self._x
    @property
    def y(self) -> int:
        return self._y
    @property
    def cor(self) -> Color:
        return self._cor
    # === SETTERS === #
    @x.setter
    def x(self, novo_x:int) -> None:
        while novo_x < 0:
            novo_x = cabeca.Cabeca.LARGURA - novo_x
        self._x = novo_x % cabeca.Cabeca.LARGURA # Limita pela largura (quem passar da a volta)
    @y.setter
    def y(self, novo_y:int) -> None:
        while novo_y < 0:
            novo_y = cabeca.Cabeca.ALTURA - novo_y
        self._y = novo_y % cabeca.Cabeca.ALTURA # Mesmo para a altura

class CelulasBoca(Celulas):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y, Color.RED)

class Leucocitos(Celulas):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y, Color.YELLOW)
        self._velocidade = 1
    
    def mover(self) -> None:
        movimento = sample([-1,1], 1)[0]*self._velocidade
        if randint(0,1):
            self.x += movimento
        else:
            self.y += movimento 

class CelulasOculares(Celulas):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y, Color.GREEN)

class CelulasNasais(Celulas):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y, Color.PURPLE)