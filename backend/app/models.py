from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    password_hash = Column(String(255), nullable=False)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    slug = Column(String(60), unique=True, nullable=False)
    image = Column(String(500))
    level = Column(String(20), default="beginner")
    title_en = Column(String(200)); title_ru = Column(String(200)); title_hy = Column(String(200))
    desc_en = Column(Text); desc_ru = Column(Text); desc_hy = Column(Text)
    lessons = relationship("Lesson", back_populates="course", order_by="Lesson.position")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    position = Column(Integer, nullable=False)
    title_en = Column(String(200)); title_ru = Column(String(200)); title_hy = Column(String(200))
    body_en = Column(Text); body_ru = Column(Text); body_hy = Column(Text)
    code = Column(Text)
    course = relationship("Course", back_populates="lessons")


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "lesson_id"),)
