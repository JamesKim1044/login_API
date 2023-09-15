from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from schema.user_Schem import *
import shutil, random, re, os, bcrypt, string

router = APIRouter(
    prefix="/users",
    tags= ["USERS"]
)

def is_valid_password(password: str) -> bool:
    # 비밀번호 규칙 검사 함수
    pattern = "^(?=.*[!@#$%^&])(?=.*[A-Z])(?=.*[0-9]).*$"
    return bool(re.match(pattern, password))

def delete_folder_contents(folder_path):
    try:
        # 폴더 내 모든 파일 및 하위 폴더 삭제
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
        
        # 최상위 폴더 삭제
        shutil.rmtree(folder_path)
        print(f"폴더 '{folder_path}' 및 내용 삭제 완료.")
    except Exception as e:
        print(f"삭제 중 오류 발생: {e}")

@router.get("")
def get_users_all(db : Session = Depends(get_db)):
    users = db.query(User).all()
    user_ids = []
    for user in users:
        user_ids.append(user.account_id)
    
    data = {
        "user_id" : user_ids
    }
    
    raise HTTPException(status_code=200, detail= {"success" : True, "message" : "유저 정보 가져오기 성공", "data" : data})

@router.get("/{user_id}")
def get_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.account_id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail={"success" : False, "message" : "유저가 존재하지 않습니다."})
    data = {
        "user_id" : user.user_id,
        "username" : user.user_name,
        "user_key" : user.key,
        "create_dt" : str(user.create_dt)
    }
    
    raise HTTPException(status_code=200, detail={"success" : True, "message" : "유저 정보 가져오기 성공", "data" : data})

@router.post("")
def create_user(user_data : UserCreate, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_data.user_id).first()
    if user != None:
        raise HTTPException(status_code=400, detail={"success" : False, "message" : "이미 존재하는 계정입니다."})
    else:
        user_id = user_data.user_id
    
    if db.query(User).filter(User.user_name == user_data.username).first() == None:
        pass
    else:
        raise HTTPException(status_code=400, detail={"success" : False, "message" : "이미 존재하는 닉네임 입니다."})
    
            
    if not is_valid_password(user_data.user_pw):
        raise HTTPException(status_code=400, detail={"success" : False, "message" : "비밀번호 규칙을 위반했습니다."})
    else:
        user_pw = bcrypt.hashpw(user_data.user_pw.encode('utf-8'), bcrypt.gensalt())
    
    while True:
        new_key = ''.join(random.choices(string.digits + string.ascii_uppercase, k=10))
        user_tmp = db.query(User).filter(User.key == new_key).first()
        if user_tmp == None:
            project_dir = os.getcwd().replace("\\", "/").replace("app", "") + "projects/" + new_key
            break
        else:
            continue
    
    new_user = User(user_id = user_id,
                    user_name = user_data.username, 
                    password = user_pw,
                    key = new_key,
                    create_dt = user_data.create_dt,
                    last_mod_dt = user_data.create_dt
                    )
    
    try:
        db.add(new_user)
        db.commit()
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
            
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code = 500, detail={"success" : False, "message" : "파일 생성 또는 데이터베이스 커밋 실패"})     

@router.put("/{user_id}")
def update_user(user_id : int, user_data : UserUpdate, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.account_id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail={"success" : False, "message" : "유저가 존재하지 않습니다."})
    
    if not bcrypt.checkpw(user_data.original_pw.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code = 401, detail={"success" : False, "message" : "비밀번호가 일치하지 않습니다."})
    
    if not is_valid_password(user_data.user_pw):
        raise HTTPException(status_code=400, detail={"success" : False, "message" : "비밀번호 규칙을 위반했습니다."})   
    
    try:
        user.password = user_data.user_pw
        user.last_mod_dt = str(datetime.now())
        db.commit()
        raise HTTPException(status_code=200, detail={"success" : True, "message" : "유저 수정 성공"})
    
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail={"success" : True, "message" : "데이터베이스 커밋 실패"})

@router.delete("/{user_id}")
def delete_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.account_id == user_id).first()
    
    if user == None:
        raise HTTPException(status_code=404, detail={"success" : False, "message" : "유저가 존재하지 않습니다."})
    
    if user:
        try:
            os.chdir("..")
            path = os.getcwd().replace("\\", "/").replace("app", "") + "projects/" + user.key
            delete_folder_contents(path)
            os.chdir("app")
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail={"success" : False, "message" : "디렉토리 삭제 실패"})
    try:
        
        db.delete(user)
        db.commit()
        raise HTTPException(status_code=200, detail={"success" : True, "message" : "유저 삭제 성공"})
        
    except Exception as e:
        print(str(e))        
        raise HTTPException(status_code=500, detail={"success" : False, "message" : "데이터베이스 커밋 실패"})

