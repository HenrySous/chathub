import asyncio
import websockets
import json
from datetime import datetime

clientes = {}  # websocket -> nome
historico = []

async def broadcast(mensagem, excluir=None):
    for ws in list(clientes):
        if ws != excluir:
            try:
                await ws.send(mensagem)
            except:
                clientes.pop(ws, None)

async def handler(ws):
    nome = await ws.recv()
    clientes[ws] = nome

    hora = datetime.now().strftime("%H:%M")
    print(f"[{hora}] {nome} entrou | {len(clientes)} online")

    # Manda histórico pra quem entrou
    for msg in historico:
        await ws.send(msg)

    entrada = json.dumps({"sistema": f">>> {nome} entrou no chat"})
    await broadcast(entrada)

    try:
        async for texto in ws:
            hora = datetime.now().strftime("%H:%M")
            msg = json.dumps({"nome": nome, "texto": texto, "hora": hora})
            historico.append(msg)
            if len(historico) > 100:
                historico.pop(0)
            print(f"[{hora}] {nome}: {texto}")
            await broadcast(msg)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clientes.pop(ws, None)
        hora = datetime.now().strftime("%H:%M")
        print(f"[{hora}] {nome} saiu | {len(clientes)} online")
        saida = json.dumps({"sistema": f"<<< {nome} saiu do chat"})
        await broadcast(saida)

async def main():
    print("=" * 40)
    print("  UniChat - Servidor rodando!")
    print("  Porta: 8765")
    print("  Ctrl+C para encerrar")
    print("=" * 40)
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
