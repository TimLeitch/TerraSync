from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_router, auth_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(auth_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust the port if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "TerraSync"}
