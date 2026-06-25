from fastapi import FastAPI
from routers import cadastro

app = FastAPI(title="Condomínio Sion - API")

# Inclui o módulo de cadastro sob o prefixo /api
app.include_router(cadastro.router, prefix="/api")

@app.get("/api")
def status_global():
    return {
        "sistema": "Condomínio Sion",
        "status": "Operacional",
        "modulos_ativos": ["cadastro"],
        "arquitetura": "OCI Ampere ARM"
    }
