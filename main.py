import re
import random
import webbrowser
import requests
from datetime import datetime

KEY = "c954e0d06e66e6c55bc1fa26fb7f75d2"


answers = {
    r"^привет$|^ку$|^здравствуйте$|^доброе утро$|^салют$|^йоу$|^кчау$": "Привет! Как я могу помочь?",
    r"как тебя зовут|имя|какое у тебя имя": "Я бот-помощник!",
    r"что ты умеешь|команды|какие задачи ты умеешь решать|задачи": "Я умею подсказывать время, дату, погоду, вычислять арифметические примеры. Также у меня есть игры: 'подбрось монетку', 'выбери число', 'камень ножницы бумага'.",
    r"который час|время|сколько времени": lambda: f"Текущее время: {datetime.now().strftime('%H:%M:%S')}",
    r"какая сегодня дата|дата|число|какое сегодня число": lambda: f"Сегодняшняя дата: {datetime.now().strftime('%d.%m.%Y')}",
    r"подбрось монетку|монетка|орел или решка": lambda: f"Результат: {'Орёл' if random.randint(0, 1) == 0 else 'Решка'}",
    r"выбери число|случайное число": lambda: f"Выбираю случайное число от 1 до 10: {random.randint(1, 10)}",
    r"как дела": lambda: random.choice([
        "Спасибо, что спросили! У меня всё в порядке.",
        "Всё отлично, рад помочь!",
        "Всё хорошо, а как у вас?",
        "Дела прекрасно! А у вас как?"
    ]),
}


def get_real_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&lang=ru&units=metric"
        response = requests.get(url)
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{description.capitalize()}, температура {temp}°C"
    except:
        return None

def parse_weather_request(text):
    weather_patterns = [
        r"погода в ([\w\- ]+)",
        r"какая погода в ([\w\- ]+)",
        r"какая погода ([\w\- ]+)",
        r"погода ([\w\- ]+)"
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, text.lower())
        if match:
            city = match.group(1)
            real_weather = get_real_weather(city)
            if real_weather:
                return f"Погода в {city.capitalize()}: {real_weather}"
            else:
                return "Не удалось получить погоду."
    return None

def parse_math(text):
    try:
        text = text.replace(' ', '')
        if re.match(r'^[0-9\+\-\*/\.]+$', text):
            result = eval(text)
            return f"Результат: {result}"
    except:
        pass
    return None


def play_rps(text):
    game_pattern = r"камень|ножницы|бумага"
    if re.search(game_pattern, text.lower()):
        player_choice = None
        if "камень" in text.lower():
            player_choice = "камень"
        elif "ножницы" in text.lower():
            player_choice = "ножницы"
        elif "бумага" in text.lower():
            player_choice = "бумага"

        if player_choice:
            bot_choice = random.choice(["камень", "ножницы", "бумага"])
            if player_choice == bot_choice:
                result = "Ничья!"
            elif (player_choice == "камень" and bot_choice == "ножницы") or \
                    (player_choice == "ножницы" and bot_choice == "бумага") or \
                    (player_choice == "бумага" and bot_choice == "камень"):
                result = "Вы выиграли!"
            else:
                result = "Я выиграл!"
            return f"Вы: {player_choice}, Я: {bot_choice}. {result}"
    return None


def parse_search_request(text):
    match = re.search(r"поиск (.+)", text.lower())
    if match:
        query = match.group(1)
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Ищу в интернете: {query}"
    return None


def bot_reply(text):
    text = text.strip().lower()
    response = None

    # Игры
    if "монетка" in text or "орел или решка" in text:
        response = f"Результат: {'Орёл' if random.randint(0, 1) == 0 else 'Решка'}"
    elif "выбери число" in text or "случайное число" in text:
        response = f"Выбираю случайное число от 1 до 10: {random.randint(1, 10)}"

    # Камень-ножницы-бумага
    if not response:
        response = play_rps(text)

    # Погода
    if not response:
        response = parse_weather_request(text)

    # Поиск
    if not response:
        response = parse_search_request(text)

    # Математика
    if not response:
        response = parse_math(text)

    # Шаблонные ответы
    if not response:
        for pattern, answer in answers.items():
            if re.search(pattern, text):
                response = answer() if callable(answer) else answer
                break

    # Непонятный вопрос
    if not response:
        response = random.choice([
            "Я не понял вопрос.",
            "Попробуйте перефразировать.",
            "Извините, я не могу ответить на этот вопрос."
        ])

    # Логирование
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"Пользователь: {text}\nБот: {response}\n\n")

    return response


if __name__ == "__main__":
    print("Привет! Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            break
        print("Бот:", bot_reply(user_input))
