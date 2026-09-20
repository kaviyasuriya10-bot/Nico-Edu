from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import GoalIn
from api.deps import current_user, owned
router=APIRouter(prefix='/api/goals',tags=['goals'])
@router.get('')
def list_goals(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute("UPDATE study_goals SET status='overdue' WHERE user_id=%s AND status='active' AND target_date<CURDATE()",(user['user_id'],));c.execute('SELECT g.*,s.name subject_name FROM study_goals g LEFT JOIN subjects s ON s.subject_id=g.subject_id WHERE g.user_id=%s ORDER BY target_date',(user['user_id'],));return c.fetchall()
@router.post('',status_code=201)
def create(data:GoalIn,user=Depends(current_user)):
 with get_db() as db:
  if data.subject_id:owned(db,'subjects','subject_id',data.subject_id,user['user_id'])
  status='completed' if data.progress_percentage==100 else data.status
  with db.cursor() as c:c.execute('INSERT INTO study_goals(user_id,subject_id,title,description,target_date,progress_percentage,status) VALUES(%s,%s,%s,%s,%s,%s,%s)',(user['user_id'],data.subject_id,data.title,data.description,data.target_date,data.progress_percentage,status));return {'goal_id':c.lastrowid,'message':'Goal created'}
@router.put('/{gid}')
def update(gid:int,data:GoalIn,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'study_goals','goal_id',gid,user['user_id']);status='completed' if data.progress_percentage==100 else data.status
  with db.cursor() as c:c.execute('UPDATE study_goals SET subject_id=%s,title=%s,description=%s,target_date=%s,progress_percentage=%s,status=%s WHERE goal_id=%s',(data.subject_id,data.title,data.description,data.target_date,data.progress_percentage,status,gid))
 return {'message':'Goal updated'}
@router.delete('/{gid}')
def delete(gid:int,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'study_goals','goal_id',gid,user['user_id'])
  with db.cursor() as c:c.execute('DELETE FROM study_goals WHERE goal_id=%s',(gid,))
 return {'message':'Goal deleted'}
