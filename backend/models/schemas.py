from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date

class Register(BaseModel):
    first_name:str=Field(min_length=1,max_length=80)
    last_name:str=Field(min_length=1,max_length=80)
    username:str=Field(min_length=3,max_length=50)
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)
    education_level:Optional[str]=None

class Login(BaseModel):
    identifier:str=Field(min_length=1,max_length=255)
    password:str=Field(min_length=1,max_length=128)

class SubjectIn(BaseModel):
    name:str=Field(min_length=1,max_length=150)
    description:Optional[str]=None

class TopicIn(BaseModel):
    name:str=Field(min_length=1,max_length=150)
    description:Optional[str]=None
    completion_percentage:float=Field(default=0,ge=0,le=100)

class NoteIn(BaseModel):
    title:str=Field(min_length=1,max_length=255)
    content:str
    subject_id:Optional[int]=None
    topic_id:Optional[int]=None
    tags:Optional[str]=None

class QuestionIn(BaseModel):
    question_text:str=Field(min_length=1)
    question_type:str='mcq'
    option_a:Optional[str]=None
    option_b:Optional[str]=None
    option_c:Optional[str]=None
    option_d:Optional[str]=None
    correct_answer:str=Field(min_length=1,max_length=500)
    explanation:Optional[str]=None

    @field_validator('question_type')
    @classmethod
    def validate_question_type(cls, value):
        allowed={'mcq','true_false','short_answer'}
        if value not in allowed:
            raise ValueError('question_type must be mcq, true_false, or short_answer')
        return value

class QuizIn(BaseModel):
    title:str=Field(min_length=1,max_length=255)
    subject_id:Optional[int]=None
    topic_id:Optional[int]=None
    difficulty:str='medium'
    questions:List[QuestionIn]=Field(min_length=1)

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, value):
        if value not in {'easy','medium','hard'}:
            raise ValueError('difficulty must be easy, medium, or hard')
        return value

class AttemptIn(BaseModel):
    answers:dict[int,str]

class GoalIn(BaseModel):
    title:str=Field(min_length=1,max_length=255)
    subject_id:Optional[int]=None
    description:Optional[str]=None
    target_date:date
    progress_percentage:float=Field(default=0,ge=0,le=100)
    status:str='active'

    @field_validator('status')
    @classmethod
    def validate_status(cls, value):
        if value not in {'active','completed','overdue'}:
            raise ValueError('status must be active, completed, or overdue')
        return value

class ProfileIn(BaseModel):
    first_name:Optional[str]=Field(default=None,min_length=1,max_length=80)
    last_name:Optional[str]=Field(default=None,min_length=1,max_length=80)
    username:Optional[str]=Field(default=None,min_length=3,max_length=50)
    email:Optional[EmailStr]=None
    education_level:Optional[str]=Field(default=None,max_length=100)
    profile_image:Optional[str]=Field(default=None,max_length=500)

class AIIn(BaseModel):
    prompt:str=Field(min_length=1,max_length=12000)
    conversation_id:Optional[int]=None
    subject:Optional[str]=None
    topic:Optional[str]=None
    education_level:Optional[str]=None
    difficulty:Optional[str]=None
