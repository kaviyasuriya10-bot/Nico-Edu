from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import SubjectIn, TopicIn
from api.deps import current_user, owned, activity
router=APIRouter(prefix='/api',tags=['subjects'])
@router.get('/subjects')
def list_subjects(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:
   c.execute("SELECT s.*,COUNT(DISTINCT t.topic_id) topic_count,COUNT(DISTINCT n.note_id) note_count,COUNT(DISTINCT q.quiz_id) quiz_count,COALESCE(AVG(t.completion_percentage),0) progress FROM subjects s LEFT JOIN topics t ON t.subject_id=s.subject_id LEFT JOIN notes n ON n.subject_id=s.subject_id LEFT JOIN quizzes q ON q.subject_id=s.subject_id WHERE s.user_id=%s GROUP BY s.subject_id ORDER BY s.updated_at DESC",(user['user_id'],)); return c.fetchall()
@router.post('/subjects',status_code=201)
def create_subject(data:SubjectIn,user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c: c.execute('INSERT INTO subjects(user_id,name,description) VALUES(%s,%s,%s)',(user['user_id'],data.name,data.description)); sid=c.lastrowid
  activity(db,user['user_id'],'subject_created',f'Created subject: {data.name}')
 return {'subject_id':sid,'message':'Subject created'}
@router.get('/subjects/{sid}')
def get_subject(sid:int,user=Depends(current_user)):
 with get_db() as db: return owned(db,'subjects','subject_id',sid,user['user_id'])
@router.put('/subjects/{sid}')
def update_subject(sid:int,data:SubjectIn,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'subjects','subject_id',sid,user['user_id'])
  with db.cursor() as c:c.execute('UPDATE subjects SET name=%s,description=%s WHERE subject_id=%s',(data.name,data.description,sid))
 return {'message':'Subject updated'}
@router.delete('/subjects/{sid}')
def delete_subject(sid:int,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'subjects','subject_id',sid,user['user_id'])
  with db.cursor() as c:c.execute('DELETE FROM subjects WHERE subject_id=%s',(sid,))
 return {'message':'Subject deleted'}
@router.get('/subjects/{sid}/topics')
def topics(sid:int,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'subjects','subject_id',sid,user['user_id'])
  with db.cursor() as c:c.execute('SELECT * FROM topics WHERE subject_id=%s ORDER BY created_at',(sid,));return c.fetchall()
@router.post('/subjects/{sid}/topics',status_code=201)
def create_topic(sid:int,data:TopicIn,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'subjects','subject_id',sid,user['user_id'])
  with db.cursor() as c:c.execute('INSERT INTO topics(subject_id,name,description,completion_percentage) VALUES(%s,%s,%s,%s)',(sid,data.name,data.description,data.completion_percentage)); tid=c.lastrowid
 return {'topic_id':tid,'message':'Topic created'}
@router.put('/topics/{tid}')
def update_topic(tid:int,data:TopicIn,user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT t.* FROM topics t JOIN subjects s ON s.subject_id=t.subject_id WHERE t.topic_id=%s AND s.user_id=%s',(tid,user['user_id']));
  if not c.fetchone():raise HTTPException(404,'Topic not found')
  with db.cursor() as c:c.execute('UPDATE topics SET name=%s,description=%s,completion_percentage=%s WHERE topic_id=%s',(data.name,data.description,data.completion_percentage,tid))
 return {'message':'Topic updated'}
@router.delete('/topics/{tid}')
def delete_topic(tid:int,user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('DELETE t FROM topics t JOIN subjects s ON s.subject_id=t.subject_id WHERE t.topic_id=%s AND s.user_id=%s',(tid,user['user_id']))
  if not c.rowcount:raise HTTPException(404,'Topic not found')
 return {'message':'Topic deleted'}
