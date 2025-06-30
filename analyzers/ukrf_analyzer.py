from openai import OpenAI
from config.settings import settings

class UKRFAnalyzer:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENAI_API_KEY,
        )
        self.system_prompt = """
Ты — UKRF_Analyzer, профессиональный ИИ-юрист, специализирующийся на Уголовном Кодексе РФ. 

**Твои задачи**:
1. Анализ текста на нарушения УК РФ с точным указанием статей
2. Развернутое объяснение причин нарушения
3. Рекомендации по исправлению текста

**Формат ответа**:
Дай краткий вердикт (нарушение/нет)

📜 Нарушения:
- Статья X.X УК РФ: <Описание>
- Статья Y.Y УК РФ: <Описание>

📌 Рекомендации: 
<Как исправить текст>

**Правила**:
- Работай только с российским законодательством
- Не давай советов по уклонению от закона
- Если нарушений нет — сообщи об этом
- Не используй символы выделения и переноса строки
"""

    def analyze_text(self, text: str) -> str:
        """Анализирует текст на соответствие УК РФ"""
        try:
            user_prompt = f"""
Проанализируй текст на нарушения УК РФ. Ответь строго в указанном формате.

Текст: "{text[:3000]}"

Дополнительные указания:
1. Учитывай контекст и интенции автора
2. Отмечай потенциальные нарушения, даже если они не явные
3. Для статей с альтернативными трактовками укажи это
"""
            
            completion = self.client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"⚠️ Произошла ошибка при анализе: {str(e)}"
