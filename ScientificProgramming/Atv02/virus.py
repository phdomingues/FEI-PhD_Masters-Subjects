# Std. Lib
from random import randint, sample
# Local
import cabeca
from render import Color

class Virus:
    # === CONSTRUTOR === #
    def __init__(self, velocidade:int, cor:Color, x:int, y:int) -> None:
        self.duplicado = False
        self._velocidade = velocidade
        self._cor = cor
        self.x = x
        self.y = y
    # === METODOS === #
    def mover(self) -> None:
        movimento = sample([-1,1], 1)[0]*self._velocidade
        if randint(0,1):
            self.x += movimento
        else:
            self.y += movimento    
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
        self._x = novo_x % cabeca.Cabeca.LARGURA
    @y.setter
    def y(self, novo_y:int) -> None:
        while novo_y < 0:
            novo_y = cabeca.Cabeca.ALTURA - novo_y
        self._y = novo_y % cabeca.Cabeca.ALTURA

class Influenza(Virus):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(
            velocidade=1,
            cor=Color.BLUE,
            x=x,
            y=y
        )
