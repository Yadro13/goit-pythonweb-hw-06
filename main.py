import argparse
from typing import Optional
from tabulate import tabulate
from db import session_scope
from models import Teacher, Group, Student, Subject, Grade

def create_teacher(name: str):
    with session_scope() as s:
        t = Teacher(name=name)
        s.add(t)
        s.flush()
        print(f"Created Teacher id={t.id} name={t.name}")

def list_teachers():
    with session_scope() as s:
        items = s.query(Teacher).order_by(Teacher.id).all()
        print(tabulate([(i.id, i.name) for i in items], headers=["id", "name"]))

def update_teacher(id: int, name: str):
    with session_scope() as s:
        t = s.get(Teacher, id)
        if not t:
            print("Teacher not found"); return
        t.name = name
        print(f"Updated Teacher id={t.id} name={t.name}")

def remove_teacher(id: int):
    with session_scope() as s:
        t = s.get(Teacher, id)
        if not t:
            print("Teacher not found"); return
        s.delete(t)
        print(f"Removed Teacher id={id}")

def create_group(name: str):
    with session_scope() as s:
        g = Group(name=name)
        s.add(g); s.flush()
        print(f"Created Group id={g.id} name={g.name}")

def list_groups():
    with session_scope() as s:
        items = s.query(Group).order_by(Group.id).all()
        print(tabulate([(i.id, i.name) for i in items], headers=["id","name"]))

def update_group(id: int, name: str):
    with session_scope() as s:
        g = s.get(Group, id)
        if not g:
            print("Group not found"); return
        g.name = name
        print(f"Updated Group id={g.id} name={g.name}")

def remove_group(id: int):
    with session_scope() as s:
        g = s.get(Group, id)
        if not g:
            print("Group not found"); return
        s.delete(g)
        print(f"Removed Group id={id}")

def create_student(name: str, group_id: Optional[int] = None):
    with session_scope() as s:
        st = Student(name=name, group_id=group_id)
        s.add(st); s.flush()
        print(f"Created Student id={st.id} name={st.name} group_id={st.group_id}")

def list_students():
    with session_scope() as s:
        items = s.query(Student).order_by(Student.id).all()
        print(tabulate([(i.id, i.name, i.group_id) for i in items], headers=["id","name","group_id"]))

def update_student(id: int, name: Optional[str] = None, group_id: Optional[int] = None):
    with session_scope() as s:
        st = s.get(Student, id)
        if not st:
            print("Student not found"); return
        if name is not None:
            st.name = name
        if group_id is not None:
            st.group_id = group_id
        print(f"Updated Student id={st.id} name={st.name} group_id={st.group_id}")

def remove_student(id: int):
    with session_scope() as s:
        st = s.get(Student, id)
        if not st:
            print("Student not found"); return
        s.delete(st)
        print(f"Removed Student id={id}")

def create_subject(name: str, teacher_id: Optional[int] = None):
    with session_scope() as s:
        sb = Subject(name=name, teacher_id=teacher_id)
        s.add(sb); s.flush()
        print(f"Created Subject id={sb.id} name={sb.name} teacher_id={sb.teacher_id}")

def list_subjects():
    with session_scope() as s:
        items = s.query(Subject).order_by(Subject.id).all()
        print(tabulate([(i.id, i.name, i.teacher_id) for i in items], headers=["id","name","teacher_id"]))

def update_subject(id: int, name: Optional[str] = None, teacher_id: Optional[int] = None):
    with session_scope() as s:
        sb = s.get(Subject, id)
        if not sb:
            print("Subject not found"); return
        if name is not None:
            sb.name = name
        if teacher_id is not None:
            sb.teacher_id = teacher_id
        print(f"Updated Subject id={sb.id} name={sb.name} teacher_id={sb.teacher_id}")

def remove_subject(id: int):
    with session_scope() as s:
        sb = s.get(Subject, id)
        if not sb:
            print("Subject not found"); return
        s.delete(sb)
        print(f"Removed Subject id={id}")

def create_grade(student_id: int, subject_id: int, grade: int):
    with session_scope() as s:
        gr = Grade(student_id=student_id, subject_id=subject_id, grade=grade)
        s.add(gr); s.flush()
        print(f"Created Grade id={gr.id} student_id={gr.student_id} subject_id={gr.subject_id} grade={gr.grade}")

def list_grades():
    with session_scope() as s:
        items = s.query(Grade).order_by(Grade.id).all()
        print(tabulate([(i.id, i.student_id, i.subject_id, i.grade, i.graded_at) for i in items],
                       headers=["id","student_id","subject_id","grade","graded_at"]))

def remove_grade(id: int):
    with session_scope() as s:
        gr = s.get(Grade, id)
        if not gr:
            print("Grade not found"); return
        s.delete(gr)
        print(f"Removed Grade id={id}")

def main():
    parser = argparse.ArgumentParser(description="CLI CRUD for University DB")
    parser.add_argument("-a", "--action", choices=["create","list","update","remove"], required=True)
    parser.add_argument("-m", "--model", choices=["Teacher","Group","Student","Subject","Grade"], required=True)
    parser.add_argument("-n", "--name", help="Name value for create/update where applicable")
    parser.add_argument("--id", type=int, help="Entity id for update/remove")
    parser.add_argument("--group-id", type=int)
    parser.add_argument("--teacher-id", type=int)
    parser.add_argument("--student-id", type=int)
    parser.add_argument("--subject-id", type=int)
    parser.add_argument("--grade", type=int)

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create": create_teacher(args.name)
        elif args.action == "list": list_teachers()
        elif args.action == "update": update_teacher(args.id, args.name)
        elif args.action == "remove": remove_teacher(args.id)

    elif args.model == "Group":
        if args.action == "create": create_group(args.name)
        elif args.action == "list": list_groups()
        elif args.action == "update": update_group(args.id, args.name)
        elif args.action == "remove": remove_group(args.id)

    elif args.model == "Student":
        if args.action == "create": create_student(args.name, args.group_id)
        elif args.action == "list": list_students()
        elif args.action == "update": update_student(args.id, args.name, args.group_id)
        elif args.action == "remove": remove_student(args.id)

    elif args.model == "Subject":
        if args.action == "create": create_subject(args.name, args.teacher_id)
        elif args.action == "list": list_subjects()
        elif args.action == "update": update_subject(args.id, args.name, args.teacher_id)
        elif args.action == "remove": remove_subject(args.id)

    elif args.model == "Grade":
        if args.action == "create": create_grade(args.student_id, args.subject_id, args.grade)
        elif args.action == "list": list_grades()
        elif args.action == "remove": remove_grade(args.id)
        else:
            print("Update for Grade is not supported in this demo (grades are immutable)")

if __name__ == "__main__":
    main()
