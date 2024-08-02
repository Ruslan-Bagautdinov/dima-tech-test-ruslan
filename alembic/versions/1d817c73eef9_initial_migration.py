"""Initial migration

Revision ID: 1d817c73eef9
Revises: 
Create Date: 2024-08-02 07:19:19.349182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d817c73eef9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('email', sa.String, unique=True, index=True),
            sa.Column('hashed_password', sa.String),
            sa.Column('full_name', sa.String),
            sa.Column('role', sa.String, default="user"),
        )

    if 'accounts' not in inspector.get_table_names():
        op.create_table(
            'accounts',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('balance', sa.Float, default=0.0),
            sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE")),
        )

    # Insert initial data
    users_table = sa.table(
        'users',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String),
        sa.column('hashed_password', sa.String),
        sa.column('full_name', sa.String),
        sa.column('role', sa.String),
    )
    op.bulk_insert(users_table, [
        {
            'id': 1,
            'email': 'admin@example.com',
            'hashed_password': '$2b$12$9gy5Tj7Hiq4KJEWwU4YYueEoYxdqVPms4NVQMg1C1//p.y8VdBf5m',
            'full_name': 'Админ Админович Админов',
            'role': 'admin',
        },
        {
            'id': 2,
            'email': 'user@example.com',
            'hashed_password': '$2b$12$HeUMonCS4oS6a1akkcRFh.ggT1bbZu9H4T8asUbPcotHnJPm3BCJe',
            'full_name': 'Юзер Юзерович Юзеров',
            'role': 'user',
        },
    ])

    accounts_table = sa.table(
        'accounts',
        sa.column('id', sa.Integer),
        sa.column('owner_id', sa.Integer),
        sa.column('balance', sa.Float),
    )
    op.bulk_insert(accounts_table, [
        {
            'id': 1,
            'owner_id': 2,
            'balance': 999.99,
        },
    ])

def downgrade():
    op.drop_table('accounts')
    op.drop_table('users')
