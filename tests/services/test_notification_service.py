import pytest
from flask_mail import Mail
from app.services.notification_service import NotificationService


@pytest.fixture
def mock_mail(mocker):
    return mocker.create_autospec(Mail)

@pytest.fixture
def service(mock_mail):
    return NotificationService(mock_mail)


def test_send_email_success(service, mock_mail, mocker):
    mock_message = mocker.patch("app.services.notification_service.Message")

    recipient = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"

    result = service.send_email(recipient, subject, body)

    assert result is True
    mock_message.assert_called_once_with(subject, recipients=[recipient], body=body)
    mock_mail.send.assert_called_once_with(mock_message.return_value)

def test_send_email_failure(service, mock_mail, mocker):
    mock_message = mocker.patch("app.services.notification_service.Message")
    mock_mail.send.side_effect = Exception("SMTP server not reachable")

    recipient = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"

    result = service.send_email(recipient, subject, body)

    assert result is False
    mock_message.assert_called_once_with(subject, recipients=[recipient], body=body)
    mock_mail.send.assert_called_once_with(mock_message.return_value)
