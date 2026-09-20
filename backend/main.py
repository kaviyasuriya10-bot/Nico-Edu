from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from api import auth, subjects, notes, quizzes, goals, ai, progress, users, admin
app=FastAPI(title='NicoEdu API',version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    # Supports local static servers such as VS Code Live Server on any port.
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
@app.exception_handler(Exception)
async def safe_error(request:Request, exc:Exception): return JSONResponse(status_code=500,content={'detail':'Something went wrong. Please try again.'})
for r in [auth.router,subjects.router,notes.router,quizzes.router,goals.router,ai.router,progress.router,users.router,admin.router]:app.include_router(r)
@app.get('/api/health')
def health():return {'status':'ok','service':'NicoEdu API'}
