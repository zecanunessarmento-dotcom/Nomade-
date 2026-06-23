from fastapi import FastAPI

app = FastAPI(
    title="E-commerce de Prata e Pedras Naturais"
)

@app.get("/")
def home():
    return {
        "mensagem": "API funcionando"
    }