import logging
import re

from app.processing import processor


def test_logs_nao_exibem_data_ou_nivel(caplog):
    caplog.set_level("INFO")
    mods = [{"nome": "UE4SS", "mod_id": 1, "versao_online": "3.0.1", "versao_local": "3.0.0"}]

    processor.retornar_mensagem(mods, "clairobscurexpedition33")

    # Garantir que nenhuma das mensagens capturadas comece com um prefixo semelhante a data ou contenha ' - INFO -'
    for rec in caplog.records:
        assert not re.match(r"^\d{4}-\d{2}-\d{2}", rec.message)
        assert " - INFO -" not in rec.message

    # Verificar também que ao menos um registro contenha a mensagem humana (sanity)
    assert any("Nome:" in rec.message for rec in caplog.records)
