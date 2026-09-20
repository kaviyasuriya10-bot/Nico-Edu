from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from database.connection import get_db
from utils.security import decode_token

bearer = HTTPBearer()
def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try: data = decode_token(credentials.credentials)
    except InvalidTokenError: raise HTTPException(401, 'Session expired or invalid')
    with get_db() as db:
        with db.cursor() as c:
            c.execute('SELECT user_id,first_name,last_name,username,email,role,education_level,profile_image,is_active FROM users WHERE user_id=%s', (data['sub'],))
            user=c.fetchone()
    if not user or not user['is_active']: raise HTTPException(401, 'Account is unavailable')
    return user
def admin_only(user=Depends(current_user)):
    if user['role'] != 'admin': raise HTTPException(403, 'Admin access required')
    return user
def owned(db, table, field, ident, user_id):
    with db.cursor() as c: c.execute(f'SELECT * FROM {table} WHERE {field}=%s AND user_id=%s', (ident,user_id)); row=c.fetchone()
    if not row: raise HTTPException(404, 'Resource not found')
    return row
def activity(db, user_id, type_, description):
    with db.cursor() as c: c.execute('INSERT INTO study_activity(user_id,activity_type,description) VALUES(%s,%s,%s)',(user_id,type_,description))
