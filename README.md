# Analisador de E-mails com Inteligência Artificial

Este projeto foi desenvolvido como parte de um desafio técnico para uma vaga de trainee, com o objetivo de criar uma solução para automatizar a leitura e classificação de e-mails. A aplicação utiliza Inteligência Artificial para categorizar o conteúdo de um e-mail como "Produtivo" ou "Improdutivo" e, em seguida, sugere uma resposta apropriada com base na classificação.

## 🚀 Acesso à Aplicação

Você pode testar a aplicação ao vivo, hospedada na Vercel, através do seguinte link:

**[https://emails-classificator.vercel.app/](https://emails-classificator.vercel.app/)**

## ✨ Funcionalidades Principais

* **Classificação Inteligente:** Utiliza a API do Google Gemini para analisar o conteúdo do e-mail.
* **Múltiplos Formatos de Entrada:** O usuário pode colar o texto diretamente ou fazer o upload de arquivos `.txt` e `.pdf`.
* **Sugestão de Respostas:** Gera automaticamente um rascunho de resposta adequado ao contexto do e-mail.
* **Interface Intuitiva:** Design limpo, moderno e responsivo, focado na facilidade de uso.

## 🛠️ Tecnologias Utilizadas

A aplicação foi construída com as seguintes tecnologias:

* **Front-End:**
    * HTML5
    * CSS3
    * JavaScript (ES6+)
    * Fetch API

* **Back-End:**
    * Python 3
    * Flask (para o servidor web e a API)
    * PyMuPDF (para extração de texto de arquivos PDF)

* **Inteligência Artificial:**
    * Google Gemini API

* **Hospedagem (Deploy):**
    * Vercel

## ⚙️ Como Executar o Projeto Localmente

Para executar a aplicação no seu ambiente local, siga os passos abaixo.

### Pré-requisitos

* [Python 3.9+](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes do Python)

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/AlbertoMarinho/EmailsClassificator.git](https://github.com/AlbertoMarinho/EmailsClassificator.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd EmailsClassificator
    ```

3.  **Crie e ative um ambiente virtual (recomendado):**
    * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * No macOS ou Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

4.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure as Variáveis de Ambiente:**
    * Este projeto precisa de uma chave de API para se comunicar com o Google Gemini.
    * Na raiz do projeto, crie um arquivo chamado `.env`.
    * Dentro do arquivo `.env`, adicione a seguinte linha, substituindo `SUA_CHAVE_API_AQUI` pela sua chave:
        ```
        GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
        ```
    * **Importante:** O arquivo `.env` contém informações sensíveis e não deve ser enviado para o GitHub. Certifique-se de que ele está listado no seu arquivo `.gitignore`.

6.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

7.  **Acesse no navegador:**
    * Abra seu navegador e acesse o endereço: `http://127.0.0.1:5000`

## 👨‍💻 Como Usar

A aplicação foi projetada para ser extremamente simples e intuitiva:

1.  **Insira o conteúdo do e-mail:** Você pode colar o texto diretamente na caixa de texto OU clicar em "Escolher arquivo" para selecionar um arquivo `.txt` ou `.pdf` do seu computador.
2.  **Clique no botão "Analisar"**.
3.  Aguarde um instante enquanto a IA processa a informação. A classificação e a resposta sugerida aparecerão logo abaixo.

---

Feito por [Alberto Marinho](https://github.com/AlbertoMarinho)