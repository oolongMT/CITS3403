"""trying out new db relationship method

Revision ID: 59b9225533ed
Revises: 
Create Date: 2021-05-17 13:04:49.896729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59b9225533ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('section', sa.String(length=128), nullable=True),
    sa.Column('question', sa.String(length=128), nullable=True),
    sa.Column('correct_answer', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('question_id'),
    sa.UniqueConstraint('question')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_admin'), ['admin'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('answer',
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=128), nullable=True),
    sa.Column('question_id_fk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id_fk'], ['question.question_id'], ),
    sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table('mark',
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.Column('question_id_fk', sa.Integer(), nullable=False),
    sa.Column('user_id_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id_fk'], ['question.question_id'], ),
    sa.ForeignKeyConstraint(['user_id_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('question_id_fk', 'user_id_fk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mark')
    op.drop_table('answer')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_admin'))

    op.drop_table('user')
    op.drop_table('question')
    # ### end Alembic commands ###
