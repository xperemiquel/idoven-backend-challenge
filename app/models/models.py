import uuid
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
    ARRAY,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

Base = declarative_base()

user_groups = Table(
    "user_permission_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column(
        "permission_group_id",
        Integer,
        ForeignKey("permission_groups.id"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    groups = relationship("PermissionGroup", secondary=user_groups, backref="users")


class PermissionGroup(Base):
    __tablename__ = "permission_groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(ARRAY(String))


class ECG(Base):
    __tablename__ = "ecgs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)

    owner = relationship("User", backref=backref("ecgs", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<ECG {self.id} recorded by {self.user.email} on {self.date}>"


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    ecg_id = Column(UUID(as_uuid=True), ForeignKey("ecgs.id"))
    name = Column(String(10))
    number_of_samples = Column(Integer, nullable=True)
    signal = Column(JSON)

    ecg = relationship("ECG", backref=backref("leads", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<{self.name} for ECG {self.ecg_id}>"


class LeadAnalysis(Base):
    __tablename__ = "lead_analysis"
    id = Column(Integer, ForeignKey("leads.id"), primary_key=True)
    num_zero_crosses = Column(Integer)

    lead = relationship(
        "Lead", backref=backref("analysis", uselist=False, cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<Analysis for Lead {self.id}>"
