import requests
import pandas as pd

# Запрос вытягивает только вакансии по следующим фильтрам:
# Фильтры именно такие, т.к. HH API ограничение на 2к вакансий
# 1) Уровень дохода: Указан доход
# 2) Регион: Россия
# 3) Специализация: Аналитикогj
# 4) Запрос в поиске: Аналитик
def get_request(page=0):
    # Запрос к HH
    url = 'https://api.hh.ru/vacancies'
    params = {"area": 113,  # Вся Россия
              "professional_role": 10,  # Специализация(Аналитик)
              "only_with_salary": True,  # Только с указанной зарплатой
              "text": "Аналитик",  # Текст, который я ввёл для поиска
              "per_page": 100,  #
              "page": page  #
              }
    # print(url+params)

    response = requests.get(url, params)
    data = response.json()
    return data


def creating_dataframe():
    df = pd.DataFrame(columns=['vacancy_name',
                               'area_name',
                               'salary_from',
                               'salary_to',
                               'url',
                               'experience',
                               ])
    return df



def main_part():

    df = creating_dataframe()
    # print('Done df')
    for count_page in range(0,20):

        request  = get_request(count_page)['items'] # Из get_request возвращается словарь, беру ключ 'items'
        # print('Done request')
                # Добавляет все нужные данные в df
        for i in range(len(request)):
            vacancy_name = request[i]['name']
            area_name = request[i]['area']['name']
            salary_from = request[i]['salary']['from']
            salary_to = request[i]['salary']['to']
            url = request[i]['alternate_url']
            experience = request[i]['experience']['id']

            df.loc[len(df.index)] = [vacancy_name, area_name, salary_from, salary_to, url, experience]

        print(f'Страница {count_page} загружена')



    df.to_csv(r'C:\all\pet_hh\data_hh.csv',index=False)

    print('Файл загружен')

    return     len(df)


if __name__ == '__main__':
    main_part()

