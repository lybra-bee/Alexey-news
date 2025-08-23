#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random
import base64

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
        """Генерация тематического изображения"""
        try:
            # Создаем промпт на основе содержания статьи
            prompt = self.create_image_prompt(article_text)
            print(f"🖼️ Тема изображения: {prompt}")
            
            # Используем встроенное SVG изображение
            image_data_url = self.get_embedded_svg_image(prompt)
            
            print("✅ Встроенное изображение сгенерировано")
            return image_data_url
            
        except Exception as e:
            print(f"❌ Ошибка генерации изображения: {e}")
            return self.get_embedded_svg_image("ai")
    
    def get_embedded_svg_image(self, prompt):
        """Создает встроенное SVG изображение"""
        # Цвета в зависимости от темы
        theme_colors = {
            "transformer": ("#3498db", "#e74c3c"),
            "language": ("#9b59b6", "#f1c40f"),
            "computer": ("#2ecc71", "#e67e22"),
            "medical": ("#e74c3c", "#3498db"),
            "research": ("#f39c12", "#8e44ad"),
            "robot": ("#7f8c8d", "#e74c3c"),
            "education": ("#27ae60", "#d35400"),
            "ai": ("#2980b9", "#c0392b"),
            "neural": ("#8e44ad", "#f39c12")
        }
        
        primary_color, secondary_color = theme_colors.get(prompt, ("#2980b9", "#c0392b"))
        
        # SVG изображение
        svg_content = f'''
        <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#2c3e50;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#34495e;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#grad1)"/>
            
            <!-- Основные элементы -->
            <circle cx="200" cy="200" r="60" fill="{primary_color}" opacity="0.7">
                <animate attributeName="r" values="60;70;60" dur="3s" repeatCount="indefinite"/>
            </circle>
            
            <rect x="400" y="150" width="120" height="120" rx="15" fill="{secondary_color}" opacity="0.7">
                <animate attributeName="y" values="150;140;150" dur="2s" repeatCount="indefinite"/>
            </rect>
            
            <polygon points="600,200 650,150 700,200 650,250" fill="{primary_color}" opacity="0.8">
                <animate attributeName="points" values="600,200 650,150 700,200 650,250; 610,200 650,140 690,200 650,260; 600,200 650,150 700,200 650,250" dur="4s" repeatCount="indefinite"/>
            </polygon>
            
            <!-- Текст -->
            <text x="400" y="320" text-anchor="middle" fill="#ecf0f1" font-family="Arial" font-size="20" font-weight="bold">
                AI NEWS • {prompt.upper()} • NEURAL NETWORKS
            </text>
            
            <text x="400" y="350" text-anchor="middle" fill="#bdc3c7" font-family="Arial" font-size="14">
                🤖 Автоматически сгенерировано • {datetime.datetime.now().strftime('%d.%m.%Y')}
            </text>
            
            <!-- Декоративные элементы -->
            <circle cx="100" cy="100" r="8" fill="#fff" opacity="0.3"/>
            <circle cx="700" cy="80" r="12" fill="#fff" opacity="0.2"/>
            <circle cx="750" cy="350" r="6" fill="#fff" opacity="0.4"/>
            <circle cx="50" cy="350" r="10" fill="#fff" opacity="0.3"/>
        </svg>
        '''
        
        # Конвертируем в base64
        encoded = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded}"
    
    def create_image_prompt(self, article_text):
        """Создает промпт для изображения на основе статьи"""
        content_lower = article_text.lower()
        
        # Определяем тему по содержанию
        themes = {
            "трансформер": "transformer",
            "transformer": "transformer",
            "gpt": "language",
            "llm": "language",
            "язык": "language",
            "компьютерное зрение": "computer",
            "видео": "computer",
            "медицин": "medical",
            "здоровь": "medical",
            "научн": "research",
            "исследован": "research",
            "образован": "education",
            "обучен": "education",
            "робот": "robot",
            "автоматизац": "robot"
        }
        
        for keyword, theme in themes.items():
            if keyword in content_lower:
                return theme
        
        return "ai"
    
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
