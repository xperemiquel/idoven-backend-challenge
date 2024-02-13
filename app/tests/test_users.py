from .dummy_data import user_data


def test_admin_can_create_user(authenticated_user_admin_client):
    response = authenticated_user_admin_client.post("/api/v1/users", json=user_data)
    assert response.status_code == 200


def test_ecg_operator_can_not_create_users(authenticated_ecg_operator_client):
    response = authenticated_ecg_operator_client.post("/api/v1/users", json=user_data)
    assert response.status_code == 403
