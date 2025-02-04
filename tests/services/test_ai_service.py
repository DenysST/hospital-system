import pytest
from unittest.mock import MagicMock, mock_open, patch
from app.services.ai_service import GeminiService
from app.consts import MESSAGE


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.generate_content = MagicMock()
    return model


@pytest.fixture
def service(mock_model):
    with patch("builtins.open", mock_open(read_data="Mocked prompt")):
        mock_model.generate_content.return_value.text = f'{{"{MESSAGE}": "I am ready to help"}}'
        return GeminiService(mock_model)


def test_gemini_service_setup_success(mock_model):
    mock_model.generate_content.return_value.text = f'{{"{MESSAGE}": "I am ready to help"}}'
    with patch("builtins.open", mock_open(read_data="Mocked prompt")):
        service = GeminiService(mock_model)
    mock_model.generate_content.assert_called_once_with("Mocked prompt")

def test_gemini_service_setup_failure_invalid_message(mock_model):
    mock_model.generate_content.return_value.text = f'{{"{MESSAGE}": "Unexpected message"}}'
    with patch("builtins.open", mock_open(read_data="Mocked prompt")):
        with pytest.raises(RuntimeError, match="Gemini setup failed. Please check the prompt file."):
            GeminiService(mock_model)
    mock_model.generate_content.assert_called_once_with("Mocked prompt")

def test_get_assignment_success(service, mock_model):
    mock_model.generate_content.return_value.text = '{"department": "Cardiology"}'
    mock_model.generate_content.reset_mock()  # Reset the mock to isolate this test
    result = service.get_assigment("Patient has chest pain.")
    assert result == {"department": "Cardiology"}
    mock_model.generate_content.assert_called_once_with("Mocked prompt".replace("<patient_problem>", "Patient has chest pain."))

def test_get_assignment_failure_invalid_json(service, mock_model):
    mock_model.generate_content.return_value.text = "Invalid JSON Response"
    mock_model.generate_content.reset_mock()  # Reset the mock to isolate this test
    with pytest.raises(RuntimeError, match="Invalid response from Gemini model."):
        service.get_assigment("Patient has chest pain.")
    mock_model.generate_content.assert_called_once_with("Mocked prompt".replace("<patient_problem>", "Patient has chest pain."))
