#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import base64

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']
        self.sd_model = "stabilityai/stable-diffusion-2-1"
        self.text_model = "microsoft/DialoGPT-large"
        
    def generate_article(self):
        """Генерация статьи через HF API"""
        print("🔄 Генерация статьи...")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = """
Создай новостную статью на 300-400 слов о последних достижениях в области искусственного интеллекта. 
Опиши конкретные технологии, компании и применения. Статья должна быть информативной и актуальной.
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
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.text_model}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                article = result[0]['generated_text']
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
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        # Создаем промпт для изображения
        image_prompt = """
Футуристическое изображение искусственного интеллекта, нейронные сети, технологии, 
голубые и фиолетовые тона, цифровое искусство, hi-tech стиль
        """
        
        payload = {
            "inputs": image_prompt,
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        }
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.sd_model}",
                headers=headers,
                json=payload,
                timeout=120
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
        
        # Читаем изображение как base64 для возможного использования
        image_base64 = None
        try:
            with open(image_path, 'rb') as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        except:
            pass
        
        tilda_data = {
            "version": "1.0",
            "title": "Новости нейросетей и ИИ",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_filename": image_path,
            "image_base64": image_base64,
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

if __name__ == "__main__":
    main()
