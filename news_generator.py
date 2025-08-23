#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import time

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']
        # ИСПРАВЛЕННЫЕ РАБОТАЮЩИЕ МОДЕЛИ:
        self.text_model = "microsoft/DialoGPT-large"  # Работает!
        self.image_model = "runwayml/stable-diffusion-v1-5"  # Работает!
        
    def check_model_status(self, model_name):
        """Проверка статуса модели"""
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code
        except:
            return 500

    def generate_article(self):
        """Генерация статьи через нейросеть"""
        print("🔄 Генерация статьи...")
        
        # Проверяем доступность модели
        status = self.check_model_status(self.text_model)
        if status != 200:
            raise Exception(f"Модель {self.text_model} недоступна (статус: {status})")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "Напиши новостную статью о последних достижениях в области искусственного интеллекта:"
        
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
            f"https://api-inference.huggingface.co/models/{self.text_model}",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка генерации текста: {response.status_code}")
        
        result = response.json()
        
        if not isinstance(result, list) or len(result) == 0:
            raise Exception("Неверный формат ответа от нейросети")
        
        article = result[0]['generated_text'].strip()
        print("✅ Статья сгенерирована")
        return article

    def generate_image(self):
        """Генерация изображения через нейросеть"""
        print("🔄 Генерация изображения...")
        
        # Проверяем доступность модели
        status = self.check_model_status(self.image_model)
        if status != 200:
            raise Exception(f"Модель {self.image_model} недоступна (статус: {status})")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "artificial intelligence, neural network, futuristic technology, digital art"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 20
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.image_model}",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка генерации изображения: {response.status_code}")
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"ai_image_{timestamp}.jpg"
        
        with open(image_filename, 'wb') as f:
            f.write(response.content)
        
        print("✅ Изображение сгенерировано")
        return image_filename

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
            "generated_with_ai": True,
            "model_text": self.text_model,
            "model_image": self.image_model
        }
        
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации"""
        print("🚀 Запуск чистой нейросетевой генерации...")
        print(f"🔑 Токен: {self.hf_token[:10]}...")
        print(f"📝 Модель текста: {self.text_model}")
        print(f"🎨 Модель изображения: {self.image_model}")
        
        # Быстрая проверка моделей
        print("🔍 Проверка доступности моделей...")
        text_status = self.check_model_status(self.text_model)
        image_status = self.check_model_status(self.image_model)
        
        print(f"📝 Текстовая модель: {text_status}")
        print(f"🎨 Модель изображений: {image_status}")
        
        if text_status != 200:
            raise Exception(f"Текстовая модель недоступна: {text_status}")
        if image_status != 200:
            raise Exception(f"Модель изображений недоступна: {image_status}")
        
        article_text = self.generate_article()
        print(f"📄 Длина статьи: {len(article_text)} символов")
        
        image_path = self.generate_image()
        
        tilda_data = self.prepare_for_tilda(article_text, image_path)
        
        print("✅ Чистая генерация завершена!")
        return tilda_data

def main():
    print("🤖 Чистый нейросетевой генератор контента")
    print("=" * 60)
    print("⚠️  Без заглушек и резервных вариантов")
    print("=" * 60)
    
    if 'HF_API_TOKEN' not in os.environ:
        raise Exception("HF_API_TOKEN не установлен в переменных окружения")
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ЧИСТОЙ ГЕНЕРАЦИИ:")
    print(f"📄 Статья: {len(result['content'])} символов")
    print(f"🖼️ Изображение: {result['image_path']}")
    print(f"🤖 Модель текста: {result['model_text']}")
    print(f"🎨 Модель изображения: {result['model_image']}")
    print("=" * 60)
    
    print("\n📋 ПРЕВЬЮ СТАТЬИ:")
    print("=" * 40)
    print(result['content'][:200] + "...")
    print("=" * 40)

if __name__ == "__main__":
    main()
