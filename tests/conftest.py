"""Helpers de configuração de teste.

Garante que a raiz do projeto esteja em sys.path para que os testes possam importar o pacote da aplicação
(`app`) independentemente de como o pytest é executado.
Também configura um logging simples e um hook que registra o resultado do teste após cada teste.
"""
from pathlib import Path
import sys
import logging

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Configuração básica de logging para os testes para que as mensagens de log sejam exibidas durante as execuções
# Usa um formato simples apenas com a mensagem (sem timestamps nem nível) para manter a saída do console compacta
logging.basicConfig(level=logging.INFO, format='%(message)s')


def pytest_runtest_makereport(item, call):
    """Registra o resultado do teste após a fase 'call' de cada teste.

    Este hook registra uma mensagem INFO quando um teste passa e ERROR quando ele falha.
    """
    # Agir apenas na fase 'call' (quando o corpo do teste foi executado)
    if call.when != "call":
        return

    if call.excinfo is None:
        logging.info("Teste feito com sucesso: %s", item.nodeid)
    else:
        logging.error("Teste falhou: %s", item.nodeid)
