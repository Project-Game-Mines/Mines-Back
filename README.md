# 🍬 Sweet Mines Backend
Este é o projeto de backend para o jogo Sweet Mines, desenvolvido em Python utilizando o framework FastAPI.

## Recursos Principais

FastAPI: Framework moderno, rápido (alto desempenho) e web para a construção de APIs assíncronas em Python, com validação de dados automática via Pydantic.

MongoDB: Banco de dados NoSQL utilizado para persistência de dados do jogo, como informações de usuários, pontuações e estados de partidas.

WebSockets: Comunicação bidirecional e em tempo real para gerenciar o estado das partidas do Sweet Mines, permitindo atualizações instantâneas no frontend.

RabbitMQ: Broker de mensagens utilizado para comunicação assíncrona. Ele gerencia a fila de eventos do jogo (ex: "Iniciar jogo", "depósito de pontos") e notifica os clientes (WebSockets) sobre as mudanças.


## Como rodar

Clone o repositório:

```powershell
git clone https://github.com/alicevital/Mines-Back.git
```
Suba os containers no Docker

```powershell
docker compose up --build
```
