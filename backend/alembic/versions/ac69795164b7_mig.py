"""mig

Revision ID: ac69795164b7
Revises: 
Create Date: 2023-12-02 10:02:39.269244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac69795164b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('airport_from', sa.String(), nullable=True),
    sa.Column('airport_in', sa.String(), nullable=True),
    sa.Column('date_from', sa.DateTime(), nullable=True),
    sa.Column('date_in', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_description'), 'ticket', ['description'], unique=False)
    op.create_index(op.f('ix_ticket_title'), 'ticket', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ticket_title'), table_name='ticket')
    op.drop_index(op.f('ix_ticket_description'), table_name='ticket')
    op.drop_table('ticket')
    # ### end Alembic commands ###