from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import NoteIn
from api.deps import current_user, owned, activity
router=APIRouter(prefix='/api/notes',tags=['notes'])
@router.get('')
def list_notes(search:str='',subject_id:int|None=None,user=Depends(current_user)):
 with get_db() as db:
  sql='SELECT n.*,s.name subject_name,t.name topic_name FROM notes n LEFT JOIN subjects s ON s.subject_id=n.subject_id LEFT JOIN topics t ON t.topic_id=n.topic_id WHERE n.user_id=%s'; p=[user['user_id']]
  if search: sql+=' AND (n.title LIKE %s OR n.content LIKE %s OR n.tags LIKE %s)';p += [f'%{search}%']*3
  if subject_id:sql+=' AND n.subject_id=%s';p.append(subject_id)
  sql+=' ORDER BY n.updated_at DESC'
  with db.cursor() as c:c.execute(sql,p);return c.fetchall()
@router.post('',status_code=201)
def create(data:NoteIn,user=Depends(current_user)):
 with get_db() as db:
  if data.subject_id: owned(db,'subjects','subject_id',data.subject_id,user['user_id'])
  with db.cursor() as c:c.execute('INSERT INTO notes(user_id,subject_id,topic_id,title,content,tags) VALUES(%s,%s,%s,%s,%s,%s)',(user['user_id'],data.subject_id,data.topic_id,data.title,data.content,data.tags));nid=c.lastrowid
  activity(db,user['user_id'],'note_created',f'Created note: {data.title}')
 return {'note_id':nid,'message':'Note created'}
@router.get('/{nid}')
def get(nid:int,user=Depends(current_user)):
 with get_db() as db:return owned(db,'notes','note_id',nid,user['user_id'])
@router.put('/{nid}')
def update(nid:int,data:NoteIn,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'notes','note_id',nid,user['user_id'])
  if data.subject_id:owned(db,'subjects','subject_id',data.subject_id,user['user_id'])
  with db.cursor() as c:c.execute('UPDATE notes SET subject_id=%s,topic_id=%s,title=%s,content=%s,tags=%s WHERE note_id=%s',(data.subject_id,data.topic_id,data.title,data.content,data.tags,nid))
 return {'message':'Note updated'}
@router.delete('/{nid}')
def delete(nid:int,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'notes','note_id',nid,user['user_id'])
  with db.cursor() as c:c.execute('DELETE FROM notes WHERE note_id=%s',(nid,))
 return {'message':'Note deleted'}
