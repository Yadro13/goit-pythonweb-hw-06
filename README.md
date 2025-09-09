# University DB Project (PostgreSQL + SQLAlchemy + Alembic)

This project implements a simple university database schema and utilities:

- **Tables**: students, groups, teachers, subjects (with teacher), grades (with timestamp)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Seeder**: `seed.py` with Faker
- **Queries**: `my_select.py` (10 required + 2 extra)
- **CLI CRUD**: `main.py` using argparse

## 0) Run Postgres with Docker

```bash
docker run --name my-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

> Replace `my-postgres` and `mysecretpassword` as you wish.

## 1) Configure connection

Edit `.env` (already included) or export env var:

```
DATABASE_URL=postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres
```

You can also change DB/port/user/password.

## 2) Create virtual environment & install deps

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Run Alembic migrations

The repository has an **initial migration** pre-created.

```bash
alembic upgrade head
```

If you change models, create a new migration:

```bash
alembic revision --autogenerate -m "update"
alembic upgrade head
```

## 4) Seed database with fake data

```bash
python seed.py
```

By default creates 3 groups, 3–5 teachers, 5–8 subjects, 30–50 students, and up to 20 grades per student.

Options:
```bash
python seed.py --students 40 --groups 3 --teachers 4 --subjects 6 --max-grades 20
```

## 5) Run the 10 required queries

```bash
python my_select.py
```

It will print results for `select_1`..`select_10` and extra queries.

You can also import and call specific functions.

## 6) CLI CRUD

Examples:

```bash
# Create teacher
python main.py -a create -m Teacher -n "Boris Jonson"

# List teachers
python main.py -a list -m Teacher

# Update teacher 3
python main.py -a update -m Teacher --id 3 -n "Andry Bezos"

# Remove teacher 3
python main.py -a remove -m Teacher --id 3

# Create group
python main.py -a create -m Group -n "AD-101"

# Create student (requires group id)
python main.py -a create -m Student -n "John Doe" --group-id 1

# Create subject (requires teacher id)
python main.py -a create -m Subject -n "Linear Algebra" --teacher-id 1

# Create grade (requires student & subject)
python main.py -a create -m Grade --student-id 1 --subject-id 2 --grade 95
```
# goit-pythonweb-hw-06
