from time import sleep

from cabeca import Cabeca

ITERATION_DELAY = 0.4

# === INICIALIZACOES === #
cabeca = Cabeca()
for i in range(100):
    cabeca.desenhaCabeca()
    cabeca.atualiza()
    # sleep(ITERATION_DELAY)