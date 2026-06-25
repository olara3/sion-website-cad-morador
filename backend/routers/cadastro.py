from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pymysql

router = APIRouter()

# Configuração da conexão com o banco de dados
def get_db():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='sion_user',
        password=os.getenv("DB_PASSWORD"), # <--- Coloque a senha do seu mariadb aqui
        database='condominio_sion',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        yield connection
    finally:
        connection.close()

# Modelo de validação para Inserção de Morador
class MoradorCreate(BaseModel):
    id_unidade: int
    nome_completo: str
    rg: str
    cpf: str
    celular: str
    grau_parentesco: str

@router.post("/morador", status_code=201)
def cadastrar_morador(morador: MoradorCreate, db: pymysql.Connection = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            sql = """
                INSERT INTO moradores (id_unidade, nome_completo, rg, cpf, celular, grau_parentesco)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                morador.id_unidade,
                morador.nome_completo,
                morador.rg,
                morador.cpf,
                morador.celular,
                morador.grau_parentesco
            ))
            db.commit()
            return {"status": "Sucesso", "mensagem": "Morador cadastrado com sucesso!"}
            
    except pymysql.err.IntegrityError as e:
        # Captura o erro de duplicidade (clique duplo ou mesmo CPF na mesma unidade)
        if e.args[0] == 1062:
            raise HTTPException(status_code=400, detail="Este morador já está cadastrado nesta unidade.")
        raise HTTPException(status_code=400, detail=f"Erro de integridade: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")

@router.get("/unidade/{numero_unidade}")
def buscar_unidade_portaria(numero_unidade: str, db: pymysql.Connection = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            # Query com INNER JOIN e máscara de CPF no banco (LGPD)
            sql = """
                SELECT 
                    u.numero AS apartamento,
                    u.bloco_torre,
                    m.nome_completo,
                    m.celular,
                    m.grau_parentesco,
                    CONCAT('******', SUBSTRING(m.cpf, 7, 3), '-', SUBSTRING(m.cpf, 10, 2)) AS cpf_mascarado
                FROM unidades u
                INNER JOIN moradores m ON u.id = m.id_unidade
                WHERE u.numero = %s
            """
            cursor.execute(sql, (numero_unidade,))
            resultados = cursor.fetchall()
            
            if not resultados:
                raise HTTPException(status_code=404, detail="Nenhum morador encontrado para esta unidade.")
                
            return resultados
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta: {str(e)}")

