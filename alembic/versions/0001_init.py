"""init schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-09-08 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=64), nullable=False, unique=True),
    )

    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False),
    )

    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey('groups.id', ondelete="SET NULL"), nullable=True),
    )

    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('teacher_id', sa.Integer(), sa.ForeignKey('teachers.id', ondelete="SET NULL"), nullable=True),
        sa.UniqueConstraint('name', name='uq_subject_name'),
    )

    op.create_table(
        'grades',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('students.id', ondelete="CASCADE"), nullable=False),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.Column('graded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint('grade BETWEEN 0 AND 100', name='ck_grade_range'),
        sa.UniqueConstraint('student_id', 'subject_id', 'graded_at', name='uq_grade_unique_time'),
    )

def downgrade():
    op.drop_table('grades')
    op.drop_table('subjects')
    op.drop_table('students')
    op.drop_table('teachers')
    op.drop_table('groups')
