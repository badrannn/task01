import google.generativeai as genai


class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        genai.configure(api_key="AIzaSyAjA17zRzYyUgpnpMBcAyzCDJDBUJwGe7w")

    def get_response(
        self,
        prompt: str = "",
    ):
        response = self.model.generate_content(prompt)

        return response.text
