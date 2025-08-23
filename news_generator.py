#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import time

class ContentGenerator:
    def __init__(self):
        self.hf_token = os.environ.get('HF_API_TOKEN', '')
        self.text_model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.image_model = "stabilityai/stable-diffusion-2-1"
        
    def wait_for_model(self, model_name):
        """Ожидание готовности модели"""
        print(f"⏳ Ожидание готовности модели {model_name}...")
        
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        for attempt in range(12):  # 2 минуты ожидания
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
        
        if not self.wait_for_model(self.text_model):
            return self.create_fallback_article()
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompt = """<s>[INST] Напиши новостную статью на 250-300 слов о последних достижениях в области искусственного интеллекта. 
        Опиши конкретные технологии, компании и их применение. Статья должна быть информативной и уникальной.
        Формат: обычный текст без заголовков. [/INST]"""
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.8,
                "top_p": 0.9,
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
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    article = result[0]['generated_text'].strip()
                    # Очищаем от тегов инструкций
                    article = article.replace('[INST]', '').replace('[/INST]', '')
                    article = article.split('</s>')[0].strip()
                    print("✅ Статья сгенерирована нейросетью")
                    return article
            
            print("⚠️ Нейросеть вернула неожиданный ответ, используем fallback")
            return self.create_fallback_article()
            
        except Exception as e:
            print(f"❌ Ошибка генерации: {e}")
            return self.create_fallback_article()

    def create_fallback_article(self):
        """Резервная генерация статьи"""
        print("🔄 Используем резервную генерацию...")
        
        themes = [
            "OpenAI представила новую версию GPT-4 с улучшенными возможностями понимания контекста",
            "Google DeepMind анонсировал прорыв в области reinforcement learning",
            "Новые архитектуры трансформеров демонстрируют беспрецедентную эффективность",
            "Развитие мультимодальных моделей позволяет обрабатывать текст, изображения и аудио одновременно"
        ]
        
        details = [
            "Эта технология позволяет значительно улучшить качество генерации текста и понимание сложных запросов.",
            "Исследователи добились значительного прогресса в области обучения с подкреплением для сложных сред.",
            "Современные модели показывают на 40% лучшую производительность при меньших вычислительных затратах.",
            "Новые подходы к обучению позволяют создавать более универсальные и адаптивные системы ИИ."
        ]
        
        applications = [
            "Технология уже применяется в customer service, образовании и научных исследованиях.",
            "Разработка открывает новые возможности для создания автономных систем и робототехники.",
            "Улучшенная эффективность позволяет развертывать модели на менее мощном оборудовании.",
            "Мультимодальные системы находят применение в медицине, анализе данных и творческих индустриях."
        ]
        
        article = (
            f"{random.choice(themes)}. {random.choice(details)} "
            f"{random.choice(applications)} Эксперты отмечают, что это открывает новые "
            f"горизонты для развития искусственного интеллекта и его интеграции в повседневную жизнь."
        )
        
        return article

    def generate_image(self):
        """Генерация изображения через нейросеть"""
        print("🔄 Генерация изображения через нейросеть...")
        
        if not self.wait_for_model(self.image_model):
            return self.download_fallback_image()
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        prompts = [
            "futuristic artificial intelligence concept, neural networks, digital brain, glowing connections, blue and purple light, cyberpunk style, high technology, intricate details, 4k resolution",
            "abstract neural network architecture, data flow, connections, futuristic technology, digital art, vibrant colors, complex patterns, AI concept, machine learning",
            "high-tech AI system, quantum computing, holographic interface, futuristic technology, glowing elements, sci-fi style, advanced robotics, innovation"
        ]
        
        payload = {
            "inputs": random.choice(prompts),
            "parameters": {
                "width": 1024,
                "height": 512,
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            }
        }
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.image_model}",
                headers=headers,
                json=payload,
                timeout=180
            )
            
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"ai_image_{timestamp}.jpg"
                
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print("✅ Изображение сгенерировано нейросетью")
                return image_filename
            
            print("⚠️ Нейросеть изображений не ответила, используем fallback")
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
            
        except:
            print("❌ Не удалось загрузить резервное изображение")
            return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости ИИ и нейросетей",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path,
            "short_description": article_text[:120] + "..." if len(article_text) > 120 else article_text,
            "tags": ["AI", "нейросети", "технологии", "машинное обучение"],
            "generated_with_ai": True,
            "model_used": self.text_model
        }
        
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации"""
        print("🚀 Запуск нейросетевой генерации...")
        print(f"🔑 Токен: {'есть' if self.hf_token else 'отсутствует'}")
        
        try:
            # Генерируем статью
            article_text = self.generate_article()
            print(f"📄 Длина: {len(article_text)} символов")
            
            # Генерируем изображение
            image_path = self.generate_image()
            
            # Подготавливаем данные
            tilda_data = self.prepare_for_tilda(article_text, image_path)
            
            print("✅ Нейросетевая генерация завершена!")
            return tilda_data
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            return None

def main():
    print("🤖 Нейросетевой генератор контента")
    print("=" * 50)
    
    if not os.environ.get('HF_API_TOKEN'):
        print("⚠️  Внимание: HF_API_TOKEN не установлен")
        print("💡 Добавьте токен в Secrets GitHub")
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    if result:
        print("\n" + "=" * 50)
        print("📊 РЕЗУЛЬТАТЫ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print(f"🤖 Сгенерировано нейросетью: {result['generated_with_ai']}")
        print("💾 Данные сохранены")
        print("=" * 50)
        
        print("\n📋 ПРЕВЬЮ:")
        print(result['content'][:200] + "...")
    else:
        print("❌ Генерация не удалась")

if __name__ == "__main__":
    import random
    main()
