#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import time
import random

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        
    def generate_article(self):
        """Генерация статьи через бесплатный API"""
        print("🔄 Генерация статьи...")
        
        # Пробуем разные бесплатные модели
        models = [
            "microsoft/DialoGPT-medium",
            "facebook/blenderbot-400M-distill",
            "mosaicml/mpt-7b-chat",
            "togethercomputer/RedPajama-INCITE-7B-Chat"
        ]
        
        for model in models:
            try:
                headers = {
                    "Authorization": f"Bearer {self.hf_token}" if self.hf_token else "",
                    "Content-Type": "application/json"
                }
                
                prompt = """Напиши новостную статью о последних достижениях в области искусственного интеллекта. 
Опиши новые технологии и их применение. Объем: 300-400 слов. Только текст без заголовков."""
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 500,
                        "temperature": 0.9,
                        "do_sample": True,
                        "return_full_text": False
                    }
                }
                
                print(f"Пробуем модель: {model}")
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=45
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        article = result[0]['generated_text'].strip()
                        print(f"✅ Статья сгенерирована моделью {model}")
                        return article
                
                time.sleep(2)  # Пауза между попытками
                
            except Exception as e:
                print(f"Ошибка с моделью {model}: {e}")
                continue
        
        # Если все API не сработали, генерируем локально
        return self.generate_local_article()

    def generate_local_article(self):
        """Локальная генерация статьи если API не работают"""
        print("🔄 Локальная генерация статьи...")
        
        themes = [
            """В 2024 году искусственный интеллект продолжает стремительно развиваться. Новые языковые модели демонстрируют удивительные способности в понимании и генерации текста. 
Исследователи из ведущих tech-компаний представили инновационные архитектуры нейронных сетей, которые значительно эффективнее предыдущих версий. 
В области компьютерного зрения достигнут прогресс в распознавании объектов и создании синтетических изображений. 
Многие стартапы активно внедряют AI-решения в медицину, образование и бизнес-процессы. 
Эксперты прогнозируют, что в ближайшие годы искусственный интеллект станет неотъемлемой частью повседневной жизни.""",

            """Современные нейросетевые технологии открывают новые горизонты для креативных индустрий. Генеративные модели позволяют создавать уникальный контент, 
от текстов до изображений и музыки. В 2024 году особое внимание уделяется этическим аспектам использования ИИ и разработке ответственных алгоритмов. 
Развитие open-source сообщества способствует демократизации технологий, делая их доступными для более широкого круга разработчиков. 
Квантовые вычисления и нейроморфные процессоры promise ускорить обработку данных и сделать ИИ еще более эффективным."""
        ]
        
        return random.choice(themes)

    def generate_image(self):
        """Генерация изображения через бесплатный API"""
        print("🔄 Генерация изображения...")
        
        try:
            # Пробуем Stable Diffusion
            headers = {
                "Authorization": f"Bearer {self.hf_token}" if self.hf_token else "",
                "Content-Type": "application/json"
            }
            
            prompt = "futuristic artificial intelligence, neural network, digital art, blue purple colors, technology concept"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": 1024,
                    "height": 512,
                    "num_inference_steps": 20
                }
            }
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"article_image_{timestamp}.jpg"
                
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print("✅ Изображение сгенерировано")
                return image_filename
            
        except Exception as e:
            print(f"Ошибка генерации изображения: {e}")
        
        # Если API не сработал, используем placeholder
        return self.download_placeholder()

    def download_placeholder(self):
        """Скачивание красивого placeholder"""
        try:
            placeholders = [
                "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1024&h=512&fit=crop"
            ]
            
            response = requests.get(random.choice(placeholders), timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"article_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print("✅ Использован placeholder из Unsplash")
            return image_filename
            
        except:
            print("⚠️ Не удалось скачать placeholder")
            return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости нейросетей и технологий",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path,
            "short_description": article_text[:150] + "..." if len(article_text) > 150 else article_text,
            "tags": ["AI", "нейросети", "технологии"]
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
        
        try:
            # Генерируем статью
            article_text = self.generate_article()
            print(f"📄 Длина статьи: {len(article_text)} символов")
            
            # Генерируем изображение
            image_path = self.generate_image()
            
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
        print("💾 Данные сохранены в tilda_data.json и article.txt")
        print("=" * 50)
        
        # Показываем начало статьи
        print("\n📋 Начало статьи:")
        print(result['content'][:200] + "...")
    else:
        print("❌ Не удалось сгенерировать контент")

if __name__ == "__main__":
    main()
