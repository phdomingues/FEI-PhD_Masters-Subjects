import os
import platform
from time import sleep

from cabeca import Cabeca

clr_str = 'cls' if platform.system().lower() == 'windows' else 'clear'

ITERATION_DELAY = 0.1
MAX_ITER = 500

# === INICIALIZACOES === #
cabeca = Cabeca()
i = 0
while cabeca.infectada() and i < MAX_ITER:
    # Impressao de texto base e limpeza de output
    os.system(clr_str) # Clear output
    print(f"Iteracao: {i:>5}/{MAX_ITER}\n")
    # Atualiza a simulacao
    cabeca.desenhaCabeca()
    cabeca.atualiza()
    sleep(ITERATION_DELAY)
    # Atualiza iteracao
    i+=1