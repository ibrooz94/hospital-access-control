"""create appointment table

Revision ID: f1d8f0ddc280
Revises: e7a6ed384fd5
Create Date: 2024-04-17 23:05:34.495237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import fastapi_users_db_sqlalchemy

# revision identifiers, used by Alembic.
revision: str = 'f1d8f0ddc280'
down_revision: Union[str, None] = 'e7a6ed384fd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('PENDING', 'ACCEPTED', 'CANCELLED', name='appointmentstatus').create(op.get_bind())
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requested_by', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('on_behalf_of', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('scheduled_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'ACCEPTED', 'CANCELLED', name='appointmentstatus', create_type=False), nullable=False),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('assigned_doctor', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['assigned_doctor'], ['user.id'], name=op.f('fk_appointment_assigned_doctor_user')),
    sa.ForeignKeyConstraint(['on_behalf_of'], ['user.id'], name=op.f('fk_appointment_on_behalf_of_user')),
    sa.ForeignKeyConstraint(['requested_by'], ['user.id'], name=op.f('fk_appointment_requested_by_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_appointment'))
    )
    op.create_index(op.f('ix_appointment_id'), 'appointment', ['id'], unique=False)
    op.add_column('visit', sa.Column('appointment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_visit_appointment_id_appointment'), 'visit', 'appointment', ['appointment_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_visit_appointment_id_appointment'), 'visit', type_='foreignkey')
    op.drop_column('visit', 'appointment_id')
    op.drop_index(op.f('ix_appointment_id'), table_name='appointment')
    op.drop_table('appointment')
    sa.Enum('PENDING', 'ACCEPTED', 'CANCELLED', name='appointmentstatus').drop(op.get_bind())
    # ### end Alembic commands ###
