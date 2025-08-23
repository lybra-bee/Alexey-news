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
        # ИСПРАВЛЕННЫЕ МОДЕЛИ (работающие):
        self.text_model = "microsoft/DialoGPT-large"  # Работающая модель
        self.image_model = "runwayml/stable-diffusion-v1-5"  # Работающая модель
        
    def wait_for_model(self, model_name):
        """Ожидание готовности модели"""
        print(f"⏳ Ожидание готовности модели {model_name}...")
        
        headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        for attempt in range(6):  # 1 минута ожидания
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    print("✅ Модель готова к работе")
                    return True
                elif response.status_code == 503:
                    wait_time = (attempt + 1) * 10
                    print(f"🔄 Модель загружается... ({wait_time} сек)")
                    time.sleep(10)
                else:
                    print(f"⚠️ Статус: {response.status_code}")
                    time.sleep(5)
            except Exception as e:
                print(f"⚠️ Ошибка: {e}")
                time.sleep(5)
        
        print("❌ Модель не загрузилась")
        return False

    def generate_article(self):
        """Генерация статьи через нейросеть"""
        print("🔄 Генерация статьи через нейросеть...")
        
        if not self.hf_token:
            print("⚠️ Токен отсутствует, используем резервную генерацию")
            return self.create_fallback_article()
            
        if not self.wait_for_model(self.text_model):
            return self.create_fallback_article()
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "Напиши новостную статью на 200 слов о последних достижениях в области искусственного интеллекта и нейронных сетей."
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 400,
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
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    article = result[0]['generated_text'].strip()
                    print("✅ Статья сгенерирована нейросетью")
                    return article
            
            print("⚠️ Нейросеть вернула неожиданный ответ")
            return self.create_fallback_article()
            
        except Exception as e:
            print(f"❌ Ошибка генерации: {e}")
            return self.create_fallback_article()

    def create_fallback_article(self):
        """Резервная генерация статьи"""
        print("🔄 Используем резервную генерацию статьи...")
        
        articles = [
            "OpenAI представила новую версию GPT-4 с улучшенными возможностями понимания контекста и генерации текста. Эта технология позволяет значительно улучшить качество диалоговых систем и автоматического создания контента.",
            "Google DeepMind анонсировал прорыв в области reinforcement learning. Новые алгоритмы демонстрируют беспрецедентную эффективность в обучении сложным задачам, что открывает возможности для создания более advanced AI систем.",
            "Развитие мультимодальных моделей позволяет обрабатывать текст, изображения и аудио одновременно. Это революционное достижение меняет подход к созданию универсальных искусственных интеллектов.",
            "Новые архитектуры трансформеров показывают на 40% лучшую производительность при меньших вычислительных затратах. Эксперты отмечают, что это ускорит внедрение AI технологий в повседневную жизнь."
        ]
        
        return random.choice(articles)

    def generate_image(self):
        """Генерация изображения через нейросеть"""
        print("🔄 Генерация изображения через нейросеть...")
        
        if not self.hf_token:
            print("⚠️ Токен отсутствует, используем резервное изображение")
            return self.download_fallback_image()
            
        if not self.wait_for_model(self.image_model):
            return self.download_fallback_image()
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "futuristic artificial intelligence, neural network, digital art, technology concept"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 20
            }
        }
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.image_model}",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"ai_image_{timestamp}.jpg"
                
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print("✅ Изображение сгенерировано нейросетью")
                return image_filename
            
            print("⚠️ Нейросеть изображений не ответила")
            return self.download_fallback_image()
            
        except Exception as e:
            print(f"❌ Ошибка генерации изображения: {e}")
            return self.download_fallback_image()

    def download_fallback_image(self):
        """Резервное изображение"""
        try:
            images = [
                "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1024&h=512&fit=crop"
            ]
            
            response = requests.get(random.choice(images), timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"ai_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print("✅ Использовано резервное изображение")
            return image_filename
            
        except Exception as e:
            print(f"❌ Не удалось загрузить резервное изображение: {e}")
            return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости ИИ и нейросетей",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path or "no_image.jpg",
            "short_description": article_text[:120] + "..." if len(article_text) > 120 else article_text,
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
        print(f"🔑 Токен HF: {'есть' if self.hf_token else 'отсутствует'}")
        
        try:
            article_text = self.generate_article()
            print(f"📄 Длина: {len(article_text)} символов")
            
            image_path = self.generate_image()
            
            tilda_data = self.prepare_for_tilda(article_text, image_path)
            
            print("✅ Генерация завершена!")
            return tilda_data
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            return None

def main():
    print("🤖 Нейросетевой генератор контента")
    print("=" * 50)
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    if result:
        print("\n" + "=" * 50)
        print("📊 РЕЗУЛЬТАТЫ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print("💾 Данные сохранены")
        print("=" * 50)
    else:
        print("❌ Генерация не удалась")

if __name__ == "__main__":
    main()
