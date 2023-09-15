from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from schema.user_Schem import UserLogin
from auth.auth_handler import signJWT, decodeJWT
from auth.auth_bearer import JWTBearer
import bcrypt

router = APIRouter(
    tags= ["LOGIN"]
)
@router.post("/login")
async def user_login(user: UserLogin, db : Session = Depends(get_db)):
    user_log = db.query(User).filter(User.user_id == user.user_id).first()
    
    if user_log == None:
        raise HTTPException(status_code=404, detail={"success" : False, "message" : "유저가 존재하지 않습니다."})
    else:
        pass
    
    user_log = db.query(User).filter(User.user_id == user.user_id).first().__dict__
    
    if not bcrypt.checkpw(user.user_pw.encode('utf-8'), user_log['password'].encode('utf-8')):
        raise HTTPException(status_code = 401, detail={"success" : False, "message" : "비밀번호가 일치하지 않습니다."})
    
    else:
        new_token = signJWT(user_log['user_id'])
        token = new_token['access_token']
        raise HTTPException(status_code= 200, detail = {"success" : True, "message" : "로그인 되었습니다.", "token" : token})

@router.get("/users/me")
async def user_me(bearer: JWTBearer = Depends(JWTBearer()), db : Session = Depends(get_db)):
    
    if decodeJWT(bearer) == None:
        raise HTTPException(status_code = 401, detail={"success" : False, "message" : "토큰이 만료되었습니다."})
    
    user = db.query(User).filter(User.user_id == decodeJWT(bearer)['user_id']).first()
    if user == None:
        raise HTTPException(status_code=404, detail={"success" : False, "message" : "유저가 존재하지 않습니다."})
    
    else: 
        raise HTTPException(status_code = 200, detail={"success" : True, "message" : "승인됨", "data" : {"id" : user.account_id}})
