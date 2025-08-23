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
            
            # Пробуем разные бесплатные API по очереди
            image_url = self.try_unsplash_api(prompt)
            if image_url:
                return image_url
                
            # Fallback - тематическое изображение
            return self.get_themed_fallback_image(prompt)
            
        except Exception as e:
            print(f"❌ Ошибка генерации изображения: {e}")
            return self.get_themed_fallback_image("нейросети")

    def create_image_prompt(self, article_text):
        """Создает промпт для изображения на основе статьи"""
        # Берем ключевые слова из статьи
        keywords = ["нейросети", "искусственный интеллект", "AI", "машинное обучение"]
        
        # Ищем специфичные термины в статье
        ai_terms = ["трансформер", "transformer", "GPT", "LLM", "deep learning", 
                    "компьютерное зрение", "NLP", "генеративный AI"]
        
        content_lower = article_text.lower()
        for term in ai_terms:
            if term in content_lower:
                if "трансформер" in term or "transformer" in term:
                    return "transformer neural network architecture"
                elif "GPT" in term or "LLM" in term:
                    return "large language model AI"
                elif "компьютерное зрение" in term:
                    return "computer vision AI"
                elif "NLP" in term:
                    return "natural language processing"
                elif "генеративный" in term:
                    return "generative AI art"
        
        # Определяем общую тематику
        if any(word in content_lower for word in ["медицин", "здоровь", "health"]):
            return "AI in healthcare medical technology"
        elif any(word in content_lower for word in ["научн", "research", "исследовани"]):
            return "scientific research AI technology"
        elif any(word in content_lower for word in ["образован", "education", "обучен"]):
            return "AI education technology"
        elif any(word in content_lower for word in ["робот", "robot", "автоматизац"]):
            return "robotics AI automation"
        
        return "artificial intelligence neural network technology"

    def try_unsplash_api(self, prompt):
        """Пробуем найти изображение через Unsplash API"""
        try:
            # Unsplash Source API (бесплатно)
            url = f"https://source.unsplash.com/800x400/?"
            keywords = ["technology", "ai", "neural network", prompt.split()[0]]
            
            # Создаем URL с тематическими ключевыми словами
            unsplash_url = f"{url}{','.join(keywords)}"
            
            # Проверяем доступность
            response = requests.head(unsplash_url, timeout=5)
            if response.status_code == 200:
                return unsplash_url
                
        except Exception as e:
            print(f"⚠️  Unsplash API недоступен: {e}")
        
        return None

    def get_themed_fallback_image(self, prompt):
        """Тематические fallback изображения"""
        theme = prompt.lower()
        
        themed_images = {
            "transformer": "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b?w=800&h=400&fit=crop",
            "language": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800&h=400&fit=crop",
            "computer vision": "https://images.unsplash.com/photo-1534723328310-e82dad3ee43f?w=800&h=400&fit=crop",
            "medical": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=800&h=400&fit=crop",
            "research": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800&h=400&fit=crop",
            "robot": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=400&fit=crop",
            "education": "https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800&h=400&fit=crop",
            "ai": "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?w=800&h=400&fit=crop",
            "neural": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&h=400&fit=crop"
        }
        
        # Ищем подходящую тему
        for keyword, image_url in themed_images.items():
            if keyword in theme:
                return image_url
        
        # Общее AI изображение
        ai_images = [
            "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop"
        ]
        
        return random.choice(ai_images)
    
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
        if image_url is None:
            image_html = '<div class="image-placeholder">🖼️ Изображение появится позже</div>'
        else:
            image_html = f'<img src="{image_url}" alt="Иллюстрация к статье о нейросетях" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">'
        
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
