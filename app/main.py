from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import accounts, login, posts, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, "static"))), name="static")
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))
message = "Welcome to FASTAPI Training Page."

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(login.router)
app.include_router(posts.router)
app.include_router(vote.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"root_path": request.scope.get("root_path"), "request":request, "message":message})
