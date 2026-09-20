from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
class Register(BaseModel): first_name:str=Field(min_length=1,max_length=80); last_name:str=Field(min_length=1,max_length=80); username:str=Field(min_length=3,max_length=50); email:EmailStr; password:str=Field(min_length=8,max_length=128); education_level:Optional[str]=None
class Login(BaseModel): identifier:str; password:str
class SubjectIn(BaseModel): name:str=Field(min_length=1,max_length=150); description:Optional[str]=None
class TopicIn(BaseModel): name:str=Field(min_length=1,max_length=150); description:Optional[str]=None; completion_percentage:float=Field(default=0,ge=0,le=100)
class NoteIn(BaseModel): title:str=Field(min_length=1,max_length=255); content:str; subject_id:Optional[int]=None; topic_id:Optional[int]=None; tags:Optional[str]=None
class QuestionIn(BaseModel): question_text:str; question_type:str='mcq'; option_a:Optional[str]=None; option_b:Optional[str]=None; option_c:Optional[str]=None; option_d:Optional[str]=None; correct_answer:str; explanation:Optional[str]=None
class QuizIn(BaseModel): title:str; subject_id:Optional[int]=None; topic_id:Optional[int]=None; difficulty:str='medium'; questions:List[QuestionIn]
class AttemptIn(BaseModel): answers:dict[int,str]
class GoalIn(BaseModel): title:str; subject_id:Optional[int]=None; description:Optional[str]=None; target_date:date; progress_percentage:float=Field(default=0,ge=0,le=100); status:str='active'
class ProfileIn(BaseModel): first_name:Optional[str]=None; last_name:Optional[str]=None; username:Optional[str]=None; email:Optional[EmailStr]=None; education_level:Optional[str]=None; profile_image:Optional[str]=None
class AIIn(BaseModel): prompt:str=Field(min_length=1,max_length=12000); conversation_id:Optional[int]=None; subject:Optional[str]=None; topic:Optional[str]=None; education_level:Optional[str]=None; difficulty:Optional[str]=None
