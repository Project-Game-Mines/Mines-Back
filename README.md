# 🐰 Sweet Mines Backend
Este é o projeto de backend para o jogo Sweet Mines, desenvolvido em Python utilizando o framework FastAPI.

## Recursos Principais

FastAPI: Framework moderno, rápido (alto desempenho) e web para a construção de APIs assíncronas em Python, com validação de dados automática via Pydantic.

MongoDB: Banco de dados NoSQL utilizado para persistência de dados do jogo, como informações de usuários, pontuações e estados de partidas.

WebSockets: Comunicação bidirecional e em tempo real para gerenciar o estado das partidas do Sweet Mines, permitindo atualizações instantâneas no frontend.

RabbitMQ: Broker de mensagens utilizado para comunicação assíncrona. Ele gerencia a fila de eventos do jogo (ex: "Iniciar jogo", "depósito de pontos") e notifica os clientes (WebSockets) sobre as mudanças.


## Como rodar

Clone o repositório:

```powershell
git clone https://github.com/Project-Game-Mines/Mines-Back.git
```
Crie as imagens e suba os containers no Docker

```powershell
docker compose up --build
```

## Eventos

```python
{"event":"GAME_START","data":{"bet_amount":100, "total_cells": 25, "total_mines":3}, "user_id":"..."}
{"event":"GAME_STEP","data":{"match_id":"...","cell":5}}
{"event":"GAME_CASHOUT","data":{"match_id":"..."}}
{"event": "GAME_WIN","prize": prize, "mines_positions": mines_positions}
{"event": "GAME_LOSE", "mines_positions": mines_positions}
```

## Trechos

Função de game_start:
```python
async def handle_game_start(data, services, user_id):
    return await services["start"].start_game(
        user_id=user_id,
        bet_amount=data.get("bet_amount"),
        total_mines=data.get("total_mines"),
        total_cells=data.get("total_cells")
    )
```

Campos de step_result:
```python
user_id = mines_match["user_id"]
bet_amount = mines_match["bet_amount"]
current_step = mines_match["current_step"] + 1
mines_positions = mines_match["mines_positions"]

safe_cells = mines_match['total_cells'] - len(mines_positions)
progress = current_step / safe_cells
prize = round(bet_amount * (1 + progress), 2)
```

Função que mostra balanço na carteira: 
```python
def get_balance(self, user_id: str) -> WalletSchemas:
        
  wallet = self.collection_wallet.find_one({"user_id": user_id})
        if not wallet:
            return None
        return WalletSchemas(**wallet)
```
