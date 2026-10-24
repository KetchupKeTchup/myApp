import json
from PIL import Image
from google import genai

class AiService:
    def __init__(self, api_key):
        # Ініціалізація клієнта за новим стандартом
        self.client = genai.Client(api_key=api_key)

    def analyze_food_label(self, image_path):
        """Зчитує фото і повертає JSON із БЖВ"""
        try:
            img = Image.open(image_path)
            
            prompt = """
            Це фото етикетки продукту. Знайди калорійність (kcal), білки, вуглеводи та жири на 100 грамів.
            Поверни відповідь СУВОРО у форматі JSON без жодного додаткового тексту, форматування чи маркдауну:
            {
                "product_name": "коротка назва",
                "kkal": 0.0,
                "protein": 0.0,
                "sacharidy": 0.0,
                "fat": 0.0
            }
            Якщо якогось значення немає, пиши 0.0.
            """

            # Виклик моделі через новий метод generate_content
            response = self.client.models.generate_content(
                model='gemini-3.8-flash',
                contents=[img, prompt]
            )
            
            # Очищаємо відповідь від можливих маркерів ```json ... ```
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            
            # Перетворюємо рядок на справжній Python словник
            data = json.loads(clean_text)
            return data

        except Exception as e:
            print(f"Помилка розпізнавання ШІ: {e}")
            return None