from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Carrega os dados
df = pd.read_csv("pedido.csv", encoding='utf-16', delimiter=';', index_col='IdPedido')


df.index = df.index.astype(int)

@app.get("/pedido/{pedido_id}")
def get_pedido(pedido_id: int):
    if pedido_id in df.index:
        return {"IdPedido": pedido_id, "Dados": df.loc[pedido_id].to_dict()}
    else:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")