"""Add UserAdmin and ECG groups

Revision ID: abcdef123456
Revises: 73ef6c05a3a1
Create Date: 2024-02-10 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "abcdef123456"
down_revision = "73ef6c05a3a1"
branch_labels = None
depends_on = None


def upgrade():
    # Use op.execute to perform raw SQL operations
    op.execute(
        """
        INSERT INTO permission_groups (name, permissions) VALUES
        ('UserAdmin', '{"user:create", "user:read", "user:update", "user:delete"}'),
        ('ECGOperator', '{"ecg:create", "ecg:read"}');
        """
    )


def downgrade():
    # Use op.execute to revert the changes made in the upgrade function
    op.execute(
        "DELETE FROM permission_groups WHERE name IN ('UserAdmin', 'ECGOperator');"
    )
