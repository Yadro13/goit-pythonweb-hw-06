import argparse
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from db import session_scope
from models import Group, Teacher, Student, Subject, Grade

def seed(students_n: int = 40, groups_n: int = 3, teachers_n: int = 4, subjects_n: int = 6, max_grades_per_student: int = 20) -> None:
    fake = Faker()
    with session_scope() as s:
        # Очистка таблиць (для простоти)
        s.query(Grade).delete()
        s.query(Subject).delete()
        s.query(Student).delete()
        s.query(Teacher).delete()
        s.query(Group).delete()

        # Групи
        groups = [Group(name=f"AD-{i:03d}") for i in range(101, 101 + groups_n)]
        s.add_all(groups)
        s.flush()

        # Викладачі
        teachers = [Teacher(name=fake.name()) for _ in range(teachers_n)]
        s.add_all(teachers)
        s.flush()

        # Предмети
        subject_names = [
            "Mathematics", "Physics", "Chemistry", "Biology", "History",
            "Literature", "Philosophy", "Computer Science", "Economics",
        ]
        random.shuffle(subject_names)
        subjects = []
        for i in range(subjects_n):
            subjects.append(Subject(name=subject_names[i], teacher=random.choice(teachers)))
        s.add_all(subjects)
        s.flush()

        # Студенти
        students = []
        for _ in range(students_n):
            students.append(Student(name=fake.name(), group=random.choice(groups)))
        s.add_all(students)
        s.flush()

        # Оцінки
        for st in students:
            num_grades = random.randint(max(5, max_grades_per_student // 2), max_grades_per_student)
            for _ in range(num_grades):
                subj = random.choice(subjects)
                grade_val = random.randint(60, 100)
                days_ago = random.randint(0, 180)
                t = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                s.add(Grade(student_id=st.id, subject_id=subj.id, grade=grade_val, graded_at=t))

        # Комміт відбувається в session_scope()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed PostgreSQL database with fake data.")
    parser.add_argument("--students", type=int, default=40)
    parser.add_argument("--groups", type=int, default=3)
    parser.add_argument("--teachers", type=int, default=4)
    parser.add_argument("--subjects", type=int, default=6)
    parser.add_argument("--max-grades", type=int, default=20)
    args = parser.parse_args()

    seed(args.students, args.groups, args.teachers, args.subjects, args.max_grades)
    print("Seeding done.")
