import csv

CSV_FILE = "exports_gdp.csv"  # Файл, створений у завданні 1


# Функція запитує в користувача назви країн (через кому) та перевіряє введення
def input_countries():
    while True:
        text = input("Введіть назви країн англійською через кому (наприклад: Ukraine, Poland): ")
        countries = []
        for name in text.split(","):
            name = name.strip()
            if name != "":
                countries.append(name)

        if len(countries) == 0:
            print("Помилка: потрібно ввести хоча б одну назву країни!")
            continue

        # Назва країни не може містити цифр
        has_digit = False
        for name in countries:
            for symbol in name:
                if symbol.isdigit():
                    has_digit = True
                    break
            if has_digit:
                break

        if has_digit:
            print("Помилка: назва країни не може містити цифри!")
            continue

        return countries


# Функція запитує назву файлу, у який будуть записані результати пошуку
def input_filename():
    name = input("Введіть назву файлу для результатів: ").strip()
    if name == "":
        name = "result"
    if not name.endswith(".csv"):
        name = name + ".csv"
    return name


# Функція шукає в CSV-файлі рядки для введених країн
def search(countries):
    results = []
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            rows = list(reader)
    except FileNotFoundError:
        print("Файл", CSV_FILE, "не знайдено! Спочатку виконайте завдання 1.")
        return results

    for country in countries:
        found = False
        for row in rows:
            # Порівняння без урахування великих і малих літер
            if row["Country Name"].lower() == country.lower():
                results.append(row)
                found = True
        if not found:
            print("Країну", country, "не знайдено.")
    return results


# Функція зберігає результати пошуку в новий CSV-файл із заголовками
def save_results(results, filename):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Country Name", "Year", "Exports of goods and services (% of GDP)"])
            for row in results:
                writer.writerow([
                    row["Country Name"],
                    row["Year"],
                    row["Exports of goods and services (% of GDP)"]
                ])
        print("Результати успішно збережено у файл:", filename)
    except OSError:
        print("Помилка запису файлу:", filename)


# Функція виконує всі дії завдання 2 по черзі
def run_task2():
    countries = input_countries()
    results = search(countries)

    if len(results) == 0:
        print("Збігів не знайдено.")
        return

    print("\nРезультати пошуку:")
    for row in results:
        print(row["Country Name"], row["Year"], row["Exports of goods and services (% of GDP)"])

    filename = input_filename()
    save_results(results, filename)


if __name__ == "__main__":
    run_task2()