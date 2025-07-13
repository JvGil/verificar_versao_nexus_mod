import logging
import time

from processing.processor import retornar_mensagem, executar_processamento
from utils.utils import setup_logging, log_error


def main():
    setup_logging()
    start_time = time.time()
    logging.info("Início da execução")
    nome_jogo = 'eldenring'

    try:
        mods = executar_processamento(nome_jogo)
        retornar_mensagem(mods, nome_jogo)
    except Exception as e:
        log_error(f"Erro ao processar dados: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Fim da execução - Tempo total: {total_time:.2f} segundos")


if __name__ == "__main__":
    main()
