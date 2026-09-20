from fastapi import APIRouter, HTTPException, Depends  # type: ignore[reportMissingImports]
from models.schemas import Register, Login
from database.connection import get_db
from utils.security import hash_password, verify_password, create_token
from api.deps import current_user

router=APIRouter(prefix='/api/auth',tags=['authentication'])
@router.post('/register',status_code=201)
def register(data:Register):
    with get_db() as db:
        with db.cursor() as c:
            c.execute('SELECT user_id FROM users WHERE username=%s OR email=%s',(data.username,data.email))
            if c.fetchone(): raise HTTPException(409,'Username or email is already registered')
            c.execute('INSERT INTO users(first_name,last_name,username,email,password_hash,education_level) VALUES(%s,%s,%s,%s,%s,%s)',(data.first_name,data.last_name,data.username,data.email,hash_password(data.password),data.education_level))
            uid=c.lastrowid
    return {'token':create_token(uid,'student'),'user':{'user_id':uid,'first_name':data.first_name,'role':'student'}}
@router.post('/login')
def login(data:Login):
    with get_db() as db:
        with db.cursor() as c:
            c.execute('SELECT * FROM users WHERE username=%s OR email=%s',(data.identifier,data.identifier)); u=c.fetchone()
            if not u or not verify_password(data.password,u['password_hash']): raise HTTPException(401,'Invalid username/email or password')
            if not u['is_active']: raise HTTPException(403,'Your account has been deactivated')
            c.execute('UPDATE users SET last_login=NOW() WHERE user_id=%s',(u['user_id'],))
    return {'token':create_token(u['user_id'],u['role']),'user':{k:u[k] for k in ('user_id','first_name','last_name','username','email','role','education_level','profile_image')}}
@router.post('/logout')
def logout(user=Depends(current_user)): return {'message':'Logged out. Remove the token on this device.'}
@router.get('/me')
def me(user=Depends(current_user)): return user
