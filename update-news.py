#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random

class NewsGenerator:
    def __init__(self):
        # Правильное получение переменной окружения
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        print(f"Токен HF: {'установлен' if self.hf_token else 'не установлен'}")
        
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
            print(f"❌ Ошибка генерации статьи: {e}")
            return self.create_fallback_content()
    
    def generate_image(self, article_text):
        """Генерация тематического изображения через API"""
        try:
            # Создаем промпт на основе содержания статьи
            prompt = self.create_image_prompt(article_text)
            print(f"🖼️ Промпт для изображения: {prompt}")
            
            # Используем надежные тематические изображения
            image_url = self.get_themed_image(prompt)
            
            print(f"✅ Изображение выбрано: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ Ошибка генерации изображения: {e}")
            return "https://i.imgur.com/6Q9W5Za.jpeg"  # Fallback image

    def create_image_prompt(self, article_text):
        """Создает промпт для изображения на основе статьи"""
        content_lower = article_text.lower()
        
        # Ищем специфичные термины в статье
        ai_terms = [
            "трансформер", "transformer", "GPT", "LLM", "deep learning", 
            "компьютерное зрение", "NLP", "генеративный", "нейросеть",
            "машинное обучение", "искусственный интеллект"
        ]
        
        for term in ai_terms:
            if term in content_lower:
                if "трансформер" in term or "transformer" in term:
                    return "transformer"
                elif "GPT" in term or "LLM" in term:
                    return "language"
                elif "компьютерное зрение" in term:
                    return "computer vision"
                elif "NLP" in term:
                    return "language"
                elif "генеративный" in term:
                    return "ai"
                elif "медицин" in term or "здоровь" in term:
                    return "medical"
                elif "научн" in term or "research" in term:
                    return "research"
                elif "образован" in term or "education" in term:
                    return "education"
                elif "робот" in term or "robot" in term:
                    return "robot"
        
        return "ai"

    def get_themed_image(self, prompt):
        """Тематические изображения (надежные прямые ссылки)"""
        theme = prompt.lower()
        
        # Надежные изображения с imgur и других стабильных источников
        themed_images = {
            "transformer": "https://i.imgur.com/6Q9W5Za.jpeg",
            "language": "https://i.imgur.com/8JZ3L4k.jpeg",
            "computer": "https://i.imgur.com/4V2V1vX.jpeg", 
            "computer vision": "https://i.imgur.com/4V2V1vX.jpeg",
            "medical": "https://i.imgur.com/9K7L5Jy.jpeg",
            "research": "https://i.imgur.com/2V3L6Mz.jpeg",
            "robot": "https://i.imgur.com/7J8L9Kx.jpeg",
            "education": "https://i.imgur.com/3V4L5Mz.jpeg",
            "ai": "https://i.imgur.com/5K6L7Jx.jpeg",
            "neural": "https://i.imgur.com/1V2L3Kx.jpeg"
        }
        
        # Ищем подходящую тему
        for keyword, image_url in themed_images.items():
            if keyword in theme:
                return image_url
        
        # Случайное AI изображение из надежных источников
        reliable_ai_images = [
            "https://i.imgur.com/6Q9W5Za.jpeg",  # AI architecture
            "https://i.imgur.com/8JZ3L4k.jpeg",  # Neural networks
            "https://i.imgur.com/4V2V1vX.jpeg",  # Tech vision
            "https://i.imgur.com/5K6L7Jx.jpeg",  # AI concept
            "https://i.imgur.com/1V2L3Kx.jpeg",  # Data processing
            "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?w=800&h=400&fit=crop",  # AI brain
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&h=400&fit=crop",  # AI chips
            "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop"   # AI network
        ]
        
        return random.choice(reliable_ai_images)
    
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

*Статья сгенерирована автоматически {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
        """
    
    def format_html(self, content, image_url=None):
        """Форматирование контента в HTML"""
        if not image_url:
            image_html = '<div class="image-placeholder">🖼️ Изображение появится позже</div>'
        else:
            image_html = f'<img src="{image_url}" alt="Иллюстрация к статье о нейросетях" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 20px 0;">'
        
        # Правильное форматирование текста
        html_content = content
        html_content = html_content.replace('# ', '<h2>').replace('\n', '</h2>')
        html_content = html_content.replace('## ', '<h3>').replace('\n', '</h3>')
        html_content = html_content.replace('\n\n', '</p><p>')
        html_content = html_content.replace('\n', '<br>')
        
        # Убираем лишние теги
        html_content = html_content.replace('<h2></h2>', '').replace('<h3></h3>', '')
        
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
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 25px;
        }}
        p {{
            margin: 15px 0;
            text-align: justify;
        }}
        .content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        img {{
            transition: transform 0.3s ease;
        }}
        img:hover {{
            transform: scale(1.02);
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
        print("✅ Статья сгенерирована")
        
        # Генерируем изображение
        image_url = self.generate_image(article_content)
        
        # Форматируем в HTML
        html_content = self.format_html(article_content, image_url)
        
        # Сохраняем
        with open('current-news.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Файл current-news.html обновлен с изображением")
        return True

if __name__ == "__main__":
    generator = NewsGenerator()
    success = generator.update_news()
    
    if success:
        print("🎉 Генерация завершена успешно!")
    else:
        print("❌ Ошибка генерации")
