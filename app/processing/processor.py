import logging
import re
from typing import Any, Dict, List, Optional

from ..api import client, endpoints
from ..api.parametros import JOGOS
from ..config import PATH_JOGO

# Constantes para tratamento especial
MOASG_MOD_ID = 5513
UE4SS_MOD_ID = 1


def obter_nome_versao(mod: Dict[str, Any], versao: str) -> Dict[str, Any]:
    """Normaliza os metadados do mod em um dict padrão.

    Prefere a release do GitHub `tag_name` ao `version` do Nexus quando disponível.
    """
    if not isinstance(mod, dict):
        logging.error("Esperado um dicionário de mod, recebido %s", type(mod))
        raise TypeError("mod must be a dict")

    tag = mod.get("tag_name")
    version = mod.get("version")
    versao_online = tag if tag is not None else version
    versao_local = versao

    result: Dict[str, Any] = {
        "nome": mod.get("name"),
        "mod_id": mod.get("mod_id"),
        "versao_online": versao_online,
        "versao_local": versao_local,
    }

    if tag is not None:
        result["tag_name"] = tag

    return result


def executar_processamento(nome_jogo: str) -> List[Dict[str, Any]]:
    """Executa o processamento para todos os mods configurados para o jogo fornecido."""
    mods: List[Dict[str, Any]] = []
    lista_mods = JOGOS.get(nome_jogo, {})
    for mod_id, versao in lista_mods.items():
        mod = processar_mod(nome_jogo, mod_id, versao)
        if mod:
            mods.append(mod)
    return mods


def processar_mod(nome_jogo: str, mod_id: int, versao: str) -> Optional[Dict[str, Any]]:
    """Processa um mod: obtém dados remotos, normaliza e compara versões."""
    cliente = client.APIClient()
    get_mod = endpoints.ENDPOINTS["get_mod"]
    list_files = endpoints.ENDPOINTS["list_files"]
    param = {
        "nome_jogo": nome_jogo,
        "mod_id": mod_id,
    }

    try:
        mod_online = cliente.chamar_endpoint(get_mod, param)
    except Exception as exc:
        logging.exception("Erro ao buscar mod %s/%s: %s", nome_jogo, mod_id, exc)
        return None

    mod_processado = obter_nome_versao(mod_online, versao)

    # Tratamento especial para MOASG em Elden Ring
    if nome_jogo == "eldenring" and mod_id == MOASG_MOD_ID:
        try:
            arquivos = cliente.chamar_endpoint(list_files, param)
            mod_processado = atualizar_versao_moasg(arquivos.get("file_updates", []), mod_processado)
        except Exception:
            logging.exception("Erro ao buscar arquivos para mod %s/%s", nome_jogo, mod_id)

    # Special handling for UE4SS (GitHub release)
    if nome_jogo == "clairobscurexpedition33" and mod_id == UE4SS_MOD_ID:
        verificar_versao_mod_uess(mod_processado)

    return comparar_versao(mod_processado)


def comparar_versao(mod_online: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return mod_online when versions differ, otherwise None."""
    try:
        assert mod_online["versao_online"] == mod_online["versao_local"]
    except AssertionError:
        return mod_online
    return None


def atualizar_versao_moasg(lista_arquivos: List[Dict[str, Any]], mod: Dict[str, Any]) -> Dict[str, Any]:
    """Extrai a versão do MOASG a partir dos nomes de arquivo e atualiza o dict do mod.

    Padrão esperado de nome de arquivo: MOASG_AllinOne-5513-<version>-<build>.zip
    """
    nome_versao = "MOASG_AllinOne-5513-"
    try:
        nome_arquivo = next(
            arquivo["new_file_name"] for arquivo in lista_arquivos if
            arquivo["new_file_name"].startswith(nome_versao)
        )
    except StopIteration:
        logging.warning("Nenhum arquivo de MOASG encontrado na lista")
        return mod

    versao_match = re.search(r"-(\d+(?:-\d+)*)-\d+\.zip$", nome_arquivo)
    if versao_match:
        mod["versao_online"] = versao_match.group(1).replace("-", ".").replace("5513.", "")
    else:
        logging.warning("Padrão de versão não encontrado no arquivo: %s", nome_arquivo)

    return mod

def verificar_versao_mod_uess(mod_online: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Obtém a última release do GitHub para UE4SS e atualiza o dict do mod fornecido com 'tag_name'."""
    param = {
        "owner": "UE4SS-RE",
        "repo": "RE-UE4SS",
    }
    cliente = client.APIClient()
    release = cliente.chamar_endpoint(endpoints.ENDPOINTS["get_latest_release"], param, use_github=True)

    tag = release.get("tag_name") if isinstance(release, dict) else None
    if tag:
        logging.info("Encontrado última release do UE4SS tag: %s", tag)
        mod_online["tag_name"] = tag
        mod_online["versao_online"] = tag
        return mod_online

    logging.warning("Não foi possível obter tag do GitHub para UE4SS")
    return None


def retornar_mensagem(mods: List[Dict[str, Any]], nome_jogo: str) -> None:
    if mods:
        logging.info("Existem %d mods desatualizados. Os seguintes mods estão desatualizados:", len(mods))
        logging.info('-' * 79)
        for mod in mods:
            if mod.get('mod_id') == UE4SS_MOD_ID:
                # UE4SS está hospedado no GitHub; indicar a página de releases
                url = "https://github.com/UE4SS-RE/RE-UE4SS/releases"
            else:
                url_complemento = f"{mod['mod_id']}?tab=files"
                url = f"https://www.nexusmods.com/{nome_jogo}/mods/{url_complemento}"

            message = (
                f"Nome: {mod.get('nome')} - {mod.get('mod_id')}\n"
                f"Versão Online: {mod.get('versao_online')}\n"
                f"Versão Local:  {mod.get('versao_local')}\n"
                f"URL:           {url}"
            )
            logging.info(message)
            logging.info('-' * 79)
        caminho_jogo = PATH_JOGO.get(nome_jogo)
        if caminho_jogo:
            caminho_jogo = caminho_jogo.replace('\\', '/')  # troca barras invertidas por barras normais
            caminho_codificado = re.sub(r' ', '%20', caminho_jogo)  # apenas espaços codificados
            logging.info('file:///%s', caminho_codificado)
    else:
        logging.info("Todos os mods estão atualizados")
