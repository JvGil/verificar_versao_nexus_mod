import logging


def setup_logging():
    """Configura o registro global da aplicação.

    Utiliza um formato simples apenas com a mensagem (sem timestamps nem nível) para manter a saída do console limpa.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )


def log_error(exc: Exception | str) -> None:
    """Registra uma exceção ou mensagem de erro, incluindo o traceback quando aplicável."""
    if isinstance(exc, Exception):
        logging.exception("Ocorreu um erro: %s", exc)
    else:
        logging.error(str(exc))
