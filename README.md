Como Usar o Projeto
1. Instalar Dependências:
   * No diretório do projeto, execute:
        ```bash
        pip install -r requirements.txt
        ```
2. Pegar API_KEY:
   * No site https://next.nexusmods.com/settings/api-keys logado, basta copiar a Personal API Key localizada ao final do site
3. Configure as variáveis de ambiente:
    * Via PyCharm no caminho: "Run > Edit Configurations > Environment Variables" adicione as variáveis
      * API_KEY="valor pego no site"
      * PATH_MHWILDS="caminho local da pasta de Monster Hunter Wilds"
      * PATH_ELDENRING="caminho local da pasta de Elden Ring"
4. Executar o Projeto:
    * Alterar a variável nome jogo para um dos seguintes:
      * eldenring
      * monsterhunterworld
      * monsterhunterwilds
    * Para rodar o projeto, basta executar o main.py:
        ```bash
        python main.py
        ```