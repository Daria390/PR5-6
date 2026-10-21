import csv
import json
import requests

# Параметри програми
INDICATOR = "NE.EXP.GNFS.ZS"  # Експорт товарів і послуг (% від ВВП)
YEARS = "2018:2019"
JSON_FILE = "exports_gdp.json"
CSV_FILE = "exports_gdp.csv"


# Функція отримує дані з API Світового банку і повертає список записів
def get_data():
    url = f"https://api.worldbank.org/v2/country/all/indicator/{INDICATOR}"
    all_records = []
    page = 1
    pages = 1  # Кількість сторінок дізнаємось з першої відповіді

    # API віддає дані сторінками, тому отримуємо їх по черзі
    while page <= pages:
        full_url = f"{url}?date={YEARS}&format=json&per_page=1000&page={page}"
        try:
            response = requests.get(full_url)
        except requests.exceptions.RequestException:
            print("Помилка виконання HTTP-запиту!")
            return None

        if response.status_code != 200:
            print("Не вдалося отримати дані. Код відповіді:", response.status_code)
            return None

        data = response.json()
        # data[0] - службова інформація, data[1] - самі записи
        if len(data) < 2 or data[1] is None:
            print("Дані відсутні!")
            return None

        pages = data[0]["pages"]
        all_records.extend(data[1])
        page += 1

    print("Дані успішно отримано")
    return all_records


# Функція зберігає отримані записи у файл формату JSON
def save_json(records):
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=4)
        print("Створено файл:", JSON_FILE)
        return True
    except OSError:
        print("Помилка запису файлу:", JSON_FILE)
        return False


# Функція відбирає потрібні поля (країна, рік, значення) і зберігає їх у CSV-файл
def save_csv(records):
    rows = []
    for item in records:
        # Пропускаємо записи, де значення відсутнє
        if item.get("value") is not None:
            rows.append([item["country"]["value"], item["date"], item["value"]])

    if not rows:
        print("Немає даних для запису у CSV!")
        return False

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                [
                    "Country Name",
                    "Year",
                    "Exports of goods and services (% of GDP)",
                ]
            )
            writer.writerows(rows)
        print("Створено файл:", CSV_FILE)
        return True
    except OSError:
        print("Помилка запису файлу:", CSV_FILE)
        return False


# Функція виводить на екран перші 5 записів із JSON-файлу
def show_json():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)
    except OSError:
        print("Не вдалося відкрити файл:", JSON_FILE)
        return

    print("\nЗміст JSON:")
    for item in records[:5]:
        print(json.dumps(item, ensure_ascii=False, indent=4))
    print("Усього записів:", len(records))


# Функція виводить на екран перші рядки CSV-файлу
def show_csv():
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError:
        print("Не вдалося відкрити файл:", CSV_FILE)
        return

    print("\nЗміст CSV:")
    for line in lines[:6]:
        print(line.strip())
    print("Усього рядків:", max(0, len(lines) - 1))


# Функція виконує всі дії завдання 1 по черзі
def run_task1():
    records = get_data()
    if records is None:
        return
    if save_json(records) and save_csv(records):
        show_json()
        show_csv()


if __name__ == "__main__":
    run_task1()