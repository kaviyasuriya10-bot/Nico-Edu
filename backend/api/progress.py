from fastapi import APIRouter, Depends
from database.connection import get_db
from api.deps import current_user
router=APIRouter(prefix='/api/progress',tags=['progress'])
@router.get('')
def overview(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:
   uid=user['user_id'];c.execute('SELECT COUNT(*) total_subjects FROM subjects WHERE user_id=%s',(uid,));out=c.fetchone();c.execute('SELECT COUNT(*) notes_created FROM notes WHERE user_id=%s',(uid,));out.update(c.fetchone());c.execute('SELECT COUNT(*) quizzes_completed,COALESCE(AVG(percentage),0) average_score FROM quiz_attempts WHERE user_id=%s',(uid,));out.update(c.fetchone());c.execute('SELECT COALESCE(AVG(completion_percentage),0) overall_progress FROM topics t JOIN subjects s ON s.subject_id=t.subject_id WHERE s.user_id=%s',(uid,));out.update(c.fetchone());return out
@router.get('/subjects')
def by_subject(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT s.subject_id,s.name,COALESCE(AVG(t.completion_percentage),0) progress FROM subjects s LEFT JOIN topics t ON t.subject_id=s.subject_id WHERE s.user_id=%s GROUP BY s.subject_id,s.name',(user['user_id'],));return c.fetchall()
@router.get('/activity')
def activity(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT * FROM study_activity WHERE user_id=%s ORDER BY created_at DESC LIMIT 30',(user['user_id'],));return c.fetchall()
