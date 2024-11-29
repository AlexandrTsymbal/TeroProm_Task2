import requests
import argparse


def get_weather_data(city: str, api_key: str) -> dict:
    """
    Функция получающая данные о погоде
    с сервиса OpenWeatherMap в формате JSON

    :param city: Город, для которого получается прогноз
    :param api_key: API ключ
    :return: Словарь с кодом ответа и JSONl
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Не удалось получить данные о погоде.")


def parse_weather_data(data: dict) -> dict:
    """
    Функция превращающая JSON данные
    в читаемый формат

    :param data: JSON-данные
    :return: Словарь с полученными данными
    """
    city_name = data['name']
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']

    return {
        "city": city_name,
        "description": weather_description,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed
    }


def save_weather_info_to_file(weather: dict, filename: str):
    """
    Функция сохранения распаршенных данных
    в текстовый файл

    :param weather: Словарь с данными
    :param filename: Путь к выходному файлу
    :return:
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Погода в {weather['city']}:\n")
            file.write(f"Описание: {weather['description']}\n")
            file.write(f"Температура: {weather['temperature']}°C\n")
            file.write(f"Влажность: {weather['humidity']}%\n")
            file.write(f"Давление: {weather['pressure']} гПа\n")
            file.write(f"Скорость ветра: {weather['wind_speed']} м/с\n")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")


if __name__ == "__main__":

    api_key = r'8057335aa7504aa13349506231477c44'

    parser = argparse.ArgumentParser(description="Получить данные о погоде по названию города.")
    parser.add_argument("city", type=str, help="Название города")
    parser.add_argument("output_file", type=str, help="Имя файла для записи информации о погоде")

    args = parser.parse_args()
    try:
        data = get_weather_data(args.city, api_key)
        weather = parse_weather_data(data)
        save_weather_info_to_file(weather, args.output_file)
    except Exception as e:
        print(f"Ошибка: {e}")
