import re

from api import client, endpoints
from api.parametros import JOGOS
from config import PATH_JOGO


def obter_nome_versao(mod, versao):
    return {
        "nome": mod["name"],
        "mod_id": mod["mod_id"],
        "versao_online": mod["version"],
        "versao_local": versao
    }


def executar_processamento(nome_jogo):
    mods = []
    lista_mods = JOGOS.get(nome_jogo)
    for mod_id, versao in lista_mods.items():
        mod = processar_mod(nome_jogo, mod_id, versao)
        if mod:
            mods.append(mod)
    return mods


def processar_mod(nome_jogo, mod_id, versao):
    cliente = client.APIClient()
    get_mod = endpoints.ENDPOINTS["get_mod"]
    list_files = endpoints.ENDPOINTS["list_files"]
    param = {
        "nome_jogo": nome_jogo,
        "mod_id": mod_id,
    }
    mod_online = cliente.chamar_endpoint(get_mod, param)
    mod_processado = obter_nome_versao(mod_online, versao)
    if mod_id == 5513:
        teste = cliente.chamar_endpoint(list_files, param)
        mod_processado = atualizar_versao_moasg(teste['file_updates'], mod_processado)

    return comparar_versao(mod_processado)


def comparar_versao(mod_online):
    try:
        assert mod_online['versao_online'] == mod_online['versao_local']
    except AssertionError:
        return mod_online


def atualizar_versao_moasg(lista_arquivos, mod):
    nome_versao = "MOASG_AllinOne-5513-"
    nome_arquivo = next(
        arquivo['new_file_name'] for arquivo in lista_arquivos if
        arquivo["new_file_name"].startswith(nome_versao))
    if nome_arquivo:
        versao = re.search(r'-(\d+(-\d+)*)-\d+\.zip$', nome_arquivo)
        mod['versao_online'] = versao.group(1).replace('-', '.').replace(
            '5513.', '')
    return mod


def retornar_mensagem(mods: list, nome_jogo):
    if mods:
        print(f"Existem {mods.__len__()} mods desatualizados.\n"
              f"Os seguintes mods estão desatualizados:")
        print('-' * 79)
        for mod in mods:
            url_complemento = f"{mod['mod_id']}?tab=files"
            url = f"https://www.nexusmods.com/{nome_jogo}/mods/{url_complemento}"
            print(
                f"Nome:          {mod['nome']} - {mod['mod_id']}\n"
                f"Versão Online: {mod['versao_online']}\n"
                f"Versão Local:  {mod['versao_local']}\n"
                f"url:           {url}"
            )
            print('-' * 79)
        caminho_jogo = PATH_JOGO.get(nome_jogo)
        if caminho_jogo:
            caminho_jogo = caminho_jogo.replace('\\', '/')  # troca barras invertidas por barras normais
            caminho_codificado = re.sub(r' ', '%20', caminho_jogo)  # apenas espaços codificados
            print(f'file:///{caminho_codificado}')
    else:
            print("Todos os mods estão atualizados")
