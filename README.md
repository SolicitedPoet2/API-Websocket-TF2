# API-Websocket-TF2

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

Uma API RESTful robusta com integração WebSocket, projetada para atuar como uma ponte entre um servidor de jogo Team Fortress 2 (TF2) e múltiplos clientes em tempo real, como aplicações web, bots de Discord, e outras plataformas.

## Visão Geral

Este projeto recebe eventos de um servidor de jogo TF2 através de endpoints HTTP POST e os retransmite em tempo real para todos os clientes conectados via WebSocket. Ele também armazena certos eventos, como mensagens de chat, em um banco de dados MySQL para persistência e consulta futura.

A arquitetura desacoplada permite que o servidor de jogo (através de um plugin como o SourceMod) notifique a API sobre eventos importantes, e a API cuida da distribuição desses eventos para os interessados.

## ✨ Funcionalidades

-   **Ponte de Eventos em Tempo Real**: Conecta um servidor de jogo a múltiplos clientes via WebSockets.
-   **Endpoints HTTP Dedicados**: Rotas específicas para diferentes tipos de eventos do jogo.
-   **Eventos Suportados**:
    -   Mensagens de Chat (com persistência no banco de dados)
    -   Conexão de Jogadores
    -   Desconexão de Jogadores
    -   Mudança de Mapa
    -   Fim de Votação
-   **Persistência de Dados**: Armazena mensagens de chat em um banco de dados MySQL.
-   **Segurança**: Proteção de endpoints através de token de autenticação.
-   **Pronto para Contêineres**: Totalmente configurado para deploy com Docker.

## 🛠️ Tecnologias Utilizadas

-   **Backend**: Python 3.10+
-   **Framework**: FastAPI
-   **Comunicação em Tempo Real**: WebSockets
-   **Banco de Dados**: MySQL (com `SQLModel` para ORM)
-   **Gerenciador de Pacotes**: uv
-   **Servidor ASGI**: Uvicorn
-   **Contêiner**: Docker

## 📋 Pré-requisitos

-   Python 3.10 ou superior
-   `uv` (gerenciador de pacotes)
-   Docker (para deploy em contêiner)
-   Um servidor MySQL

## 🚀 Instalação e Execução Local

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/API-Websocket-TF2.git
    cd API-Websocket-TF2
    ```

2.  **Crie e configure o arquivo de ambiente:**
    Copie o arquivo de exemplo e preencha com suas credenciais.
    ```bash
    cp .env.example .env
    ```
    Edite o arquivo `.env` com os dados do seu banco de dados e um token de API.

3.  **Instale as dependências:**
    Use o `uv` para criar o ambiente virtual e instalar as dependências.
    ```bash
    uv sync
    ```

4.  **Inicie a aplicação:**
    O servidor será iniciado e estará acessível em `http://127.0.0.1:8000`.
    ```bash
    uv run uvicorn main:app --reload
    ```

## 🐳 Como Usar com Docker

1.  **Construa a imagem Docker:**
    ```bash
    docker build -t api-websocket-tf2 .
    ```

2.  **Execute o contêiner:**
    Certifique-se de passar as variáveis de ambiente necessárias. Você pode usar um arquivo `.env` para isso.
    ```bash
    docker run --rm -d -p 8080:80 --name tf2-api --env-file .env api-websocket-tf2
    ```
    A API estará disponível na porta `8080` do seu host.

## 📡 Endpoints da API

### WebSocket

O endpoint principal para clientes que desejam receber eventos em tempo real.

-   **URL**: `ws://<host>/ws/{client_name}`
-   **`client_name`**: Um identificador único para o cliente (ex: `webapp`, `discord_bot`).

### HTTP Endpoints

Esses endpoints são destinados ao servidor de jogo para enviar eventos para a API. As requisições devem incluir o token de API no header `Authorization` ou como um query parameter `token`.

-   `POST /cm/{client}`: Envia uma mensagem de chat.
    -   **Body**: `{ "user": "string", "content": "string", "steamid": "string", "team": "string" }`
-   `POST /pc/`: Notifica a conexão de um jogador.
    -   **Body**: `{ "name": "string", "steamid": "string", "country": "string" }`
-   `POST /pd/`: Notifica a desconexão de um jogador.
    -   **Body**: `{ "name": "string", "steamid": "string", "reason": "string" }`
-   `POST /mc/`: Notifica uma mudança de mapa.
    -   **Body**: `{ "did_map_end": true, "map_name": "string" }`
-   `POST /ve/`: Notifica o fim de uma votação.
    -   **Body**: `{ "case": "string", "reason": "string" }`

Todos os dados recebidos por esses endpoints são enriquecidos com um campo `event_type` e retransmitidos para os clientes WebSocket.

## ⚙️ Configuração

As seguintes variáveis de ambiente precisam ser definidas no arquivo `.env`:

-   `API_TOKEN`: Token secreto para autorizar as requisições POST.
-   `MYSQL_URL`: Endereço do servidor MySQL.
-   `MYSQL_PORT`: Porta do servidor MySQL.
-   `MYSQL_USER`: Usuário do banco de dados.
-   `MYSQL_PASSWORD`: Senha do banco de dados.
-   `MYSQL_DATABASE`: Nome do banco de dados.

---

*Este projeto foi gerado para fornecer uma solução robusta e escalável para a comunicação de eventos de servidores de jogos.*