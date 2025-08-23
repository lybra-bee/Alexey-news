#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import time

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']  # Обязательный токен
        self.text_model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.image_model = "stabilityai/stable-diffusion-xl-base-1.0"
        
    def wait_for_model(self, model_name, max_wait=300):
        """Ожидание готовности модели"""
        print(f"⏳ Ожидание готовности модели {model_name}...")
        
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    print("✅ Модель готова к работе")
                    return True
                elif response.status_code == 503:
                    print("🔄 Модель загружается...")
                    time.sleep(10)
                else:
                    raise Exception(f"Ошибка модели: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Ошибка: {e}")
                time.sleep(10)
        
        raise Exception(f"Модель {model_name} не загрузилась за {max_wait} секунд")

    def generate_article(self):
        """Генерация статьи через нейросеть"""
        print("🔄 Генерация статьи...")
        
        self.wait_for_model(self.text_model)
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = """<s>[INST] Напиши развернутую новостную статью на 300-400 слов о последних достижениях в области искусственного интеллекта. 
Опиши конкретные технологии, компании и реальные применения. Статья должна быть информативной и уникальной.
Формат: обычный текст без заголовков. [/INST]"""
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 600,
                "temperature": 0.8,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.text_model}",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        response.raise_for_status()
        result = response.json()
        
        if not isinstance(result, list) or len(result) == 0:
            raise Exception("Неверный формат ответа от нейросети")
        
        article = result[0]['generated_text'].strip()
        article = article.replace('[INST]', '').replace('[/INST]', '')
        article = article.split('</s>')[0].strip()
        
        print("✅ Статья сгенерирована")
        return article

    def generate_image(self):
        """Генерация изображения через нейросеть"""
        print("🔄 Генерация изображения...")
        
        self.wait_for_model(self.image_model)
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "futuristic artificial intelligence, neural network concept, digital art, technology, glowing connections, blue and purple colors, high quality, 4k"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
                "negative_prompt": "blurry, low quality, text, watermark"
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.image_model}",
            headers=headers,
            json=payload,
            timeout=180
        )
        
        response.raise_for_status()
        
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
        print(f"🔑 Используется токен: {self.hf_token[:10]}...")
        
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
