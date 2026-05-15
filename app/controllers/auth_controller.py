# Rotas de autenticação vai ficar aqui
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuario
from app.auth import hash_senha, verificar_senha, criar_token, get_usuario_logado

# APIRouter agrupa as rotas dentro desse módulo com prefixo /auth
router = APIRouter(prefix="/auth", tags=["Autenticação"])

templates = Jinja2Templates(directory="app/templates")


# tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

#Tela de login
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )

# Rota para criar o usuario
@router.post("/cadastro")
def fazer_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar se o email já esta cadastrado
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()

    #Mensagem de erro se o email já estiver em uso
    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            { "request": request, "erro": "Email já cadastrado! Por favor, escolha outro."}
        )
    # Criar o novo usuario
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha)
    )
    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(url="/auth/login", status_code=302)