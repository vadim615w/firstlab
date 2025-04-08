import re
import random
from datetime import datetime

weather = {
    r"москва|москве": ["Облачно", "Дождь", "Солнечно", "Небольшой снег"],
    r"санкт-петербург|санкт-петербурге": ["Пасмурно", "Мелкий дождь", "Ясно", "Легкий ветер"],
    r"новосибирск|новосибирске": ["Морозно", "Снегопад", "Ясно", "Прохладно"],
    r"владивосток|владивостоке": ["Облачно", "Дождь", "Солнечно", "Туманно"],
    r"сочи|сочи": ["Жарко", "Солнечно", "Небольшой дождь", "Тепло"],
    r"нижний|нижний новгород|нижнем|нижнем новгороде": ["Жарко", "Солнечно", "Небольшой дождь", "Тепло"]
}

answers = {
    r"^привет$|^ку$|^здравствуйте$|^доброе утро$|^салют$|^йоу$|^кчау$": "Привет! Как я могу помочь?",
    r"как тебя зовут|имя|какое у тебя имя|\?": "Я бот-помощник!",
    r"что ты умеешь|команды|какие задачи ты умеешь решать|задачи|\?": "Я умею подсказывать время, дату, погоду, вычислять арифметические примеры. Также у меня есть игры: 'подбрось монетку', 'выбери число', 'камень ножницы бумага'.",
    r"который час|время|сколько времени|\?": lambda: f"Текущее время: {datetime.now().strftime('%H:%M:%S')}",
    r"погода$": "Я могу подсказать погоду в Москве, Санкт-Петербурге, Новосибирске, Владивостоке, Сочи и Нижнем Новгороде.",
    r"какая сегодня дата|дата|число|какое сегодня число|\?": lambda: f"Сегодняшняя дата: {datetime.now().strftime('%d.%m.%Y')}",
    r"подбрось монетку|монетка|орел или решка": lambda: f"Результат: {'Орёл' if random.randint(0, 1) == 0 else 'Решка'}",
    r"выбери число|случайное число": lambda: f"Выбираю случайное число от 1 до 10: {random.randint(1, 10)}",
}


def get_weather(city):
    city = city.lower()
    for pattern, weather_list in weather.items():
        if re.search(pattern, city):
            return random.choice(weather_list)
    return None


def parse_weather_request(text):
    weather_patterns = [
        r"погода (\w+)",
        r"погода в (\w+)",
        r"какая погода в (\w+)",
        r"какая погода (\w+)"
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, text.lower())
        if match:
            city = match.group(1)
            weather_result = get_weather(city)
            if weather_result:
                return f"Погода в {city.capitalize()}: {weather_result}"
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
            result = ""

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


def bot_reply(text):
    text = text.lower()

    if "подбрось монетку" in text or "монетка" in text or "орел или решка" in text:
        return f"Результат: {'Орёл' if random.randint(0, 1) == 0 else 'Решка'}"

    if "выбери число" in text or "случайное число" in text:
        return f"Выбираю случайное число от 1 до 10: {random.randint(1, 10)}"

    game_result = play_rps(text)
    if game_result:
        return game_result

    weather_result = parse_weather_request(text)
    if weather_result:
        return weather_result

    math_result = parse_math(text)
    if math_result:
        return math_result

    for pattern, answer in answers.items():
        if re.search(pattern, text):
            return answer() if callable(answer) else answer

    return random.choice([
        "Я не понял вопрос.",
        "Попробуйте перефразировать.",
        "Извините, я не могу ответить на этот вопрос."
    ])


if __name__ == "__main__":
    print("Привет! Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            break
        print("Бот:", bot_reply(user_input))
