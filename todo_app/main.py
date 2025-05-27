from datetime import datetime
from fastapi import FastAPI
from sqlmodel import Field,SQLModel, create_engine


app = FastAPI()

DATABASE_URL="postgresql://admin:adminpassword@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
        


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    end_time: datetime

@app.on_event('startup')
def create_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/") 
def home():
    return{"message": "Home"}   