from sqlalchemy import func, desc, select
from sqlalchemy.orm import aliased
from db import session_scope
from models import Student, Group, Teacher, Subject, Grade

# 1. Top-5 студентів за середнім балом
def select_1():
    with session_scope() as s:
        q = (
            s.query(Student.id, Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
        )
        return q.all()

# 2. Студент з найвищим середнім балом у конкретному предметі (за subject_id)
def select_2(subject_id: int):
    with session_scope() as s:
        q = (
            s.query(Student.id, Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
            .join(Grade, Grade.student_id == Student.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(1)
        )
        return q.first()

# 3. Середній бал по групах для конкретного предмета
def select_3(subject_id: int):
    with session_scope() as s:
        q = (
            s.query(Group.id, Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .order_by(Group.id)
        )
        return q.all()

# 4. Загальний середній бал по всій таблиці оцінок
def select_4():
    with session_scope() as s:
        (avg_val,) = s.query(func.round(func.avg(Grade.grade), 2)).one()
        return avg_val

# 5. Список курсів, які читає конкретний викладач
def select_5(teacher_id: int):
    with session_scope() as s:
        q = s.query(Subject.id, Subject.name).filter(Subject.teacher_id == teacher_id)
        return q.all()

# 6. Студенти в конкретній групі
def select_6(group_id: int):
    with session_scope() as s:
        q = s.query(Student.id, Student.name).filter(Student.group_id == group_id).order_by(Student.id)
        return q.all()

# 7. Оцінки студентів у конкретній групі з конкретного предмета
def select_7(group_id: int, subject_id: int):
    with session_scope() as s:
        q = (
            s.query(Student.id, Student.name, Grade.grade, Grade.graded_at)
            .join(Grade, Grade.student_id == Student.id)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .order_by(Student.id, Grade.graded_at.desc())
        )
        return q.all()

# 8. Середній бал, який ставить конкретний викладач по своїх предметах
def select_8(teacher_id: int):
    with session_scope() as s:
        q = (
            s.query(func.round(func.avg(Grade.grade), 2))
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.teacher_id == teacher_id)
        )
        (avg_val,) = q.one()
        return avg_val

# 9. Список курсів, які відвідує конкретний студент (має оцінки за них)
def select_9(student_id: int):
    with session_scope() as s:
        q = (
            s.query(Subject.id, Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Grade.student_id == student_id)
            .group_by(Subject.id)
            .order_by(Subject.id)
        )
        return q.all()

# 10. Список курсів, які читає конкретний викладач
def select_10(teacher_id: int, student_id: int):
    with session_scope() as s:
        q = (
            s.query(Subject.id, Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .group_by(Subject.id)
        )
        return q.all()

# Екстра 1. Середній бал конкретного студента по конкретному викладачу
def extra_1(teacher_id: int, student_id: int):
    with session_scope() as s:
        (avg_val,) = (
            s.query(func.round(func.avg(Grade.grade), 2))
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        ).one()
        return avg_val

# Екстра 2. Оцінки в групі за предметом на останньому уроці (остання graded_at для студента)
def extra_2(group_id: int, subject_id: int):
    with session_scope() as s:
        # остання оцінка для студента за предметом
        subq = (
            s.query(Grade.student_id, func.max(Grade.graded_at).label("max_time"))
            .join(Student, Student.id == Grade.student_id)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .group_by(Grade.student_id)
        ).subquery()

        q = (
            s.query(Student.id, Student.name, Grade.grade, Grade.graded_at)
            .join(subq, (subq.c.student_id == Student.id))
            .join(Grade, (Grade.student_id == subq.c.student_id) & (Grade.graded_at == subq.c.max_time) & (Grade.subject_id == subject_id))
            .order_by(Student.id)
        )
        return q.all()

if __name__ == "__main__":
    # Демонстраційний запуск усіх запитів
    print("1.", select_1())
    print()
    print("2.", select_2(subject_id=1))
    print()
    print("3.", select_3(subject_id=1))
    print()
    print("4.", select_4())
    print()
    print("5.", select_5(teacher_id=1))
    print()
    print("6.", select_6(group_id=1))
    print()
    print("7.", select_7(group_id=1, subject_id=1))
    print()
    print("8.", select_8(teacher_id=1))
    print()
    print("9.", select_9(student_id=1))
    print()
    print("10.", select_10(teacher_id=1, student_id=1))
    print()
    print("E1.", extra_1(teacher_id=1, student_id=1))
    print()
    print("E2.", extra_2(group_id=1, subject_id=1))
