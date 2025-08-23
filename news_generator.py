#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ['HF_API_TOKEN']
        # Используем альтернативные API endpoints
        self.text_api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
        self.image_api_url = "https://api-inference.huggingface.co/models/google/ddpm-ema-church-256"
        
    def generate_article(self):
        """Генерация статьи через работающее API"""
        print("🔄 Генерация статьи через GPT-Neo...")
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = "Artificial intelligence news:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 200,
                "temperature": 0.9,
                "do_sample": True,
                "return_full_text": True
            }
        }
        
        try:
            response = requests.post(
                self.text_api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            print(f"📊 Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📦 Получен ответ: {result}")
                
                if isinstance(result, list) and len(result) > 0:
                    article = result[0]['generated_text'].strip()
                    # Убираем промпт из результата
                    if article.startswith(prompt):
                        article = article[len(prompt):].strip()
                    print("✅ Статья сгенерирована")
                    return article
                else:
                    raise Exception("Пустой ответ от API")
            else:
                raise Exception(f"Ошибка API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            # Если API не работает, используем простую генерацию
            return self.generate_fallback_article()

    def generate_fallback_article(self):
        """Простая генерация статьи"""
        print("🔄 Используем базовую генерацию...")
        
        articles = [
            "Современные нейросетевые архитектуры демонстрируют impressive результаты в обработке естественного языка. Новые transformer-based модели показывают unprecedented точность в understanding complex contexts.",
            "Развитие computer vision technologies достигло новых высот. Современные алгоритмы способны accurately распознавать объекты, лица и даже emotions с высочайшей precision.",
            "Generative AI революционизирует creative индустрии. Нейросети теперь создают realistic изображения, музыку и тексты, opening new possibilities для digital art.",
            "Machine learning algorithms становятся более efficient и accessible. Новые разработки позволяют deploy сложные модели на edge устройствах, democratizing AI технологии."
        ]
        
        import random
        return random.choice(articles)

    def generate_image(self):
        """Генерация изображения"""
        print("🔄 Генерация изображения...")
        
        try:
            # Используем разнообразные изображения с Unsplash
            images = [
                "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1024&h=512&fit=crop",
                "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1024&h=512&fit=crop"
            ]
            
            import random
            response = requests.get(random.choice(images), timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"ai_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print("✅ Изображение загружено")
            return image_filename
            
        except Exception as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
            return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости ИИ и технологий",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path or "default.jpg",
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
        print("🚀 Запуск генерации контента...")
        print(f"🔑 Токен: {self.hf_token[:10]}...")
        
        article_text = self.generate_article()
        print(f"📄 Длина статьи: {len(article_text)} символов")
        
        image_path = self.generate_image()
        
        tilda_data = self.prepare_for_tilda(article_text, image_path)
        
        print("✅ Генерация завершена!")
        return tilda_data

def main():
    print("🤖 Генератор контента")
    print("=" * 60)
    print("🚀 Используются доступные API и ресурсы")
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
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
