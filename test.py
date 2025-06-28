import re

def remove_date_line(text):
    # Регулярное выражение для поиска строки "дата обращения: DD.MM.YYYY"
    pattern = r'\(дата обращения:\s*\d{2}\.\d{2}\.\d{4}\)'

    # Удаляем найденные строки
    cleaned_text = re.sub(pattern, '', text)

    # Удаляем лишние пробелы и пустые строки
    cleaned_text = re.sub(r'\ns*\n', '\n', cleaned_text).strip()

    return cleaned_text

# Пример использования
input_text = """Это пример текста. (дата обращения: 28.06.2025) Этот текст должен остаться."""

output_text = remove_date_line(input_text)
print(output_text)
