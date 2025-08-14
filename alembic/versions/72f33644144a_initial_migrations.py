"""Initial Migrations

Revision ID: 72f33644144a
Revises: 
Create Date: 2025-08-14 14:31:19.540152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '72f33644144a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    postgresql.ENUM('admin', 'customer', name='user_type').create(bind)
    postgresql.ENUM('pending', 'completed', 'cancelled', name='order_status').create(bind)
    postgresql.ENUM('read', 'unread', name='notification_status').create(bind)
    postgresql.ENUM('main_courses', 'drinks', 'other', name='menu_category').create(bind)
    op.create_table('admins',
    sa.Column('employee_id', sa.String(), nullable=True),
    sa.Column('user_type', postgresql.ENUM('admin', 'customer', name='user_type', create_type=False), server_default=sa.text("'admin'::user_type"), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admins_email'), 'admins', ['email'], unique=True)
    op.create_index(op.f('ix_admins_employee_id'), 'admins', ['employee_id'], unique=False)
    op.create_table('customers',
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('user_type', postgresql.ENUM('admin', 'customer', name='user_type', create_type=False), server_default=sa.text("'customer'::user_type"), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=True)
    op.create_table('menu',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.DECIMAL(), nullable=False),
    sa.Column('category', postgresql.ENUM('main_courses', 'drinks', 'other', name='menu_category', create_type=False), server_default=sa.text("'other'::menu_category"), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('thumbnail', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_name'), 'menu', ['name'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('detail', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_type', sa.String(), nullable=True),
    sa.Column('status', postgresql.ENUM('read', 'unread', name='notification_status', create_type=False), server_default=sa.text("'unread'::notification_status"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('amount', sa.DECIMAL(), nullable=False),
    sa.Column('status', postgresql.ENUM('pending', 'completed', 'cancelled', name='order_status', create_type=False), server_default=sa.text("'pending'::order_status"), nullable=False),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.UUID(), nullable=False),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_menu',
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('menu_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id', 'menu_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    bind = op.get_bind()
    op.drop_table('order_menu')
    op.drop_table('reviews')
    op.drop_table('orders')
    op.drop_table('notifications')
    op.drop_table('messages')
    op.drop_index(op.f('ix_menu_name'), table_name='menu')
    op.drop_table('menu')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_admins_employee_id'), table_name='admins')
    op.drop_index(op.f('ix_admins_email'), table_name='admins')
    op.drop_table('admins')
    postgresql.ENUM('main_courses', 'drinks', 'other', name='menu_category').drop(bind)
    postgresql.ENUM('read', 'unread', name='notification_status').drop(bind)
    postgresql.ENUM('pending', 'completed', 'cancelled', name='order_status').drop(bind)
    postgresql.ENUM('admin', 'customer', name='user_type').drop(bind)
    # ### end Alembic commands ###
