import os
from json import JSONDecodeError, loads
import google.generativeai as genai
from app.config import SingletonMeta
from app.consts import GEMINI_MODEL, MESSAGE
from app.exceptions import GeminiException

class GeminiService(metaclass=SingletonMeta):
    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self._model = genai.GenerativeModel(GEMINI_MODEL)
        self._patient_basic_prompt = None
        self._setup_gemini()


    def get_assigment(self, prompt: str):
        try:
            patient_prompt = self._patient_basic_prompt.replace("<patient_problem>", prompt)
            response = self._model.generate_content(patient_prompt)
            return loads(response.text.strip())
        except JSONDecodeError as e:
            print("Invalid response from Gemini model.")
            raise GeminiException("Invalid response from Gemini model.", e)

    def _setup_gemini(self):
        with open("gemini_setup_prompt.txt", "r") as file:
            prompt = file.read()

        with open("gemini_patient_prompt.txt", "r") as file:
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
