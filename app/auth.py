# Lógica de autenticação

# 1. Hash e verificação de senhas com bcrypt

# 2. Geração de token JWT


# 3. Leitura e validação do token vindo do cookie

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Configurar o algoritmo do hash = bcrypt
pwd_context = CryptContext(schemes={"bcrypt"}, deprecated="auto")

# funcões de senha

def hash_senha(senha:str):
    return pwd_context.hash(senha)

def verificar_senha(senha:str, senha_hash:str):
    return pwd_context.verify(senha, senha_hash)


# Função para criar o token JWT
def criar_token(dados: dict):
    payload = dados.copy()

    #Definir quando o token vai expirar
    expira = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expira})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decodificar_token(token:str):
    #return jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
    payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
    return payload

# funcao para usar na rotas 
def get_usuario_logado(resquest: Request):
    token = resquest.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não esta autenticado"
        )
    try:
        payload = decodificar_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não esta autenticado"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token inválido"
            )
    
def get_usuario_opcional(resquest: Request):
    try:
        return get_usuario_logado(resquest)
    except HTTPException:
        return None
    

# Dependencia que exige login e perfil do admin
def get_admin(resquest: Request):
    usuario = get_usuario_logado(resquest)

    #Validar o admin
    if usuario.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return usuario