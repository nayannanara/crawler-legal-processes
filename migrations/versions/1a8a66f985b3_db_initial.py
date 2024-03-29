"""db_initial

Revision ID: 1a8a66f985b3
Revises:
Create Date: 2023-03-31 07:20:35.655847
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1a8a66f985b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'processes',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('process_number', sa.String(), nullable=False),
        sa.Column('class_', sa.String(), nullable=True),
        sa.Column('area', sa.String(), nullable=True),
        sa.Column('topic', sa.String(), nullable=True),
        sa.Column('distribution_date', sa.DateTime(), nullable=True),
        sa.Column('judge', sa.String(), nullable=True),
        sa.Column('stock_price', sa.String(), nullable=True),
        sa.Column(
            'process_parties',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column('degree', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_processes_id'), 'processes', ['id'], unique=False)
    op.create_table(
        'movimentations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('process_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ['process_id'],
            ['processes.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_movimentations_process_id'),
        'movimentations',
        ['process_id'],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f('ix_movimentations_process_id'), table_name='movimentations'
    )
    op.drop_table('movimentations')
    op.drop_index(op.f('ix_processes_id'), table_name='processes')
    op.drop_table('processes')
    # ### end Alembic commands ###
