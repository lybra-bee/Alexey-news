#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']
        # Используем API которые точно работают
        self.text_api_url = "https://api-inference.huggingface.co/models/gpt2"
        self.image_api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        
    def generate_article(self):
        """Генерация статьи через работающее API"""
        print("🔄 Генерация статьи через GPT-2...")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "Современные достижения в области искусственного интеллекта:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 300,
                "temperature": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
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
                    print("✅ Статья сгенерирована")
                    return article
            elif response.status_code == 503:
                # Модель загружается, ждем и пробуем again
                print("⏳ Модель загружается, ждем 30 секунд...")
                import time
                time.sleep(30)
                return self.generate_article()  # Рекурсивный вызов
            else:
                raise Exception(f"Ошибка API: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Ошибка генерации текста: {e}")

    def generate_image(self):
        """Генерация изображения через работающее API"""
        print("🔄 Генерация изображения через Stable Diffusion...")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "artificial intelligence neural network futuristic technology digital art"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 512,
                "height": 256,
                "num_inference_steps": 20
            }
        }
        
        try:
            response = requests.post(
                self.image_api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"ai_image_{timestamp}.jpg"
                
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print("✅ Изображение сгенерировано")
                return image_filename
            elif response.status_code == 503:
                print("⏳ Модель изображений загружается, ждем 30 секунд...")
                import time
                time.sleep(30)
                return self.generate_image()  # Рекурсивный вызов
            else:
                raise Exception(f"Ошибка генерации изображения: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Ошибка генерации изображения: {e}")

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости ИИ и нейросетей",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path,
            "short_description": article_text[:150] + "..." if len(article_text) > 150 else article_text,
            "tags": ["AI", "нейросети", "технологии", "машинное обучение"],
            "generated_with_ai": True
        }
        
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации"""
        print("🚀 Запуск нейросетевой генерации...")
        print(f"🔑 Токен: {self.hf_token[:10]}...")
        
        article_text = self.generate_article()
        print(f"📄 Длина статьи: {len(article_text)} символов")
        
        image_path = self.generate_image()
        
        tilda_data = self.prepare_for_tilda(article_text, image_path)
        
        print("✅ Генерация завершена!")
        return tilda_data

def main():
    print("🤖 Нейросетевой генератор контента")
    print("=" * 60)
    print("🚀 Используются работающие модели:")
    print("   - GPT-2 для текста")
    print("   - Stable Diffusion v1-4 для изображений")
    print("=" * 60)
    
    if 'HF_API_TOKEN' not in os.environ:
        raise Exception("HF_API_TOKEN не установлен в переменных окружения")
    
    try:
        generator = ContentGenerator()
        result = generator.generate_content()
        
        print("\n" + "=" * 60)
        print("📊 РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print("💾 Данные сохранены")
        print("=" * 60)
        
        print("\n📋 ПРЕВЬЮ СТАТЬИ:")
        print("=" * 40)
        print(result['content'][:200] + "...")
        print("=" * 40)
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
