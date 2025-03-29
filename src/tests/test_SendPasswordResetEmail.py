import pytest

from services import SendPasswordResetEmail

@pytest.mark.email
def test_SendPasswordResetEmail():

    response = SendPasswordResetEmail("ruanazeredo@gmail.com", "1234567890abcdef1234567890abcdef1234567890abcdef")
    print(response)
    assert response["message"] == "Email sent successfully"
