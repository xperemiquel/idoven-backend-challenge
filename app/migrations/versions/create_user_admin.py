"""Add user to UserAdmin group

Revision ID: 123456789abc
Revises: abcdef123456
Create Date: 2024-02-10 15:00:00.000000

"""
from alembic import op
import sqlalchemy
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision = "123456789abc"
down_revision = "abcdef123456"
branch_labels = None
depends_on = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("password")

email = "admin@idoven.com"


def upgrade():
    # Step 1: Insert the new user
    op.execute(
        sqlalchemy.text(
            "INSERT INTO users (email, password) VALUES (:email, :hashed_password) RETURNING id"
        ).bindparams(email=email, hashed_password=hashed_password)
    )

    # Step 2: Associate the user with the UserAdmin group
    op.execute(
        sqlalchemy.text(
            "INSERT INTO user_permission_groups (user_id, permission_group_id) "
            "VALUES ((SELECT id FROM users WHERE email = :email), (SELECT id FROM permission_groups WHERE name = 'UserAdmin'))"
        ).bindparams(email=email)
    )


def downgrade():
    # Step 1: Remove the user from the UserAdmin group
    op.execute(
        sqlalchemy.text(
            "DELETE FROM user_permission_groups WHERE user_id = (SELECT id FROM users WHERE email = :email)"
        ).bindparams(email=email)
    )

    # Step 2: Delete the user
    op.execute(
        sqlalchemy.text("DELETE FROM users WHERE email = :email").bindparams(
            email=email
        )
    )
