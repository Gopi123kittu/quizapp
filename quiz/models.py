from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
engine = create_engine('sqlite:///myexam.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship

class Test(Base):
    __tablename__ ="test"
    id = Column(Integer, primary_key = True)
    name = Column(String)

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    choices = relationship('Choice', secondary = 'queans')
   
class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    questions = relationship('Question',secondary='queans')

class Queans(Base):
    __tablename__ = 'queans'
    question_id = Column(
        Integer, 
        ForeignKey('question.id'), 
        primary_key = True)

    choice_id = Column(
        Integer, 
        ForeignKey('choice.id'), 
        primary_key = True)

class Queanstest(Base):
    __tablename__ = 'Queanstest'
    test_id = Column(
        Integer, 
        ForeignKey('test.id'), 
        primary_key = True)

    ques_id_id = Column(
        Integer, 
        ForeignKey('question.id'), 
        primary_key = True)
    
    teacher_id = Column(
        Integer, 
        ForeignKey('teacher.id'), 
        primary_key = True)

class Pupil(Base):
    __tablename__ ="pupil"
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    sur_name = Column(String)
    email_add = Column(String)
    contact = Column(Integer)
    
class Teacher(Base):
    __tablename__ ="teacher"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    contact = Column(Integer)

class Testsubmission(Base):
    __tablename__ ="testsubmission"
    pupil_id = Column(
        Integer, 
        ForeignKey('pupil.id'), 
        primary_key = True)

    ques_id = Column(
        Integer, 
        ForeignKey('question.id'), 
        primary_key = True)

    choice_id = Column(
        Integer, 
        ForeignKey('choice.id'), 
        primary_key = True)
    
    test_id = Column(
        Integer, 
        ForeignKey('test.id'), 
        primary_key = True)

    teacher_id = Column(
        Integer, 
        ForeignKey('teacher.id'), 
        primary_key = True)

class Testresults(Base):
    __tablename__ = "testresults"
    pupil_id = Column(
        Integer, 
        ForeignKey('pupil.id'), 
        primary_key = True)
    
    test_id = Column(
        Integer, 
        ForeignKey('test.id'), 
        primary_key = True)

    status = Column(String)
    
    perc = Column(Integer)

Base.metadata.create_all(engine)
    
    
    
    
