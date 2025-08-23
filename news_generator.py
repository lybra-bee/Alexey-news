#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import os
import json
import random
import time

class ContentGenerator:
    def __init__(self):
        self.article_templates = [
            """В 2024 году искусственный интеллект продолжает революционизировать различные отрасли. Новые разработки в области машинного обучения позволяют создавать более эффективные и точные модели. 

Крупные tech-компании представили инновационные алгоритмы, способные обрабатывать огромные объемы данных с невероятной скоростью. Особое внимание уделяется этическим аспектам ИИ и разработке прозрачных систем.

В сфере компьютерного зрения достигнут значительный прогресс - современные нейросети могут точно распознавать объекты, лица и даже эмоции. Генеративные модели создают реалистичные изображения и тексты, что открывает новые возможности для креативных индустрий.

Эксперты прогнозируют, что в ближайшие годы ИИ станет неотъемлемой частью повседневной жизни, от умных домов до персональных ассистентов.""",

            """Современные нейронные сети демонстрируют впечатляющие результаты в обработке естественного языка. Новые языковые модели понимают контекст и генерируют осмысленные тексты, почти неотличимые от человеческих.

В 2024 году особый акцент делается на разработке энергоэффективных алгоритмов. Исследователи работают над снижением вычислительной сложности моделей без потери качества их работы.

Развитие open-source сообщества способствует демократизации технологий ИИ. Теперь даже небольшие стартапы могут использовать передовые разработки в своих проектах.

Квантовые вычисления и нейроморфные процессоры promise совершить очередной прорыв в области искусственного интеллекта, значительно ускорив обработку данных.""",

            """Прогресс в области генеративного искусственного интеллекта достиг беспрецедентных масштабов. Всего за последний квартал было представлено несколько инновационных моделей, которые кардинально меняют подход к созданию цифрового контента.

Нейросети теперь способны генерировать не только тексты и изображения, но также видео и музыку высокого качества. Это открывает новые возможности для креативных профессий и развлекательной индустрии.

Важным трендом становится развитие мультимодальных систем, способных одновременно обрабатывать различные типы данных. Такие системы демонстрируют удивительную способность к пониманию контекста."""
        ]
        
        self.image_urls = [
            "https://images.unsplash.com/photo-1677442135135-416f8aa26a5b",
            "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6",
            "https://images.unsplash.com/photo-1535223289827-42f1e9919769",
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485"
        ]

    def generate_article(self):
        """Генерация статьи локально"""
        print("🔄 Генерация статьи...")
        article = random.choice(self.article_templates)
        print("✅ Статья сгенерирована")
        return article

    def download_image(self):
        """Скачивание изображения с Unsplash"""
        print("🔄 Загрузка изображения...")
        
        try:
            image_url = random.choice(self.image_urls)
            # Добавляем параметры для нужного размера
            image_url += "?w=1024&h=512&fit=crop&auto=format"
            
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"article_image_{timestamp}.jpg"
            
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Изображение загружено: {image_filename}")
            return image_filename
            
        except Exception as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
            # Создаем пустой файл как заглушку
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"article_image_{timestamp}.jpg"
            with open(image_filename, 'w') as f:
                f.write("")  # Создаем пустой файл
            print(f"✅ Создан файл-заглушка: {image_filename}")
            return image_filename

    def prepare_for_tilda(self, article_text, image_path):
        """Подготовка данных для Tilda"""
        print("📝 Подготовка данных для Tilda...")
        
        tilda_data = {
            "title": "Новости нейросетей и технологий",
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "content": article_text,
            "image_path": image_path,
            "short_description": article_text[:150] + "..." if len(article_text) > 150 else article_text,
            "tags": ["AI", "нейросети", "технологии", "машинное обучение"]
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
        print("🚀 Запуск генерации контента...")
        
        try:
            # Генерируем статью
            article_text = self.generate_article()
            print(f"📄 Длина статьи: {len(article_text)} символов")
            
            # Загружаем изображение
            image_path = self.download_image()
            
            # Подготавливаем для Tilda
            tilda_data = self.prepare_for_tilda(article_text, image_path)
            
            print("✅ Генерация завершена!")
            return tilda_data
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

def main():
    print("🤖 Генератор новостей AI")
    print("=" * 50)
    
    generator = ContentGenerator()
    result = generator.generate_content()
    
    if result:
        print("\n" + "=" * 50)
        print("📊 РЕЗУЛЬТАТЫ:")
        print(f"📄 Статья: {len(result['content'])} символов")
        print(f"🖼️ Изображение: {result['image_path']}")
        print("💾 Данные сохранены в tilda_data.json и article.txt")
        print("=" * 50)
        
        # Показываем начало статьи
        print("\n📋 Начало статьи:")
        print(result['content'][:200] + "...")
    else:
        print("❌ Не удалось сгенерировать контент")

if __name__ == "__main__":
    main()
