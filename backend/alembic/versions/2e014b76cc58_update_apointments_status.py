"""update apointments status

Revision ID: 2e014b76cc58
Revises: 37ac408ad845
Create Date: 2024-06-27 18:41:21.114647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_postgresql_enum import TableReference

# revision identifiers, used by Alembic.
revision: str = '2e014b76cc58'
down_revision: Union[str, None] = '37ac408ad845'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'appointmentstatus', ['PENDING', 'COMPLETED', 'CANCELLED', 'BOOKED'],
                        [TableReference(table_schema='public', table_name='appointment', column_name='status')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'appointmentstatus', ['PENDING', 'ACCEPTED', 'CANCELLED'],
                        [TableReference(table_schema='public', table_name='appointment', column_name='status')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###
