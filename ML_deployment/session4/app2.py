from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Instagram Like Counter API running"}

class LikesInput(BaseModel):
    current_likes: int
    new_likes: int

@app.post("/predict-likes")
def predict_likes(data: LikesInput):
    total_likes = data.current_likes + data.new_likes
    return {"total_likes": total_likes}