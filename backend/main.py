from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import auth, post

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"message": "DB Project"}


app.include_router(auth.router)
app.include_router(post.router)
