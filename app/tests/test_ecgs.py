from ecg.processors import process_ecg
import uuid
from models.models import ECG, User
from .dummy_data import ecgs_data


def test_admin_can_not_create_ecgs(db_session, authenticated_user_admin_client):
    response = authenticated_user_admin_client.post("/api/v1/ecgs", json=ecgs_data)
    assert response.status_code == 403


def test_ecg_operator_can_create_ecgs(db_session, authenticated_ecg_operator_client):
    response = authenticated_ecg_operator_client.post("/api/v1/ecgs", json=ecgs_data)
    assert response.status_code == 200


def test_background_task_is_being_queued(
    db_session, authenticated_ecg_operator_client, mocker
):
    mock_add_task = mocker.patch("fastapi.BackgroundTasks.add_task")
    response = authenticated_ecg_operator_client.post("/api/v1/ecgs", json=ecgs_data)
    new_ecg_id = uuid.UUID(response.json()["ecg_id"])
    mock_add_task.assert_called_once_with(process_ecg, new_ecg_id)


def test_ecg_user_cannot_read_unprocessed_ecg_analysis(
    db_session, authenticated_ecg_operator_client
):
    ecg_id = (
        db_session.query(ECG)
        .filter(ECG.user_id == 3, ECG.processed == False)
        .first()
        .id
    )
    response = authenticated_ecg_operator_client.get(f"/api/v1/ecgs/{str(ecg_id)}")
    assert response.status_code == 204


def test_ecg_user_can_read_processed_ecg_analysis(
    db_session, authenticated_ecg_operator_client
):
    ecg_id = (
        db_session.query(ECG).filter(ECG.user_id == 3, ECG.processed == True).first().id
    )
    response = authenticated_ecg_operator_client.get(f"/api/v1/ecgs/{str(ecg_id)}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == str(ecg_id)
    assert len(json_response["leads"]) == 3
