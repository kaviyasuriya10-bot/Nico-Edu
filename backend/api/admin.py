from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from database.connection import get_db
from api.deps import admin_only
router=APIRouter(prefix='/api/admin',tags=['admin'])
@router.get('/dashboard')
def dashboard(admin=Depends(admin_only)):
 with get_db() as db:
  with db.cursor() as c:
   c.execute("SELECT COUNT(*) total_students,SUM(is_active) active_students FROM users WHERE role='student'");out=c.fetchone()
   for key,table in [('total_subjects','subjects'),('total_notes','notes'),('total_quizzes','quizzes')]:c.execute(f'SELECT COUNT(*) {key} FROM {table}');out.update(c.fetchone())
   c.execute('SELECT COALESCE(AVG(percentage),0) average_quiz_score FROM quiz_attempts');out.update(c.fetchone());return out
@router.get('/students')
def students(search:str='',admin=Depends(admin_only)):
 with get_db() as db:
  with db.cursor() as c:c.execute("SELECT user_id,first_name,last_name,username,email,education_level,is_active,last_login,created_at FROM users WHERE role='student' AND (username LIKE %s OR email LIKE %s OR first_name LIKE %s) ORDER BY created_at DESC",[f'%{search}%']*3);return c.fetchall()
@router.get('/students/{uid}')
def student(uid:int,admin=Depends(admin_only)):
 with get_db() as db:
  with db.cursor() as c:c.execute("SELECT user_id,first_name,last_name,username,email,education_level,is_active,last_login,created_at FROM users WHERE user_id=%s AND role='student'",(uid,));u=c.fetchone()
  if not u:raise HTTPException(404,'Student not found')
  return u
@router.put('/students/{uid}/status')
def status(uid:int,active:bool,admin=Depends(admin_only)):
 with get_db() as db:
  with db.cursor() as c:c.execute("UPDATE users SET is_active=%s WHERE user_id=%s AND role='student'",(active,uid))
  if not c.rowcount:raise HTTPException(404,'Student not found')
 return {'message':'Student status updated'}
