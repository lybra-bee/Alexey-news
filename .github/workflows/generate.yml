name: Generate AI Content

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: pip install requests

    - name: Generate content
      run: python news_generator.py

    - name: List generated files
      run: ls -la

    - name: Check if files exist
      run: |
        if [ -f "article.txt" ] && [ -f "tilda_data.json" ]; then
          echo "✅ Основные файлы созданы"
          # Ищем файлы изображений
          IMAGE_FILES=$(find . -name "article_image_*.jpg" -type f)
          if [ -n "$IMAGE_FILES" ]; then
            echo "✅ Найдены файлы изображений:"
            echo "$IMAGE_FILES"
          else
            echo "⚠️ Файлы изображений не найдены, создаем заглушку"
            touch "article_image_placeholder.jpg"
          fi
        else
          echo "❌ Основные файлы не созданы"
          exit 1
        fi

    - name: Add all generated files
      run: |
        git config --local user.email "github-actions@github.com"
        git config --local user.name "GitHub Actions"
        # Добавляем все сгенерированные файлы
        git add article.txt tilda_data.json
        # Добавляем любые jpg файлы
        git add *.jpg || echo "No jpg files to add"
        # Проверяем есть ли изменения для коммита
        if git diff --staged --quiet; then
          echo "No changes to commit"
        else
          git commit -m "Auto-generated content $(date +'%Y-%m-%d %H:%M')"
          git push
        fi

    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: generated-content
        path: |
          article.txt
          tilda_data.json
          *.jpg
