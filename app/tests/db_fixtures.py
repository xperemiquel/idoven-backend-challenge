import datetime

from models.models import User, PermissionGroup, ECG, Lead, LeadAnalysis
from ecg.processors import calculate_zero_crossings
from auth.security import get_password_hash
import uuid


def data_to_model(model, datas):
    models = list()
    for data in datas:
        models.append(model(**data))
    return models


_permission_groups = [
    {
        "id": 1,
        "name": "UserAdmin",
        "permissions": ["user:create", "user:read", "user:update", "user:delete"],
    },
    {
        "id": 2,
        "name": "ECGOperator",
        "permissions": ["user:create", "user:read", "user:update", "user:delete"],
    },
]

permission_groups = data_to_model(PermissionGroup, _permission_groups)

_users = [
    {
        "id": 2,
        "email": "admin@admin.com",
        "password": get_password_hash("password"),
        "groups": [permission_groups[0]],
    },
    {
        "id": 3,
        "email": "ecgoperator1@company.com",
        "password": get_password_hash("password"),
        "groups": [permission_groups[1]],
    },
]

users = data_to_model(User, _users)

_ecgs = [
    {
        "id": uuid.uuid4(),
        "processed": True,
        "date": datetime.datetime.now(),
        "owner": users[1],
    },
    {
        "id": uuid.uuid4(),
        "processed": False,
        "date": datetime.datetime.now(),
        "owner": users[1],
    },
]

ecgs = data_to_model(ECG, _ecgs)

_leads = [
    #  Processed ECG
    {
        "id": 10,
        "name": "Lead I",
        "number_of_samples": 5,
        "signal": [1, -1, 1, -1, 1],
        "ecg_id": ecgs[0].id,
    },
    {
        "id": 11,
        "name": "Lead II",
        "number_of_samples": 5,
        "signal": [2, -2, 2, -2, 2],
        "ecg_id": ecgs[0].id,
    },
    {
        "id": 12,
        "name": "Lead III",
        "number_of_samples": 5,
        "signal": [3, -3, 3, -3, 3],
        "ecg_id": ecgs[0].id,
    },
    #  Unprocessed ECG
    {
        "id": 13,
        "name": "Lead I",
        "number_of_samples": 5,
        "signal": [1, -1, 1, -1, 1],
        "ecg_id": ecgs[1].id,
    },
    {
        "id": 14,
        "name": "Lead II",
        "number_of_samples": 5,
        "signal": [2, -2, 2, -2, 2],
        "ecg_id": ecgs[1].id,
    },
    {
        "id": 15,
        "name": "Lead III",
        "number_of_samples": 5,
        "signal": [3, -3, 3, -3, 3],
        "ecg_id": ecgs[1].id,
    },
]

leads = data_to_model(Lead, _leads)

_lead_analysis = [
    {
        "id": index + 1,
        "lead": leads[index],
        "num_zero_crosses": calculate_zero_crossings(lead.signal),
    }
    for index, lead in enumerate(leads)
]

lead_analysis = data_to_model(LeadAnalysis, _lead_analysis)
