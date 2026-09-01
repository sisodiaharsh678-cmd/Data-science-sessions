from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Instagram Like Counter API running"}