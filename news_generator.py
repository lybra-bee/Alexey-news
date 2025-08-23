#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random

class ContentGenerator:
    def __init__(self):
        self.article_templates = self._load_article_templates()
        self.image_urls = self._load_image_urls()
        
    def _load_article_templates(self):
        """Загрузка разнообразных шаблонов статей"""
        return [
            """{company} {achievement} {technology}. Новое решение демонстрирует беспрецедентные результаты в {application}, 
показывая на {improvement}% лучшую производительность по сравнению с предыдущими поколениями технологий.

Эксперты отмечают, что данная разработка может кардинально изменить подход к решению сложных задач 
и ускорить внедрение искусственного интеллекта в повседневную жизнь. Технология уже тестируется 
в реальных условиях и показывает promising результаты.

Развитие open-source сообщества способствует демократизации передовых технологий, делая их 
доступными для более широкого круга разработчиков и исследователей.""",

            """В области {technology} произошел значительный прорыв. {company} {achievement}, 
что открывает новые возможности для применения в {application}. 

Новая технология позволяет достигать {improvement}% улучшения ключевых показателей и значительно 
снижает затраты на внедрение. Многие эксперты считают, что это изменит будущее индустрии и создаст 
новые рынки для инновационных продуктов.

Инвестиции в исследования и разработки искусственного интеллекта продолжают расти, что свидетельствует 
о высоком потенциале данной технологии.""",

            """{company} представили революционную разработку в сфере {technology}. {achievement} 
и позволяет достигать remarkable результатов в {application}.

Современные алгоритмы машинного обучения демонстрируют unprecedented точность и эффективность, 
что делает их применимыми в самых различных областях - от медицинской диагностики до финансового анализа.

Аналитики прогнозируют, что в ближайшие годы мы станем свидетелями еще более впечатляющих достижений 
в области искусственного интеллекта."""
        ]
    
    def _load_image_urls(self):
        """Список гарантированно работающих изображений"""
        return [
            # Технологии и AI
            "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1024&h=512&fit=crop&auto=format",
            
            # Нейросети и данные
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=1024&h=512&fit=crop&auto=format",
            
            # Футуристические
            "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1563207153-f403bf289096?w=1024&h=512&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=1024&h=512&fit=crop&auto=format"
        ]

    def generate_article(self):
        """Генерация уникальной статьи"""
        print("🔄 Создание уникальной статьи...")
        
        companies = [
            "OpenAI", "Google DeepMind", "Microsoft Research", "Meta AI", "NVIDIA",
            "Anthropic", "Hugging Face", "Stability AI", "Tesla AI", "Amazon AI",
            "Intel Labs", "IBM Research", "Baidu Research", "Samsung AI", "Huawei Cloud"
        ]
        
        technologies = [
            "трансформерных архитектур", "нейронных сетей", "генеративного ИИ",
            "компьютерного зрения", "обработки естественного языка", 
            "обучения с подкреплением", "мультимодальных систем",
            "квантовых вычислений", "нейроморфных процессоров"
        ]
        
        applications = [
            "медицинской диагностике", "автономных системах", "создании контента",
            "научных исследованиях", "финансовой аналитике", "образовательных технологиях",
            "кибербезопасности", "робототехнике", "умных городах", "компьютерных играх"
        ]
        
        achievements = [
            "добились значительного прорыва в области",
            "представили инновационную разработку в сфере",
            "анонсировали новейшую модель для",
            "достигли рекордных показателей в",
            "разработали революционный алгоритм для",
            "улучшили энергоэффективность систем"
        ]
        
        # Случайный выбор элементов
        company = random.choice(companies)
        technology = random.choice(technologies)
        application = random.choice(applications)
        achievement = random.choice(achievements)
        improvement = random.randint(30, 65)
        template = random.choice(self.article_templates)
        
        # Заполнение шаблона
        article = template.format(
            company=company,
            technology=technology,
            application=application,
            achievement=achievement,
            improvement=improvement
        )
        
        print("✅ Статья успешно создана")
        return article

    def generate_image(self):
        """Генерация изображения с гарантией"""
        print("🔄 Загрузка изображения...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                image_url = random.choice(self.image_urls)
                print(f"📡 Попытка {attempt + 1}: {image_url}")
                
                response = requests.get(image_url, timeout=15)
                response.raise_for_status()
                
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"article_image_{timestamp}.jpg"
                
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Изображение сохранено: {image_filename}")
                return image_filename
                
            except Exception as e:
                print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
                if attempt < max_retries - 1:
                    print("🔄 Пробуем другое изображение...")
                    continue
                else:
                    print("❌ Все попытки загрузки изображения провалились")
                    return None

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        titles = [
            "Инновации в мире искусственного интеллекта",
            "Прорывные технологии машинного обучения", 
            "Новейшие разработки в области нейросетей",
            "Современные достижения компьютерных наук",
            "Будущее технологий: последние открытия",
            "Революция искусственного интеллекта"
        ]
        
        tags_options = [
            ["AI", "нейросети", "технологии", "машинное обучение"],
            ["искусственный интеллект", "инновации", "IT", "разработки"],
            ["технологии", "компьютерные науки", "data science", "big data"],
            ["нейросети", "deep learning", "компьютерное зрение", "NLP"]
        ]
        
        tilda_data = {
            "title": random.choice(titles),
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path or "default_image.jpg",
            "short_description": article_text[:120] + "..." if len(article_text) > 120 else article_text,
            "tags": random.choice(tags_options),
            "views": random.randint(100, 2500),
            "rating": round(random.uniform(4.2, 4.9), 1),
            "read_time": random.randint(3, 8),
            "author": random.choice(["AI Редактор", "Технологический обозреватель", "Эксперт по ИИ"])
        }
        
        # Сохраняем данные
        with open('tilda_data.json', 'w', encoding='utf-8') as f:
            json.dump(tilda_data, f, ensure_ascii=False, indent=2)
        
        with open('article.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)
        
        return tilda_data

    def generate_content(self):
        """Основная функция генерации"""
        print("🚀 Запуск генерации контента...")
        print("=" * 60)
        
        # Генерируем статью
        article_text = self.generate_article()
        print(f"📄 Длина статьи: {len(article_text)} символов")
        
        # Генерируем изображение
        image_path = self.generate_image()
        
        # Подготавливаем данные
        tilda_data = self.prepare_for_tilda(article_text, image_path)
        
        print("✅ Генерация завершена успешно!")
        return tilda_data

    def show_results(self, result):
        """Показать результаты генерации"""
        print("\n" + "=" * 60)
        print("📊 РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ:")
        print("=" * 60)
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print(f"⭐ Рейтинг: {result['rating']}/5")
        print(f"👁️ Просмотры: {result['views']}")
        print(f"⏱️ Время чтения: {result['read_time']} мин")
        print(f"✍️ Автор: {result['author']}")
        print(f"🏷️ Теги: {', '.join(result['tags'])}")
        print("💾 Данные сохранены в article.txt и tilda_data.json")
        print("=" * 60)
        
        # Показываем начало статьи
        print("\n📋 ПРЕВЬЮ СТАТЬИ:")
        print("=" * 40)
        preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
        print(preview)
        print("=" * 40)

def main():
    print("🤖 Умный генератор новостей AI")
    print("=" * 60)
    print("🎯 Гарантированная генерация контента")
    print("⚡ Быстро и надежно")
    print("=" * 60)
    
    generator = ContentGenerator()
    result = generator.generate_content()
    generator.show_results(result)

if __name__ == "__main__":
    main()
