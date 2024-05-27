# -_Movie_Recommender
“Кадр” поможет определиться с выбором фильма, опираясь на Ваши предпочтения и вкусы. Отвечайте на вопросы, экономьте свое время и начинайте смотреть фильм прямо сейчас! / "Кадр" will help you decide on the choice of a movie based on your preferences and tastes. Answer the questions, save your time and start watching the movie right now!

Этот проект представляет собой бота для рекомендаций фильмов, созданного с использованием Streamlit и классификатора k-ближайших соседей (KNN). Он предоставляет рекомендации по фильмам на основе выбранных фильмов или жанров, а также получает дополнительную информацию и постеры с IMDb.

## Функциональность

- **Рекомендации по фильмам**: Получите рекомендации по фильмам на основе выбранного фильма или жанров.
- **Постеры фильмов**: Получение и отображение постеров фильмов с IMDb.
- **Информация о фильме**: Отображение дополнительной информации о фильме, такой как режиссер, актерский состав, сюжет и рейтинг IMDb.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone 
    cd movierecommendationbot
    ```

2. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Убедитесь, что у вас есть следующая структура папок:
    ```
    .
    ├── cache
    ├── Data
    │   ├── movie_data.json
    │   └── movie_titles.json
    ├── meta
    │   └── Frame 3.png
    ├── Classifier.py
    ├── app.py
    └── requirements.txt
    ```

## Запуск приложения

1. Запустите приложение Streamlit:
    ```bash
    streamlit run app.py
    ```

2. Откройте браузер и перейдите по адресу `http://localhost:8501`.

## Структура файлов

- **app.py**: Основной файл приложения, содержащий код Streamlit.
- **Classifier.py**: Содержит класс KNearestNeighbours для системы рекомендаций.
- **Data/movie_data.json**: JSON-файл с данными о фильмах.
- **Data/movie_titles.json**: JSON-файл с названиями фильмов.
- **meta**: Изображение, используемое в приложении Streamlit.
- **cache**: Папка для кэширования постеров фильмов.

## Использование

1. Выберите тип рекомендации:
    - **На основе фильма**: Выберите фильм из выпадающего списка для получения рекомендаций.
    - **На основе жанра**: Выберите один или несколько жанров и установите рейтинг IMDb для получения рекомендаций.

2. Просмотрите рекомендуемые фильмы вместе с их постерами и подробной информацией.

## Требования

- Python 3.7 или выше
- Необходимые пакеты Python, указанные в `requirements.txt`

## Вклад

Не стесняйтесь форкнуть этот репозиторий и внести свои изменения. Пулл-реквесты приветствуются!



## Благодарности

- Данные основаны на "IMDB 5000 Movie Dataset".
- В проекте используется Streamlit для веб-интерфейса и BeautifulSoup для веб-скрапинга.

