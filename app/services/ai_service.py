from json import JSONDecodeError, loads
from google.generativeai import GenerativeModel
from app.consts import MESSAGE
from app.exceptions import GeminiException

class GeminiService:
    def __init__(self, model: GenerativeModel):
        self._model = model
        self._patient_basic_prompt = None

        self._setup_gemini()


    def get_assigment(self, prompt: str):
        try:
            patient_prompt = self._patient_basic_prompt.replace("<patient_problem>", prompt)
            response = self._model.generate_content(patient_prompt)
            return loads(response.text.strip())
        except JSONDecodeError as e:
            raise GeminiException("Invalid response from Gemini model.", e)

    def _setup_gemini(self):
        with open("resources/gemini_setup_prompt.txt", "r") as file:
            prompt = file.read()

        with open("resources/gemini_patient_prompt.txt", "r") as file:
            self._patient_basic_prompt = file.read()

        response = self._model.generate_content(prompt)
        try:
            response_message = loads(response.text.strip())[MESSAGE]
            if response_message == "I am ready to help":
                print("Gemini setup successful.")
            else:
                print("Gemini setup failed. Expected response message: 'I am ready to help', but got", response_message)
                raise GeminiException("Gemini setup failed. Please check the prompt file.")
        except JSONDecodeError:
            print("Gemini setup failed. Expected json serializable response, but got:", response.text)
            raise GeminiException("Gemini setup failed. Got non-json serializable response. Please check the prompt file.")
