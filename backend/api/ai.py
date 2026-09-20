from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from models.schemas import AIIn
from api.deps import current_user
from services.ai_service import respond, AIUnavailable
router=APIRouter(prefix='/api/ai',tags=['ai'])
def run(data,user,kind='answer'):
 try: answer=respond(data.prompt)
 except AIUnavailable as e: raise HTTPException(503,str(e))
 with get_db() as db:
  with db.cursor() as c:
   cid=data.conversation_id
   if cid:
    c.execute('SELECT conversation_id FROM ai_conversations WHERE conversation_id=%s AND user_id=%s',(cid,user['user_id']))
    if not c.fetchone():raise HTTPException(404,'Conversation not found')
   else:c.execute('INSERT INTO ai_conversations(user_id,title) VALUES(%s,%s)',(user['user_id'],data.prompt[:80]));cid=c.lastrowid
   c.execute("INSERT INTO ai_messages(conversation_id,sender,message) VALUES(%s,'user',%s)",(cid,data.prompt));c.execute("INSERT INTO ai_messages(conversation_id,sender,message) VALUES(%s,'assistant',%s)",(cid,answer))
 return {'conversation_id':cid,'message':answer}
@router.post('/chat')
def chat(data:AIIn,user=Depends(current_user)):return run(data,user)
@router.post('/summarize')
def summarize(data:AIIn,user=Depends(current_user)):data.prompt='Summarize clearly for a student:\n'+data.prompt;return run(data,user)
@router.post('/generate-notes')
def notes(data:AIIn,user=Depends(current_user)):data.prompt='Generate structured study notes with overview, definitions, key concepts, examples, common mistakes and quick revision:\n'+data.prompt;return run(data,user)
@router.post('/generate-questions')
def questions(data:AIIn,user=Depends(current_user)):data.prompt='Generate useful practice questions and answers:\n'+data.prompt;return run(data,user)
@router.post('/generate-quiz')
def quiz(data:AIIn,user=Depends(current_user)):data.prompt='Generate an MCQ quiz in JSON-like clear structure including correct answers and explanations:\n'+data.prompt;return run(data,user)
@router.get('/conversations')
def conversations(user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT * FROM ai_conversations WHERE user_id=%s ORDER BY updated_at DESC',(user['user_id'],));return c.fetchall()
@router.get('/conversations/{cid}')
def messages(cid:int,user=Depends(current_user)):
 with get_db() as db:
  with db.cursor() as c:c.execute('SELECT m.* FROM ai_messages m JOIN ai_conversations c ON c.conversation_id=m.conversation_id WHERE m.conversation_id=%s AND c.user_id=%s ORDER BY m.created_at',(cid,user['user_id']));return c.fetchall()
