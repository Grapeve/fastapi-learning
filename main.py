import uuid

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from database import engine, get_db
import models
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# @app.get("/", response_model=schemas.User)
# def read_user(db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == 1).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@app.get("/")
def hello_world():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Success!"
        }
    )


@app.get("/has_register")
def check_user(username: str, db: Session = Depends(get_db)):
    has_register = db.query(models.User).filter(models.User.username == username).first()
    if not has_register:
        return JSONResponse(
            status_code=201,
            content={
                'detail': 'username can be used'
            }
        )
    else:
        raise HTTPException(status_code=409, detail="Username has been use")


@app.post("/register")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    has_register = db.query(models.User).filter(models.User.username == user.username).first()
    if not has_register:
        db_user = models.User(username=user.username, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(
            status_code=201,
            content={
                'id': db_user.id,
                'user': db_user.username
            }
        )
    else:
        raise HTTPException(status_code=409, detail="Username has been use")


# get请求中不能使用schemas
@app.get("/login")
def user_login(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username,
                                           models.User.password == password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Username or password error")

    token = str(uuid.uuid4())
    db_user.token = token
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            'id': db_user.id,
            'token': token
        }
    )


@app.get('/verify_login_status')
def user_verify_login(username: str, token: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username,
                                           models.User.token == token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Login failed")
    return JSONResponse(
        status_code=200,
        content={
            "message": 'Login successful'
        }
    )


@app.put('/user_logout')
def user_logout(user: schemas.UserLogout, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username,
                                           models.User.token == user.token).first()
    db_user.token = " "
    db.commit()
    return {
        "status": 204
    }


if __name__ == '__main__':
    uvicorn.run(app)
