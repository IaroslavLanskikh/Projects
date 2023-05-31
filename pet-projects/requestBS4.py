import requests 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pandas as pd
import time

# Сразу создам DataFrame в который буду собирать
def collect_data():

    df = pd.DataFrame(columns=['Название',
                                'Рейтинг', 
                                'Количество отзывов',
                                'Тип', 
                                'Эпизоды', 
                                'Статус', 
                                'Жанр', 
                                'Первоисточник', 
                                'Сезон', 
                                'Выпуск', 
                                'Студия', 
                                'Рейтинг MPAA', 
                                'Возрастные ограничения', 
                                'Длительность', 
                                'Снят по манге', 
                                'Главные герои'
        
    ])


    useragent = UserAgent()

    # Для проверки количества
    len_links = 0
    done = 0

    # Посмотрел на количество страниц. Всего их 108.
    for num_page in range(1,109):

        time.sleep(5)

        headers = {
        "User-Agent" : useragent.random
        }
        url = f"https://animego.org/anime/filter/status-is-released/apply?sort=createdAt&direction=desc&type=animes&page={num_page}"
        
        try:
            req = requests.get(url, headers=headers)
        except:
            print(f'Skip {num_page} url')
            continue

        soup = BeautifulSoup(req.text, 'lxml')


        links = soup.find_all("div",class_ = "h5 font-weight-normal mb-1")

        # Забираю ссылки со страницы.
        project_links= []
        for row in links:
            link = row.find("a").get("href")   
            project_links.append(link)

        len_links += len(project_links)
        # Перехожу по ссылкам и забираю данные.

        for project_link in project_links:

            headers = {
        "User-Agent" : useragent.random
        }

            time.sleep(1)
            try:
                req = requests.get(project_link, headers)
            except:
                print(f'Skip {project_link} link')
                continue
            soup = BeautifulSoup(req.text,"lxml")

            #Название аниме.
            try:
                title = soup.find("h1").text
            except:
                title = 'Не найдено'
                print('Skip title')

            #Рейтинг аниме.
            try:
                rating = soup.find("div",class_ = "pr-2").find("span",class_ = "rating-value").text
                rating = re.sub("^\s+|\n|\r|\s+$", '', rating)

                rating_count = soup.find("div",class_ = "pr-2").find("div",class_ = "rating-count").text
                rating_count = re.sub("^\s+|\n|\r|\s+$", '', rating_count)
            except:
                rating = 'Нет оценок'
                rating_count = 0
                print('Skip rating')

            #Все остальные данные лежат в dl, который состоит из dt и dd
            try:
                info_columns = soup.find("div",class_ = "anime-info").find_all("dt")
                columns = []
                
                for column in info_columns:
                    
                    col = column.text
                    col = re.sub("^\s+|\n|\r|\s+$", '', col)
                    columns.append(col)
                
                info_values = soup.find("div",class_ = "anime-info").find_all("dd")
                values = []
                
                
                
                for value in info_values:
                    # На странице есть тег dd с классом 'mt-2 col-12', который является разделителем. Надо убрать. 
                    if value.get('class') == ["mt-2","col-12"]:
                        continue
                    # print(value.get('class'))
                    val = value.text
                    val = re.sub("^\s+|\n|\r|\s+$", '', val)
                    values.append(val)
                
                #Добавляю рейтинг и название в списки
                columns.insert(0,'Рейтинг')
                values.insert(0,rating)

                columns.insert(0,'Количество отзывов')
                values.insert(0,rating_count)

                columns.insert(0,'Название')
                values.insert(0,title)
                
                # Создаю словарь для добавления в df
                dict = {}
                for i in range(len(columns)):
                    dict[columns[i]] = values[i]

                # Насколько нормально добавлять таким методом? Вроде это самой простой способ, 
                # но я видел ещё append. Хотел его применить, но написало, что этот метод будет удалён
                # в скором будущем, поэтому используйте pandas.concat. Но мне было лень на него смотреть.
                # Короче: есть ли разница в скорости между способом ниже и concat?
                df.loc[len(df)] = dict
 
                
                done += 1
                # print(headers)
                
            except:
                print('Skip main part')
                continue
                

            print(f'Записано ----- {title}')
        print(f'Страница {num_page} из 108 обработана.')

    df.to_csv('data.csv')


    print(f'Загружено {done} из {len_links}')
    print(f'Процент: {round(done * 100 / len_links,2)}%')
    print('Ура, я победитель!!!')

def main():
    collect_data()

if __name__ == '__main__':
    main()






