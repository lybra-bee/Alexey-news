#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random

class ContentGenerator:
    def __init__(self):
        # Альтернативные бесплатные API
        self.text_apis = [
            self.try_deepinfra,
            self.try_huggingface,
            self.generate_quality_article
        ]
        
    def generate_article(self):
        """Генерация статьи через доступные API"""
        print("🔄 Поиск работающего API для генерации статьи...")
        
        for api_method in self.text_apis:
            try:
                article = api_method()
                if article:
                    return article
            except Exception as e:
                print(f"⚠️ {api_method.__name__}: {e}")
                continue
        
        # Если все API не сработали
        return self.generate_quality_article()

    def try_deepinfra(self):
        """Пробуем DeepInfra (бесплатный лимит)"""
        print("🔄 Пробуем DeepInfra...")
        
        # DeepInfra API key (можно получить бесплатно)
        api_key = os.environ.get('DEEPINFRA_API_KEY', '')
        if not api_key:
            return None
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "inputs": "Напиши новостную статью о искусственном интеллекте:",
            "parameters": {"max_length": 300}
        }
        
        response = requests.post(
            "https://api.deepinfra.com/v1/inference",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['results'][0]['generated_text']
        return None

    def try_huggingface(self):
        """Пробуем Hugging Face Inference API"""
        print("🔄 Пробуем Hugging Face...")
        
        hf_token = os.environ.get('HF_API_TOKEN', '')
        if not hf_token:
            return None
            
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": "Создай новость о технологиях ИИ:",
            "parameters": {"max_length": 250}
        }
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]['generated_text']
        return None

    def generate_quality_article(self):
        """Качественная генерация статьи"""
        print("🔄 Генерация качественной статьи локально...")
        
        technologies = [
            "трансформерные архитектуры", "нейронные сети", "генеративный ИИ", 
            "компьютерное зрение", "обработка естественного языка", "обучение с подкреплением",
            "мультимодальные системы", "квантовые вычисления", "нейроморфные процессоры"
        ]
        
        companies = [
            "OpenAI", "Google DeepMind", "Microsoft Research", "Meta AI", "NVIDIA", 
            "Anthropic", "Hugging Face", "Stability AI", "Tesla AI", "Amazon Web Services"
        ]
        
        applications = [
            "медицинской диагностике", "автономных транспортных средствах", "создании цифрового контента",
            "научных исследованиях", "финансовой аналитике", "образовательных платформах",
            "кибербезопасности", "робототехнике", "умных городах"
        ]
        
        achievements = [
            "добились значительного прорыва в области", "представили инновационную разработку",
            "анонсировали новейшую модель", "достигли рекордных показателей точности",
            "разработали революционный алгоритм", "улучшили энергоэффективность систем"
        ]
        
        impacts = [
            "кардинально изменить подход к", "существенно ускорить внедрение",
            "демократизировать доступ к", "создать новые возможности для",
            "революционизировать область", "повысить эффективность"
        ]
        
        tech = random.choice(technologies)
        company = random.choice(companies)
        app = random.choice(applications)
        achievement = random.choice(achievements)
        impact = random.choice(impacts)
        
        article = f"""
{company} {achievement} {tech}. Новое решение демонстрирует беспрецедентные результаты в {app}, 
показывая на 40% лучшую производительность по сравнению с предыдущими поколениями технологий.

Эксперты отмечают, что данная разработка может {impact} решению сложных задач и ускорить 
внедрение искусственного интеллекта в повседневную жизнь. Технология уже проходит тестирование 
в реальных условиях и показывает promising результаты.

Развитие open-source сообщества способствует демократизации передовых технологий, делая их 
доступными для более широкого круга разработчиков и исследователей. Это ускоряет инновационный 
процесс и создает условия для появления новых breakthrough решений в области {tech}.

По словам аналитиков, в 2024 году ожидается дальнейший рост инвестиций в исследования 
и разработки искусственного интеллекта, что приведет к появлению еще более совершенных 
и эффективных систем.
"""
        
        return article.strip()

    def generate_image(self):
        """Генерация качественного изображения"""
        print("🔄 Загрузка изображения...")
        
        # Альтернативные источники изображений
        image_sources = [
            self.try_unsplash,
            self.try_pexels,
            self.try_picsum
        ]
        
        for source_method in image_sources:
            try:
                image_path = source_method()
                if image_path:
                    return image_path
            except Exception as e:
                print(f"⚠️ {source_method.__name__}: {e}")
                continue
        
        return None

    def try_unsplash(self):
        """Пробуем Unsplash"""
        themes = ["technology", "computer", "network", "data", "ai", "future"]
        theme = random.choice(themes)
        url = f"https://source.unsplash.com/1024x512/?{theme}"
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        filename = f"article_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print("✅ Изображение с Unsplash")
        return filename

    def try_pexels(self):
        """Пробуем Pexels"""
        themes = ["technology", "computer", "data", "innovation", "digital"]
        theme = random.choice(themes)
        url = f"https://images.pexels.com/photos/1024/512?{theme}"
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        filename = f"article_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print("✅ Изображение с Pexels")
        return filename

    def try_picsum(self):
        """Пробуем Picsum"""
        image_id = random.randint(1, 1000)
        url = f"https://picsum.photos/1024/512?image={image_id}"
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        filename = f"article_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print("✅ Изображение с Picsum")
        return filename

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        titles = [
            "Инновации в мире искусственного интеллекта",
            "Прорывные технологии машинного обучения", 
            "Новейшие разработки в области нейросетей",
            "Современные достижения компьютерных наук"
        ]
        
        tilda_data = {
            "title": random.choice(titles),
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path or "default.jpg",
            "short_description": article_text[:150] + "..." if len(article_text) > 150 else article_text,
            "tags": ["AI", "нейросети", "технологии", "машинное обучение"],
            "generated_with_ai": True,
            "source": "Качественная локальная генерация"
        }
        
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации"""
        print("🚀 Запуск интеллектуальной генерации контента...")
        print("🔍 Поиск лучших доступных источников...")
        print("=" * 60)
        
        article_text = self.generate_article()
        print(f"📄 Длина статьи: {len(article_text)} символов")
        
        image_path = self.generate_image()
        
        tilda_data = self.prepare_for_tilda(article_text, image_path)
        
        print("✅ Генерация завершена успешно!")
        return tilda_data

def main():
    print("🤖 Умный генератор новостей AI")
    print("=" * 60)
    print("🎯 Многоуровневая система генерации")
    print("⚡ Автоматический выбор лучшего источника")
    print("=" * 60)
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ:")
    print(f"📄 Статья: {len(result['content'])} символов")
    print(f"🖼️ Изображение: {result['image_path'] or 'не сгенерировано'}")
    print(f"🏷️ Теги: {', '.join(result['tags'])}")
    print(f"🔧 Источник: {result['source']}")
    print("💾 Данные сохранены в article.txt и tilda_data.json")
    print("=" * 60)
    
    print("\n📋 ПРЕВЬЮ СТАТЬИ:")
    print("=" * 40)
    print(result['content'][:200] + "...")
    print("=" * 40)

if __name__ == "__main__":
    main()
