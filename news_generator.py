#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random

class ContentGenerator:
    def __init__(self):
        # Бесплатные API endpoints
        self.text_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.image_api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        
    def generate_article(self):
        """Генерация статьи через API"""
        print("🔄 Генерация статьи через API...")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            prompt = """Напиши короткую новостную статью о последних достижениях в области искусственного интеллекта. 
            Опиши конкретные технологии и их применение. Объем: 200-300 слов."""
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 400,
                    "temperature": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.text_api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    article = result[0]['generated_text'].strip()
                    print("✅ Статья сгенерирована через API")
                    return article
            
            # Если API не сработал, генерируем разнообразный контент локально
            return self.generate_dynamic_article()
            
        except Exception as e:
            print(f"❌ Ошибка API: {e}")
            return self.generate_dynamic_article()

    def generate_dynamic_article(self):
        """Динамическая генерация статьи с вариациями"""
        print("🔄 Локальная генерация статьи...")
        
        themes = [
            "нейронные сети", "машинное обучение", "компьютерное зрение", 
            "обработка естественного языка", "генеративный ИИ"
        ]
        
        companies = [
            "Google", "OpenAI", "Microsoft", "Meta", "DeepMind", "Amazon",
            "нейросетевые стартапы", "исследовательские лаборатории"
        ]
        
        applications = [
            "медицинской диагностике", "автономных транспортных средствах", 
            "персональных ассистентах", "создании контента", "научных исследованиях"
        ]
        
        theme = random.choice(themes)
        company = random.choice(companies)
        application = random.choice(applications)
        
        articles = [
            f"""В области {theme} произошел значительный прорыв. {company} представили новую технологию, 
            которая кардинально улучшает производительность алгоритмов. Это достижение открывает 
            новые возможности для применения в {application}.

Эксперты отмечают, что данная разработка может изменить подход к решению сложных задач 
и ускорить внедрение искусственного интеллекта в повседневную жизнь.""",

            f"""Современные разработки в сфере {theme} демонстрируют впечатляющие результаты. 
{company} анонсировали инновационное решение, которое значительно превосходит предыдущие версии.

Новая технология уже тестируется в {application} и показывает promising результаты. 
Исследователи believe, что это лишь начало революционных изменений в отрасли.""",

            f"""Прогресс в области {theme} достиг новых высот. Команда из {company} 
разработала breakthrough алгоритм, который устанавливает новые стандарты точности и скорости.

Применение этой технологии в {application} может привести к значительному улучшению 
качества услуг и созданию принципиально новых продуктов."""
        ]
        
        article = random.choice(articles)
        print("✅ Статья сгенерирована локально")
        return article

    def download_image(self):
        """Скачивание реального изображения"""
        print("🔄 Загрузка изображения...")
        
        try:
            # Используем разнообразные изображения с Unsplash
            image_urls = [
                "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b?w=1024&h=512&fit=crop&auto=format",
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1024&h=512&fit=crop&auto=format",
                "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1024&h=512&fit=crop&auto=format",
                "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1024&h=512&fit=crop&auto=format",
                "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1024&h=512&fit=crop&auto=format",
                "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=1024&h=512&fit=crop&auto=format"
            ]
            
            image_url = random.choice(image_urls)
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"article_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Изображение загружено: {image_filename}")
            return image_filename
            
        except Exception as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
            return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        # Создаем уникальное описание
        descriptions = [
            "Свежие новости из мира искусственного интеллекта и нейросетей",
            "Актуальные разработки в области машинного обучения",
            "Последние достижения в сфере высоких технологий",
            "Инновационные решения в области компьютерных наук"
        ]
        
        tilda_data = {
            "title": "Новости нейросетей и технологий",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path or "no_image.jpg",
            "short_description": random.choice(descriptions),
            "tags": ["AI", "нейросети", "технологии", "машинное обучение", "инновации"],
            "views": random.randint(100, 1000),
            "rating": round(random.uniform(4.0, 5.0), 1)
        }
        
        # Сохраняем в JSON
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        # Сохраняем текст отдельно
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации контента"""
        print("🚀 Запуск генерации контента...")
        print(f"📝 Токен HF: {'есть' if self.hf_token else 'отсутствует'}")
        
        try:
            # Генерируем статью
            article_text = self.generate_article()
            print(f"📄 Длина статьи: {len(article_text)} символов")
            
            # Загружаем изображение
            image_path = self.download_image()
            
            # Подготавливаем для Tilda
            tilda_data = self.prepare_for_tilda(article_text, image_path)
            
            print("✅ Генерация завершена!")
            return tilda_data
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

def main():
    print("🤖 Генератор новостей AI")
    print("=" * 50)
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    if result:
        print("\n" + "=" * 50)
        print("📊 РЕЗУЛЬТАТЫ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print(f"⭐ Рейтинг: {result['rating']}")
        print(f"👁️ Просмотры: {result['views']}")
        print("💾 Данные сохранены в tilda_data.json и article.txt")
        print("=" * 50)
        
        # Показываем начало статьи
        print("\n📋 Начало статьи:")
        print(result['content'][:200] + "...")
    else:
        print("❌ Не удалось сгенерировать контент")

if __name__ == "__main__":
    main()
