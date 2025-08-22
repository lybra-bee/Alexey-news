#!/usr/bin/env python3
# -- coding: utf-8 --

import requests
import datetime
import os
import json

class NewsGenerator:
    def _init_(self):
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        print(f"Токен: {'установлен' if self.hf_token else 'не установлен'}")
        
    def generate_article(self):
        """Генерация статьи через Hugging Face API"""
        try:
            # Если токен не установлен, используем fallback
            if not self.hf_token:
                print("⚠️  Токен не установлен, используем fallback контент")
                return self.create_fallback_content()
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            prompt = """
Создай новостную статью о последних тенденциях в искусственном интеллекте и нейросетях. 
Статья должна включать: заголовок, введение, основной контент и заключение.
            """
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            print("🔄 Отправка запроса к Hugging Face API...")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    print("✅ Статья сгенерирована через API")
                    return result[0]['generated_text']
            
            # Fallback если API не работает
            print("⚠️  API не ответил, используем fallback")
            return self.create_fallback_content()
            
        except Exception as e:
            print(f"❌ Ошибка генерации: {e}")
            return self.create_fallback_content()
    
    def create_fallback_content(self):
        """Резервный контент если API не работает"""
        themes = [
            "Развитие трансформерных архитектур в 2024 году",
            "Новые открытые языковые модели от Meta и Google",
            "Применение AI в научных исследованиях и медицине",
            "Экосистема инструментов машинного обучения"
        ]
        
        current_theme = themes[datetime.datetime.now().day % len(themes)]
        
        return f"""
# {current_theme}

## Введение
В мире искусственного интеллекта продолжаются стремительные изменения. {current_theme} становится ключевым трендом этого года.

## Основное содержание
Исследователи со всего мира активно работают над улучшением алгоритмов машинного обучения. 
Новые подходы позволяют достигать лучших результатов при меньших вычислительных затратах.

Open-source сообщество вносит значительный вклад в развитие экосистемы AI. 
Такие проекты как Hugging Face Transformers становятся стандартом де-факто.

## Заключение
Будущее искусственного интеллекта выглядит многообещающе. 
Ожидается, что в ближайшие годы мы увидим еще больше прорывных технологий.

Статья сгенерирована автоматически {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def format_html(self, content, image_url=None):
        """Форматирование контента в HTML"""
        if image_url is None:
            image_html = '<div class="image-placeholder">🖼️ Изображение появится позже</div>'
        else:
            image_html = f'<img src="{image_url}" alt="Иллюстрация" style="max-width: 100%; border-radius: 8px;">'
        
        # Простое форматирование текста
        html_content = content.replace('\n\n', '</p><p>')
        html_content = html_content.replace('\n', '<br>')
        html_content = html_content.replace('# ', '<h2>').replace('\n', '</h2>')
        html_content = html_content.replace('## ', '<h3>').replace('\n', '</h3>')
        
        return f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Новости AI</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
            line-height: 1.6;
        }}
        .news-container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .image-placeholder {{
            background: #ecf0f1;
            padding: 60px;
            text-align: center;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 18px;
            color: #7f8c8d;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
            font-size: 14px;
        }}
        h2 {{
            color: #2c3e50;
            margin-top: 30px;
        }}
        h3 {{
            color: #34495e;
        }}
    </style>
</head>
<body>
    <div class="news-container">
        {image_html}
        <div class="content">
            {html_content}
        </div>
        <div class="footer">
            Обновлено: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
        """
    
    def update_news(self):
        """Основная функция обновления новостей"""
        print("🔄 Запуск генерации новости...")
        
        # Генерируем статью
        article_content = self.generate_article()
        
        # Форматируем в HTML
        html_content = self.format_html(article_content)
        
        # Сохраняем
        with open('current-news.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Файл current-news.html обновлен")
        return True

if __name__ == "__main__":
    generator = NewsGenerator()
    success = generator.update_news()
    
    if success:
        print("🎉 Генерация завершена успешно!")
    else:
        print("❌ Ошибка генерации")
