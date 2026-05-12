import asyncio
import websockets
import json
import sys

HOST = input("IP do servidor (Enter para localhost): ").strip() or "localhost"
NOME = input("Seu nome: ").strip() or "Anônimo"

async def receber(ws):
    async for raw in ws:
        data = json.loads(raw)
        if "sistema" in data:
            print(f"\n  {data['sistema']}")
        else:
            print(f"\n[{data['hora']}] {data['nome']}: {data['texto']}")
        print("Você: ", end="", flush=True)

async def enviar(ws):
    loop = asyncio.get_event_loop()
    while True:
        texto = await loop.run_in_executor(None, lambda: input("Você: "))
        if texto.strip():
            await ws.send(texto.strip())

async def main():
    uri = f"ws://{HOST}:8765"
    print(f"\nConectando em {uri}...")
    async with websockets.connect(uri) as ws:
        await ws.send(NOME)
        print(f"Conectado! Olá, {NOME}. Digite suas mensagens:\n")
        await asyncio.gather(receber(ws), enviar(ws))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nSaindo...")
except Exception as e:
    print(f"Erro: {e}")
