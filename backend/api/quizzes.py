from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import QuizIn, AttemptIn
from api.deps import current_user, owned, activity
router=APIRouter(prefix='/api/quizzes',tags=['quizzes'])
@router.get('')
def list_quizzes(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT q.*,s.name subject_name,t.name topic_name,(SELECT MAX(percentage) FROM quiz_attempts a WHERE a.quiz_id=q.quiz_id AND a.user_id=%s) last_score FROM quizzes q LEFT JOIN subjects s ON s.subject_id=q.subject_id LEFT JOIN topics t ON t.topic_id=q.topic_id WHERE q.user_id=%s ORDER BY q.created_at DESC',(user['user_id'],user['user_id']));return c.fetchall()
@router.post('',status_code=201)
def create(data:QuizIn,user=Depends(current_user)):
 if not data.questions:raise HTTPException(422,'Add at least one question')
 with get_db() as db:
  if data.subject_id:owned(db,'subjects','subject_id',data.subject_id,user['user_id'])
  with db.cursor() as c:
   c.execute('INSERT INTO quizzes(user_id,subject_id,topic_id,title,difficulty,total_questions) VALUES(%s,%s,%s,%s,%s,%s)',(user['user_id'],data.subject_id,data.topic_id,data.title,data.difficulty,len(data.questions)));qid=c.lastrowid
   for q in data.questions:c.execute('INSERT INTO quiz_questions(quiz_id,question_text,question_type,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(qid,q.question_text,q.question_type,q.option_a,q.option_b,q.option_c,q.option_d,q.correct_answer,q.explanation))
  activity(db,user['user_id'],'quiz_created',f'Created quiz: {data.title}')
 return {'quiz_id':qid,'message':'Quiz created'}
@router.get('/{qid}')
def get(qid:int,user=Depends(current_user)):
 with get_db() as db:
  quiz=owned(db,'quizzes','quiz_id',qid,user['user_id'])
  with db.cursor() as c:c.execute('SELECT question_id,question_text,question_type,option_a,option_b,option_c,option_d FROM quiz_questions WHERE quiz_id=%s',(qid,));quiz['questions']=c.fetchall()
  return quiz
@router.post('/{qid}/attempt')
def attempt(qid:int,data:AttemptIn,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'quizzes','quiz_id',qid,user['user_id'])
  with db.cursor() as c:
   c.execute('SELECT * FROM quiz_questions WHERE quiz_id=%s',(qid,));qs=c.fetchall()
   score=sum(1 for q in qs if str(data.answers.get(q['question_id'], '')).strip().lower()==q['correct_answer'].strip().lower()); pct=round(score*100/len(qs),2) if qs else 0
   c.execute('INSERT INTO quiz_attempts(quiz_id,user_id,score,percentage,completed_at) VALUES(%s,%s,%s,%s,NOW())',(qid,user['user_id'],score,pct));aid=c.lastrowid
   for q in qs:
    ans=data.answers.get(q['question_id'],'');c.execute('INSERT INTO quiz_answers(attempt_id,question_id,selected_answer,is_correct) VALUES(%s,%s,%s,%s)',(aid,q['question_id'],ans,str(ans).lower()==q['correct_answer'].lower()))
  activity(db,user['user_id'],'quiz_completed',f'Completed quiz with {pct}%')
 return {'attempt_id':aid,'score':score,'percentage':pct,'total_questions':len(qs)}
@router.get('/{qid}/results')
def results(qid:int,user=Depends(current_user)):
 with get_db() as db:
  owned(db,'quizzes','quiz_id',qid,user['user_id'])
  with db.cursor() as c:
   c.execute('SELECT * FROM quiz_attempts WHERE quiz_id=%s AND user_id=%s ORDER BY completed_at DESC LIMIT 1',(qid,user['user_id']));attempt=c.fetchone()
   if not attempt:raise HTTPException(404,'No attempt found')
   c.execute('SELECT q.*,a.selected_answer,a.is_correct FROM quiz_questions q JOIN quiz_answers a ON a.question_id=q.question_id WHERE a.attempt_id=%s',(attempt['attempt_id'],));attempt['answers']=c.fetchall();return attempt
