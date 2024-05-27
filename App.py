import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours
from bs4 import BeautifulSoup
import requests
import io
import PIL.Image
from urllib.request import urlopen
import os

CACHE_FOLDER = './cache'  # Папка для кэширования изображений
os.makedirs(CACHE_FOLDER, exist_ok=True)


# Загрузка данных из JSON-файла
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f"File {file_path} not found.")
        return None


data = load_data('./Data/movie_data.json')
movie_titles = load_data('./Data/movie_titles.json')

if not data or not movie_titles:
    st.stop()

hdr = {'User-Agent': 'Mozilla/5.0'}  # Заголовки для запросов HTTP


# Функция для получения данных с веб-страницы по URL
def fetch_url_data(url):
    try:
        response = requests.get(url, headers=hdr)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"Error fetching data from URL: {e}")
        return None


# Функция для получения постера фильма из IMDb
def movie_poster_fetcher(imdb_link):
    url_data = fetch_url_data(imdb_link)
    if url_data:
        s_data = BeautifulSoup(url_data, 'html.parser')
        imdb_dp = s_data.find("meta", property="og:image")
        if imdb_dp:
            movie_poster_link = imdb_dp.attrs['content']
            # Проверяем, есть ли изображение в кэше
            cache_filename = os.path.join(CACHE_FOLDER, movie_poster_link.split('/')[-1])
            if os.path.exists(cache_filename):
                # Используем изображение из кэша
                image = PIL.Image.open(cache_filename)
            else:
                try:
                    u = urlopen(movie_poster_link)
                    raw_data = u.read()
                    image = PIL.Image.open(io.BytesIO(raw_data))
                    image = image.resize((158, 301))
                    # Сохраняем изображение в кэше
                    image.save(cache_filename)
                except Exception as e:
                    st.error(f"Error fetching movie poster: {e}")
                    return
            st.image(image, use_column_width=False)


# Функция для получения информации о фильме с IMDb
def get_movie_info(imdb_link):
    url_data = fetch_url_data(imdb_link)
    if url_data:
        s_data = BeautifulSoup(url_data, 'html.parser')

        director_tag = s_data.find("a", {"data-testid": "title-pc-principal-credit"})
        movie_director = director_tag.text if director_tag else "Director information not available"

        cast_tags = s_data.select("a[data-testid='title-cast-item__actor']")
        movie_cast = ", ".join(tag.text for tag in cast_tags[:5]) if cast_tags else "Cast information not available"

        story_tag = s_data.find("span", {"data-testid": "plot-l"})
        movie_story = story_tag.text.strip() if story_tag else "Story information not available"

        rating_tag = s_data.find("span", {"class": "sc-7ab21ed2-1 jGRxWM"})
        movie_rating = f'IMDB Rating: {rating_tag.text}⭐' if rating_tag else 'Rating not available'

        return movie_director, movie_cast, movie_story, movie_rating
    return "Director information not available", "Cast information not available", "Story information not available", "Rating not available"


# Функция для рекомендации фильмов с использованием классификатора k-ближайших соседей
def KNN_Movie_Recommender(test_point, k, sort_by_rating=False):
    target = [0 for _ in movie_titles]
    model = KNearestNeighbours(data, target, test_point, k=k)
    model.fit()
    table = []
    for i in model.indices:
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])

    if sort_by_rating:
        table = sorted(table, key=lambda x: x[2], reverse=True)

    return table


# Функция для отображения информации о фильме
def display_movie_info(movie, link, ratings):
    director, cast, story, total_rat = get_movie_info(link)
    st.markdown(f"### [{movie}]({link})")
    st.markdown(f"**Director:** {director}")
    st.markdown(f"**Cast:** {cast}")
    st.markdown(f"**Story:** {story}")
    st.markdown(f"**Rating:** {total_rat}")
    st.markdown('IMDB Rating: ' + str(ratings) + '⭐')


# Функция для получения информации о фильме по названию
def get_movie_by_title(movie_title):
    for title_info in movie_titles:
        if movie_title.lower() in title_info[0].lower():
            return title_info
    return None


st.set_page_config(page_title="Бот для рекомендаций фильмов")  # Настройка страницы Streamlit


# Основная функция для запуска приложения
def run():
    img1 = Image.open('./meta/Frame 3.png')
    img1 = img1.resize((1024, 768))
    st.image(img1, use_column_width=False)
    st.title("Бот для рекомендаций фильмов")
    st.markdown(
        '<h4 style="text-align: left; color: #d73b5c;">* Данные основаны на "Наборе данных о фильмах IMDB 5000".</h4>',
        unsafe_allow_html=True)

    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV',
              'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Выбрать--', 'Основанный на фильме', 'Основанный на жанре']

    cat_op = st.selectbox('Выберите тип рекомендации', category)

    if cat_op == category[0]:
        st.warning('Пожалуйста, выберите тип рекомендации!!')
    elif cat_op == category[1]:
        select_movie = st.selectbox('Выберите фильм: (Рекомендации будут основаны на этом выборе)',
                                    ['--Выбрать--'] + movies)
        dec = st.radio("Хотите посмотреть афишу на фильм?", ('Да', 'Нет'))
        st.markdown('<h4 style="text-align: left; color: #d73b5c;">* Поиск афиш фильмов займет некоторое время.</h4>',
                    unsafe_allow_html=True)

        if select_movie == '--Выбрать--':
            st.warning('Пожалуйста, выберите фильм!!')
        else:
            no_of_reco = st.slider('Количество фильмов:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(select_movie)]
            test_points = genres
            table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
            table.pop(0)
            st.success('Ниже приведены некоторые фильмы из нашей рекомендации.')
            for movie, link, ratings in table:
                if dec == 'Да':
                    movie_poster_fetcher(link)
                display_movie_info(movie, link, ratings)
    elif cat_op == category[2]:
        sel_gen = st.multiselect('Выберите жанр:', genres)
        dec = st.radio("Хотите посмотреть афишу на фильм?", ('Да', 'Нет'))
        st.markdown('<h4 style="text-align: left; color: #d73b5c;">* Поиск афиш фильмов займет некоторое время.</h4>',
                    unsafe_allow_html=True)

        if sel_gen:
            imdb_score = st.slider('Выберите рейтинг IMDb:', 1, 10, 8)
            no_of_reco = st.number_input('Количество фильмов:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in sel_gen else 0 for genre in genres]
            test_point.append(imdb_score)

            # Проверка, что test_point имеет правильную размерность
            if len(test_point) != len(data[0]):
                st.error("Неправильная размерность тестовой точки")
                return

            # Проверка, что количество фильмов для рекомендации не превышает количество доступных фильмов
            if no_of_reco > len(movie_titles):
                st.error("Количество запрошенных рекомендаций превышает количество доступных фильмов")
                return

            table = KNN_Movie_Recommender(test_point, no_of_reco, sort_by_rating=True)
            st.success('Ниже приведены некоторые фильмы из нашей рекомендации.')
            for movie, link, ratings in table:
                if dec == 'Да':
                    movie_poster_fetcher(link)
                display_movie_info(movie, link, ratings)


run()
