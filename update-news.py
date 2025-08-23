#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os

class NewsGenerator:
    def __init__(self):
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        print(f"Токен HF: {'установлен' if self.hf_token else 'не установлен'}")
        
    def generate_article(self):
        """Генерация статьи"""
        try:
            if not self.hf_token:
                print("⚠️  Используем fallback контент")
                return self.create_fallback_content()
            
            headers = {"Authorization": f"Bearer {self.hf_token}", "Content-Type": "application/json"}
            
            prompt = """
Создай развернутую новостную статью объемом 600-800 слов о последних достижениях в области искусственного интеллекта и нейронных сетей. 
Статья должна быть информативной и содержательной, охватывать актуальные тенденции и developments в этой сфере.
Включи конкретные примеры, статистику и экспертные мнения, но не используй явные заголовки разделов типа "Введение", "Основная часть", "Заключение".
            """
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 800,
                    "temperature": 0.8,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            print("🔄 Запрос к API...")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    print("✅ Статья сгенерирована через API")
                    article = result[0]['generated_text']
                    # Убираем возможные явные заголовки
                    article = article.replace("Введение:", "").replace("Заключение:", "")
                    article = article.replace("Введение", "").replace("Заключение", "")
                    return article
            
            return self.create_fallback_content()
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return self.create_fallback_content()
    
    def create_fallback_content(self):
        """Резервный контент"""
        themes = [
            """Современные нейросетевые архитектуры продолжают стремительно развиваться, открывая новые горизонты в области искусственного интеллекта. За последние месяцы исследователи представили несколько прорывных технологий, которые кардинально меняют подход к машинному обучению.

Одним из наиболее значимых достижений стало создание более эффективных трансформерных моделей, которые демонстрируют беспрецедентную производительность при обработке естественного языка. Эти модели не только улучшают качество генерации текста, но и значительно снижают вычислительные затраты, что делает их более доступными для широкого круга разработчиков.

В сфере компьютерного зрения также наблюдаются существенные продвижения. Новые алгоритмы позволяют достигать высочайшей точности распознавания образов даже в условиях ограниченных данных. Это открывает возможности для применения AI в таких областях, как медицинская диагностика, автономные транспортные средства и промышленная автоматизация.

Эксперты отмечают, что важным трендом становится развитие мультимодальных систем, способных одновременно обрабатывать текст, изображения и аудио. Такие системы демонстрируют удивительную способность к пониманию контекста и генерации когерентных ответов across different modalities.

Сообщество open-source вносит неоценимый вклад в развитие экосистемы. Проекты на платформах типа Hugging Face становятся стандартом де-факто, предоставляя исследователям и разработчикам доступ к передовым моделям и инструментам.

Будущее искусственного интеллекта выглядит чрезвычайно перспективно. Ожидается, что в ближайшие годы мы станем свидетелями еще более впечатляющих достижений, которые преобразуют множество отраслей и улучшат качество жизни людей по всему миру.""",

            """Прогресс в области генеративного искусственного интеллекта достиг беспрецедентных масштабов. Всего за последний квартал было представлено несколько инновационных моделей, которые кардинально меняют ландшафт машинного обучения.

Языковые модели нового поколения демонстрируют способность к глубокому пониманию контекста и генерации человекоподобного текста. Эти достижения становятся возможными благодаря усовершенствованным архитектурам и более эффективным методам обучения.

В области компьютерного зрения исследователи добились значительных успехов в создании систем, способных accurately анализировать сложные визуальные сцены. Это имеет profound implications для таких приложений, как augmented reality, autonomous navigation и automated quality control.

Важным направлением развития становится focus на этические аспекты AI. Разработчики все больше attention уделяют вопросам fairness, transparency и accountability своих систем, что способствует responsible development технологии.

Интеграция AI с другими emerging technologies, такими как quantum computing и neuromorphic hardware, открывает новые возможности для создания еще более powerful и efficient систем.

Сообщество researchers и developers продолжает активно collaborate через open-source platforms, accelerating pace innovation и democratizing access к передовым технологиям.

Перспективы развития искусственного интеллекта остаются extremely promising. Continuous advancements в algorithms, hardware и methodologies обещают привести к созданию еще более sophisticated и capable систем в near future."""
        ]
        
        current_theme = themes[datetime.datetime.now().day % len(themes)]
        return current_theme
    
    def generate_image(self):
        """Простая надежная картинка"""
        print("🖼️ Используем placeholder изображение")
        return "https://via.placeholder.com/800x400/2c3e50/ecf0f1?text=AI+Neural+Networks+News"
    
    def format_html(self, content, image_url=None):
        """Форматирование контента в HTML"""
        if not image_url:
            image_html = '<div class="image-placeholder">🖼️ Изображение появится позже</div>'
        else:
            image_html = f'<img src="{image_url}" alt="Иллюстрация к статье о нейросетях" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 20px 0;">'
        
        # Форматируем текст без явных заголовков
        html_content = content.replace('\n\n', '</p><p>')
        html_content = html_content.replace('\n', '<br>')
        
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
        p {{
            margin: 15px 0;
            text-align: justify;
            font-size: 16px;
        }}
        .content {{
            background: #f8f9fa;
            padding: 25px;
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
            <p>{html_content}</p>
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
        image_url = self.generate_image()
        
        # Форматируем в HTML
        html_content = self.format_html(article_content, image_url)
        
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
