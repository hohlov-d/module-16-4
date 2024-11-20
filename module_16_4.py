from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_all() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create(user: User,
                 username: Annotated[
                     str, Path(min_length=5, max_length=20, description="Enter username", example="Ilya")],
                 age: int = Path(ge=18, le=120, description='Enter age', example=55)) -> str:
    user.id = 1 if len(users) == 0 else len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f'User {user.id} is registered'


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        username: Annotated[
            str, Path(min_length=5, max_length=20, description="Enter username", example="Ilya")],
        age: int = Path(ge=18, le=120, description="Enter age", example=55),
        user_id: int = Path(ge=0)) -> str:
    try:
        edit_user = next(user for user in users if user.id == user_id)
        edit_user.username = username
        edit_user.age = age
        return f"The user {user_id} is updated"
    except Exception:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        del_user = [user for user in users if user.id == user_id][0]
        users.remove(del_user)
        return f'User {user_id} has been deleted.'
    except Exception:
        raise HTTPException(status_code=404, detail='User was not found')
