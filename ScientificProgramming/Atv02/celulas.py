# Std Lib
from datetime import datetime
from random import sample,randint
# Local
import cabeca
from render import Color

class Celulas:
    """
    Classe base para qualquer tipo de celula a ser simulada, estatica ou dinamica.
        
    O atributo _cor deve ser declarado nas subclasses de forma estatica, e caso não seja, 
    Color.UNKNOWN sera interpretado por padrao.
    """
    _cor = Color.UNKNOWN
    def __init__(self, x:int, y:int) -> None:
        # Aproveitamos os setters para atribuir os valores, ja criando os 
        # atributos privados (_ na frente) e fazer as validacoes necessarias
        self.x = x
        self.y = y
    # === GETTERS === #
    @property
    def x(self) -> int:
        return self._x
    @property
    def y(self) -> int:
        return self._y
    @classmethod
    @property
    def cor(cls) -> Color:
        return cls._cor
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
    _cor = Color.RED # Declara cor como um atributo estatico
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)

class Leucocitos(Celulas):
    _cor = Color.YELLOW # Declara cor como um atributo estatico
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)
        self._velocidade = 1
    
    def mover(self) -> None:
        movimento = sample([-1,1], 1)[0]*self._velocidade
        if randint(0,1):
            self.x += movimento
        else:
            self.y += movimento 

class CelulasOculares(Celulas):
    _cor = Color.GREEN # Declara cor como um atributo estatico
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)

class CelulasNasais(Celulas):
    _cor = Color.PURPLE # Declara cor como um atributo estatico
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)