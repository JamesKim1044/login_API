from pydantic import BaseModel, constr, validator
from datetime import datetime
import re

class UserCreate(BaseModel):
    username : str
    user_id : str
    user_pw : str
    create_dt: datetime = datetime.now()  # 사용자 생성 날짜 및 시간
    
    @validator("user_pw")
    def validate_password(cls, value):
        if not re.match(r"^(?=.*[!@#$%^&])(?=.*[A-Z])(?=.*[0-9]).*$", value):
            raise ValueError("비밀번호는 8~16자리 특수문자 대문자 숫자를 적어도 하나 포함해야 합니다.")
        return value
    
class UserUpdate(BaseModel):
    user_pw : str
    original_pw : str
    
    @validator("user_pw")
    def validate_password(cls, value):
        if not re.match(r"^(?=.*[!@#$%^&])(?=.*[A-Z])(?=.*[0-9]).*$", value):
            raise ValueError("비밀번호는 8~16자리 특수문자 대문자 숫자를 적어도 하나 포함해야 합니다.")
        return value
    
class UserLogin(BaseModel):
    user_id : str
    user_pw : str
    