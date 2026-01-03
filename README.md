# 🚀 Como Usar o Projeto

## 1️⃣ Instalar Dependências

No diretório raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Obter a API_KEY do Nexus Mods

1. Acesse o site (logado):
   - https://next.nexusmods.com/settings/api-keys
2. Copie a **Personal API Key**, localizada ao final da página.

---

## 3️⃣ Configurar Variáveis de Ambiente

### 🔹 Opção A — PyCharm

1. Vá em:
   ```
   Run > Edit Configurations > Environment Variables
   ```
2. Adicione as seguintes variáveis:

```text
API_KEY="valor pego no site"
PATH_MHWORLD="caminho local da pasta de Monster Hunter World"
PATH_MHWILDS="caminho local da pasta de Monster Hunter Wilds"
PATH_ELDENRING="caminho local da pasta de Elden Ring"
PATH_EXPED33="caminho local da pasta de Expedition 33"
```

---

### 🔹 Opção B — VS Code

1. Crie uma pasta `.vscode` na raiz do projeto.
2. Dentro dela, crie o arquivo `launch.json` com o conteúdo abaixo:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run main.py",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal",
      "env": {
        "API_KEY": "CHAVE_API_NEXUS",
        "PATH_MHWORLD": "caminho local da pasta de Monster Hunter World",
        "PATH_MHWILDS": "caminho local da pasta de Monster Hunter Wilds",
        "PATH_ELDENRING": "caminho local da pasta de Elden Ring",
        "PATH_EXPED33": "caminho local da pasta de Expedition 33",
        "OUTRO_FLAG": "1"
      },
      "envFile": "${workspaceFolder}/.env",
      "args": ["--modo", "verificar_versao_mods"]
    }
  ]
}
```

---

## 4️⃣ Executar o Projeto

1. Altere a variável `nome_jogo` para um dos valores abaixo:
   - `monsterhunterworld`
   - `monsterhunterwilds`
   - `eldenring`
   - `clairobscurexpedition33`

2. Execute o projeto com:

```bash
python main.py
```

---

## 5️⃣ Configurar Novos Mods

### ➕ Adicionar novos mods

1. Abra o arquivo:
   ```
   api/parametros.py
   ```
2. No jogo desejado (respeitando a estrutura existente), adicione o **ID do mod**, que fica no final da URL do Nexus Mods.

#### 📌 Exemplo

- Mod: **ClairObscurFix**
- URL:
  ```
  https://www.nexusmods.com/clairobscurexpedition33/mods/24
  ```
- O ID do mod é: **24**

Adicione no `parametros.py`:

```python
24: "0.0.15",  # ClairObscurFix
```

---

## 6️⃣ Configurar Novos Jogos ou Remover Jogos Existentes

🚧 *Em breve...*
