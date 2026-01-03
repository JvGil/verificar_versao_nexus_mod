import pytest

from app.processing import processor


def test_obter_nome_versao_prefers_tag():
    mod = {"name": "UE4SS", "mod_id": 1, "tag_name": "v3.0.1", "version": "3.0.0"}
    res = processor.obter_nome_versao(mod, "v3.0.1")
    assert res["versao_online"] == "v3.0.1"
    assert res["tag_name"] == "v3.0.1"


def test_obter_nome_versao_falls_back_to_version():
    mod = {"name": "Foo", "mod_id": 2, "version": "1.2.3"}
    res = processor.obter_nome_versao(mod, "1.0.0")
    assert res["versao_online"] == "1.2.3"


def test_atualizar_versao_moasg():
    arquivos = [
        {"new_file_name": "MOASG_AllinOne-5513-1-2-3-456.zip"},
        {"new_file_name": "other.zip"},
    ]
    mod = {"versao_online": "1.8.1v"}
    updated = processor.atualizar_versao_moasg(arquivos, mod)
    assert updated["versao_online"] == "1.2.3"


def test_verificar_versao_mod_uess(monkeypatch):
    received = {"nome": "UE4SS", "mod_id": 1, "versao_online": "v3.0.0"}

    class DummyClient:
        def chamar_endpoint(self, endpoint, urls_params=None, use_github=False):
            return {"tag_name": "v3.0.1"}

    monkeypatch.setattr(processor.client, "APIClient", lambda: DummyClient())

    res = processor.verificar_versao_mod_uess(received)
    assert res is not None
    assert res["tag_name"] == "v3.0.1"
    assert res["versao_online"] == "v3.0.1"


def test_retornar_mensagem_ue4ss_link(caplog):
    caplog.set_level("INFO")
    mods = [{"nome": "UE4SS", "mod_id": 1, "versao_online": "v3.0.1", "versao_local": "3.0.0"}]

    processor.retornar_mensagem(mods, "clairobscurexpedition33")

    # Ensure GitHub releases link for UE4SS is logged
    assert any("https://github.com/UE4SS-RE/RE-UE4SS/releases" in rec.message for rec in caplog.records)


def test_retornar_mensagem_multiline(caplog):
    caplog.set_level("INFO")
    mods = [{"nome": "UE4SS", "mod_id": 1, "versao_online": "3.0.1", "versao_local": "3.0.0"}]

    processor.retornar_mensagem(mods, "clairobscurexpedition33")

    # Ensure at least one log record contains multiple lines (newline char)
    assert any('\n' in rec.message for rec in caplog.records), "Expected multiline message in logs"