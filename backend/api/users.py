from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import ProfileIn
from api.deps import current_user
router=APIRouter(prefix='/api/users',tags=['users'])
@router.put('/me')
def update_me(data:ProfileIn,user=Depends(current_user)):
 vals={k:v for k,v in data.model_dump().items() if v is not None}
 if not vals:return {'message':'Nothing to update'}
 with get_db() as db:
  if 'username' in vals or 'email' in vals:
   with db.cursor() as c:c.execute('SELECT user_id FROM users WHERE (username=%s OR email=%s) AND user_id!=%s',(vals.get('username',''),vals.get('email',''),user['user_id']))
   if c.fetchone():raise HTTPException(409,'Username or email already used')
  sql='UPDATE users SET '+','.join(f'{k}=%s' for k in vals)+' WHERE user_id=%s'
  with db.cursor() as c:c.execute(sql,[*vals.values(),user['user_id']])
 return {'message':'Profile updated'}
