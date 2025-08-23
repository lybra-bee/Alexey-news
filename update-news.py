#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import time
import base64

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']
        self.sd_model = "stabilityai/stable-diffusion-xl-base-1.0"  # Более новая модель
        self.text_model = "microsoft/DialoGPT-large"
        
    def wait_for_model(self, model_name, task_type="text-generation"):
        """Ожидание готовности модели"""
        print(f"⏳ Ожидание готовности модели {model_name}...")
        
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        if task_type == "text-to-image":
            url += "?wait_for_model=true"
        
        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    print("✅ Модель готова к работе")
                    return True
                elif response.status_code == 503:
                    print(f"🔄 Модель загружается... попытка {attempt + 1}/{max_retries}")
                    time.sleep(10)
                else:
                    print(f"⚠️ Статус модели: {response.status_code}")
                    time.sleep(5)
            except Exception as e:
                print(f"⚠️ Ошибка проверки модели: {e}")
                time.sleep(5)
        
        print("❌ Модель не загрузилась за отведенное время")
        return False

    def generate_article(self):
        """Генерация статьи через HF API"""
        print("🔄 Генерация статьи...")
        
        if not self.wait_for_model(self.text_model):
            raise Exception("Модель для текста не загрузилась")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = """Создай новостную статью на 300-400 слов о последних достижениях в области искусственного интеллекта в 2024 году. 
Опиши конкретные технологии, компании и реальные применения. Статья должна быть информативной и актуальной.
Формат: обычный текст без заголовков."""
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 600,
                "temperature": 0.85,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.text_model}",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                article = result[0]['generated_text'].strip()
                print("✅ Статья сгенерирована")
                return article
            else:
                raise Exception("Неверный формат ответа от API")
                
        except Exception as e:
            print(f"❌ Ошибка генерации текста: {e}")
            raise

    def generate_image(self, article_text):
        """Генерация изображения по содержанию статьи"""
        print("🔄 Генерация изображения...")
        
        if not self.wait_for_model(self.sd_model, "text-to-image"):
            raise Exception("Модель для изображений не загрузилась")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        # Создаем детальный промпт для изображения
        image_prompt = """
futuristic artificial intelligence neural network, digital brain, glowing circuits, 
blue and purple light, cyberpunk style, high technology, intricate details, 
4k resolution, professional digital art, trending on artstation
        """
        
        payload = {
            "inputs": image_prompt,
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 25,
                "guidance_scale": 8.0,
                "wait_for_model": True
            }
        }
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.sd_model}",
                headers=headers,
                json=payload,
                timeout=180  # Увеличиваем таймаут для генерации изображений
            )
            
            response.raise_for_status()
            
            # Сохраняем изображение
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"article_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print("✅ Изображение сгенерировано и сохранено")
            return image_filename
            
        except Exception as e:
            print(f"❌ Ошибка генерации изображения: {e}")
            raise

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "version": "1.0",
            "title": "Новости нейросетей и ИИ",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_filename": image_path,
            "short_description": article_text[:120] + "..." if len(article_text) > 120 else article_text,
            "tags": ["AI", "нейросети", "технологии", "машинное обучение"],
            "seo_title": "Последние новости искусственного интеллекта и нейросетей",
            "seo_description": "Свежие статьи о развитии технологий ИИ, машинного обучения и нейронных сетей"
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
        try:
            # Генерируем статью
            article_text = self.generate_article()
            
            # Генерируем изображение
            image_path = self.generate_image(article_text)
            
            # Подготавливаем для Tilda
            tilda_data = self.prepare_for_tilda(article_text, image_path)
            
            print("✅ Генерация завершена успешно!")
            return tilda_data
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            return None

def main():
    # Проверяем наличие токена
    if 'HF_API_TOKEN' not in os.environ:
        print("❌ Ошибка: HF_API_TOKEN не установлен в переменных окружения")
        print("Добавьте токен в Secrets GitHub: HF_API_TOKEN=your_token_here")
        return
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    if result:
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_filename']}")
        print(f"💾 Данные сохранены в: tilda_data.json, article.txt")
        print("="*60)
        
        # Показываем превью статьи
        print("\n📋 Превью статьи:")
        print(result['content'][:200] + "...")

if __name__ == "__main__":
    main()
