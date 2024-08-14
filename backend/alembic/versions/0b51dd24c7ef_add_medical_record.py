"""add medical record

Revision ID: 0b51dd24c7ef
Revises: 2e014b76cc58
Create Date: 2024-07-04 04:51:22.918902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_postgresql_enum import TableReference
import fastapi_users_db_sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '0b51dd24c7ef'
down_revision: Union[str, None] = '2e014b76cc58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], name=op.f('fk_medical_record_patient_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_medical_record'))
    )
    op.create_index(op.f('ix_medical_record_id'), 'medical_record', ['id'], unique=False)
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('can_view', sa.Boolean(), nullable=False),
    sa.Column('can_edit', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['medical_record.id'], name=op.f('fk_permission_record_id_medical_record')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_permission_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_permission'))
    )
    op.sync_enum_values('public', 'appointmentstatus', ['PENDING', 'BOOKED', 'COMPLETED', 'CANCELLED'],
                        [TableReference(table_schema='public', table_name='appointment', column_name='status')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'appointmentstatus', ['PENDING', 'COMPLETED', 'CANCELLED', 'BOOKED'],
                        [TableReference(table_schema='public', table_name='appointment', column_name='status')],
                        enum_values_to_rename=[])
    op.drop_table('permission')
    op.drop_index(op.f('ix_medical_record_id'), table_name='medical_record')
    op.drop_table('medical_record')
    # ### end Alembic commands ###
