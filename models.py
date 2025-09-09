from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKey, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

# Визначаємо ORM модель Group
class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    students: Mapped[list['Student']] = relationship(back_populates="group", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Group id={self.id} name={self.name!r}>"

# Визначаємо ORM модель Teacher
class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    subjects: Mapped[list['Subject']] = relationship(back_populates="teacher", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Teacher id={self.id} name={self.name!r}>"

# Визначаємо ORM модель Student
class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)

    group: Mapped[Optional['Group']] = relationship(back_populates="students")
    grades: Mapped[list['Grade']] = relationship(back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Student id={self.id} name={self.name!r} group_id={self.group_id}>"

# Визначаємо ORM модель Subject
class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    teacher: Mapped[Optional['Teacher']] = relationship(back_populates="subjects")
    grades: Mapped[list['Grade']] = relationship(back_populates="subject", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("name", name="uq_subject_name"),)

    def __repr__(self) -> str:
        return f"<Subject id={self.id} name={self.name!r} teacher_id={self.teacher_id}>"

# Визначаємо ORM модель Grade
class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    graded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student: Mapped['Student'] = relationship(back_populates="grades")
    subject: Mapped['Subject'] = relationship(back_populates="grades")

    __table_args__ = (
        CheckConstraint("grade BETWEEN 0 AND 100", name="ck_grade_range"),
        UniqueConstraint("student_id", "subject_id", "graded_at", name="uq_grade_unique_time"),
    )

    def __repr__(self) -> str:
        return f"<Grade id={self.id} student_id={self.student_id} subject_id={self.subject_id} grade={self.grade} at={self.graded_at.isoformat()}>"
