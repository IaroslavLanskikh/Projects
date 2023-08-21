import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
from matplotlib import style

# Задаю стиль
plt.style.use('ggplot')

# Читаем данные
df = pd.read_csv('data_hh.csv')

# Меняю названия в столбце.
df['experience'] = df['experience'].replace('between1And3','1-3')
df['experience'] = df['experience'].replace('between3And6','3-6')
df['experience'] = df['experience'].replace('noExperience','0')
df['experience'] = df['experience'].replace('moreThan6','6+')

# Подготовка данных.
df_mean = df.copy()

df_mean = df_mean[['url','salary_from','salary_to']]
df_mean['salary_from'].fillna(df_mean['salary_to'], inplace=True)
df_mean['salary_to'].fillna(df_mean['salary_from'], inplace=True)

df_mean['mean'] = (df_mean['salary_from'] + df_mean['salary_to']) / 2
df_mean = df_mean[['url','mean']]

df = df.merge(df_mean,how='inner',on='url')
# Создаю группы
def find_spec(row):
    if row.lower().find('маркет') != -1:
        return 'Маркет'
    elif row.lower().find('1c') != -1 or row.lower().find('1с') != -1:
        return '1C'
    elif row.lower().find('системн') != -1:
        return 'Системный'
    elif row.lower().find('бизнес') != -1:
        return 'Бизнес'
    elif row.lower().find('продукт') != -1:
        return 'Продуктовый'
    elif row.lower().find('веб') != -1 or row.lower().find('web') != -1:
        return 'Веб'
    else:
        return 'Остальное'

# Применяю функцию выше
df['specialization'] = df.apply(lambda row: find_spec(row['vacancy_name']), axis=1)

# Первая таблица для построения графиков(Направления):
for_graph = df.groupby('specialization',as_index=False) \
            .agg({'mean':'mean','url':'count'}) \
            .round()
for_graph['mean'] = ((for_graph['mean'] / 1000).round()) * 1000
for_graph = for_graph.sort_values('mean', ascending=False).reset_index(drop=True)

# Порядок отображения столбцов:
order = for_graph['specialization']

# Вторая таблица для построения графиков(Город):
area_graph = df.groupby('area_name',as_index=False) \
        .agg({'mean':'mean','url':'count'}) \
        .round()

area_graph['mean'] = (( area_graph['mean'] / 1000 ).round()) * 1000
area_graph = area_graph.sort_values('url',ascending=False)
# Третья таблица для графиков(Опыт):

for_graph_exp = df.groupby('experience',as_index=False).agg({'mean':'mean','url':'count'})
for_graph_exp['mean'] = (((for_graph_exp['mean'] / 1000).round()) * 1000).astype(int)

# Символ рубля:
rub_symbol = '\u20bd'

fig, axs = plt.subplots(ncols=4, nrows=5,figsize=(15,27))

# ФАКТОИДЫ НАЧАЛО.
# --------------------------------------------------------------------
# Задаю фактоиды

total_vacancies = len(df)
salary_mean = int(((df['mean'].mean()/10).round()) * 10)
salary_min = int(((df['mean'].min()/10).round()) * 10)
salary_max = int(((df['mean'].max()/10).round()) * 10)
today_date = date.today().strftime("%d %B %Y")

# Фактоиды и значения
factoids = ['Total vacancies', 'Salary mean', 'Salary min', 'Salary max', 'Ланских Ярослав']
values = (
         [total_vacancies,
          str(salary_mean) + ' ' + rub_symbol,
          str(salary_min) + ' ' + rub_symbol,
          str(salary_max) + ' ' + rub_symbol,
          'Updated: '+ today_date
          ]
)

# Добавление текста к фактоидам с увеличенным шрифтом и выравниванием по центру

for i in range(4):
    axs[0][i].text(0.5,0.65, f"{factoids[i]}", ha='center', va='center',color='grey',fontsize=12)
    axs[0][i].text(0.5,0.45, f"{values[i]}", ha='center', va='center',color='black',fontsize=17)
    axs[0][i].axis('off')


# --------------------------------------------------------------------
# ФАКТОИДЫ КОНЕЦ



# ГРАФИК ПО НАПРАВЛЕНИЮ НАЧАЛО
# --------------------------------------------------------------------
# Объеденение ячейки строка 1, столбец 0+1
gs = axs[1, 0].get_gridspec()
axs[1,0].remove()
axs[1,1].remove()
axbig = fig.add_subplot(gs[1, 0:2])

sns.barplot(data=for_graph, x="mean", y="specialization", ax=axbig, order=order, errorbar=None, palette='flare')
axbig.bar_label(axbig.containers[0],label_type='center',color='w',fontsize=15) # Цифры на barplot
axbig.set_title("Средняя зарплата по направлению:",fontsize=15,pad = 25)  # Задание заголовка для первого графика
# axbig.set_xlabel("Зарплата", color='black', fontsize=14, labelpad=45)    # Меняю ось x
axbig.set_xlabel('')
# axbig.set_ylabel("Направление", color='black', fontsize=14, labelpad=30) # Меняю ось y
axbig.set_ylabel('')
axbig.tick_params(axis='x', colors='grey', labelsize=12, pad = 13)       # Меняю значения на оси x
axbig.tick_params(axis='y', colors='grey', labelsize=12, pad = 13)       # Меняю значения ни оси y
plt.setp(axbig.xaxis.get_majorticklabels(), rotation=30)


# Линия
axbig.axvline(df["mean"].mean(), color='r', linestyle='-') # Добавляю линию
# Добавляю надпись
total_mean = int(((df['mean'].mean() / 1000 ).round()) * 1000)
axbig.text(df["mean"].mean(), axbig.get_ylim()[0], f'Total mean: {total_mean} {rub_symbol}', color='black', va='bottom', ha='left',fontsize=12)#


# Объеденение ячейки строка 1, столбец 2+3
gs = axs[1, 1].get_gridspec()
axs[1,2].remove()
axs[1,3].remove()
axbig = fig.add_subplot(gs[1, 2:4])

sns.barplot(data=for_graph, x="url", y="specialization", ax=axbig, order=order, errorbar=None, palette='flare')
axbig.bar_label(axbig.containers[0],color='black',fontsize=15)
axbig.set_title("Кол-во вакансий по направлению:",fontsize=15,pad=25)  # Задание заголовка для второго графика
# axbig.set(xlabel='Количество вакансий', ylabel='')  # Задание названий осей для первого графика
axbig.set(xlabel='',ylabel='')
axbig.set_yticklabels([])  # Удаление подписей оси y для второго графика
# axbig.set_xlabel("Кол-во вакансий", color='black', fontsize=14,labelpad=45)
axbig.tick_params(axis='x', colors='grey', labelsize=12, pad = 15)

plt.setp(axbig.xaxis.get_majorticklabels(), rotation=30)

fig.suptitle('По направлению', fontsize=20,y=0.75)


# ГРАФИК ПО НАПРАВЛЕНИЮ КОНЕЦ
# --------------------------------------------------------------------



# ГРАФИК ПО ГОРОДУ НАЧАЛО
# --------------------------------------------------------------------
# Объеденение ячейки строка 2, столбец 0+1
gs = axs[2, 0].get_gridspec()
axs[2,0].remove()
axs[2,1].remove()
axbig = fig.add_subplot(gs[2, 0:2])

sns.barplot(data=area_graph.head(10), x="mean", y="area_name", ax=axbig, errorbar=None, palette='flare')
axbig.bar_label(axbig.containers[0],label_type='center',color='w',fontsize=15)
axbig.set_title("Средняя зарплата по городам:",fontsize=15,pad = 25)  # Задание заголовка для первого графика
# axbig.set_xlabel("Город", color='black', fontsize=14, labelpad=20)
axbig.set_xlabel('')
# axbig.set_ylabel("Зарплата", color='black', fontsize=14, labelpad=10)
axbig.set_ylabel('')
axbig.tick_params(axis='x', colors='grey', labelsize=12, pad = 15)
axbig.tick_params(axis='y', colors='grey', labelsize=12, pad = 15)

# Объеденение ячейки строка 2, столбец 2+3
gs = axs[2, 1].get_gridspec()
axs[2,2].remove()
axs[2,3].remove()
axbig = fig.add_subplot(gs[2, 2:4])

sns.barplot(data=area_graph.head(10), x="url", y="area_name", ax=axbig, errorbar=None, palette='flare')
axbig.bar_label(axbig.containers[0],color='black',fontsize=15)
axbig.set_title("Кол-во вакансий по городам:",fontsize=15,pad=25)  # Задание заголовка для второго графика
# axbig.set(xlabel='Количество вакансий', ylabel='')  # Задание названий осей для первого графика
axbig.set(xlabel='',ylabel='')
axbig.set_yticklabels([])  # Удаление подписей оси y для второго графика
# axbig.set_xlabel("Кол-во вакансий", color='black', fontsize=14,labelpad=30)
axbig.tick_params(axis='x', colors='grey', labelsize=12, pad = 15)


# ГРАФИК ПО ГОРОДУ КОНЕЦ
# --------------------------------------------------------------------



# ГРАФИК ПО ОПЫТУ НАЧАЛО
# --------------------------------------------------------------------
# Объеденение ячейки строка 3, столбец 0+1
gs = axs[3, 0].get_gridspec()
axs[3,0].remove()
axs[3,1].remove()
axbig = fig.add_subplot(gs[3, 0:2])

exp = '0'
mean = for_graph_exp.loc[for_graph_exp['experience'] == exp]['mean'].iloc[0]
count = for_graph_exp.loc[for_graph_exp['experience'] == exp]['url'].iloc[0]


sns.histplot(data=df.loc[df['experience'] == exp],x='mean',kde=True,ax=axbig)

axbig.set_title(f'Лет опыта: {exp}',fontsize=15,pad = 30)
axbig.set_ylabel('')
axbig.set_xlabel('Salary')

axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.95, f'Среднее: {mean} {rub_symbol}', color='black', fontsize=12, ha='right', va='top')
axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.85, f'Количество вакансий: {count}', color='black', fontsize=12, ha='right', va='top')

# Объеденение ячейки строка 3, столбец 2+3
gs = axs[3, 1].get_gridspec()
axs[3,2].remove()
axs[3,3].remove()
axbig = fig.add_subplot(gs[3, 2:4])


exp = '1-3'
mean = for_graph_exp.loc[for_graph_exp['experience'] == exp]['mean'].iloc[0]
count = for_graph_exp.loc[for_graph_exp['experience'] == exp]['url'].iloc[0]


sns.histplot(data=df.loc[df['experience'] == exp],x='mean',kde=True,ax=axbig)

axbig.set_title(f'Лет опыта: {exp}',fontsize=15,pad = 30)
axbig.set_ylabel('')
axbig.set_xlabel('Salary')

axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.95, f'Среднее: {mean} {rub_symbol}', color='black', fontsize=12, ha='right', va='top')
axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.85, f'Количество вакансий: {count}', color='black', fontsize=12, ha='right', va='top')

# Объеденение ячейки строка 4, столбец 0+1
gs = axs[4, 0].get_gridspec()
axs[4,0].remove()
axs[4,1].remove()
axbig = fig.add_subplot(gs[4, 0:2])


exp = '3-6'
mean = for_graph_exp.loc[for_graph_exp['experience'] == exp]['mean'].iloc[0]
count = for_graph_exp.loc[for_graph_exp['experience'] == exp]['url'].iloc[0]


sns.histplot(data=df.loc[df['experience'] == exp],x='mean',kde=True,ax=axbig)

axbig.set_title(f'Лет опыта: {exp}',fontsize=15,pad = 30)
axbig.set_ylabel('')
axbig.set_xlabel('Salary')

axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.95, f'Среднее: {mean} {rub_symbol}', color='black', fontsize=12, ha='right', va='top')
axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.85, f'Количество вакансий: {count}', color='black', fontsize=12, ha='right', va='top')

# Объеденение ячейки строка 4, столбец 2+3
gs = axs[4, 1].get_gridspec()
axs[4,2].remove()
axs[4,3].remove()
axbig = fig.add_subplot(gs[4, 2:4])


exp = '6+'
mean = for_graph_exp.loc[for_graph_exp['experience'] == exp]['mean'].iloc[0]
count = for_graph_exp.loc[for_graph_exp['experience'] == exp]['url'].iloc[0]


sns.histplot(data=df.loc[df['experience'] == exp],x='mean',kde=True,ax=axbig)

axbig.set_title(f'Лет опыта: {exp}',fontsize=15,pad = 30)
axbig.set_ylabel('')
axbig.set_xlabel('Salary')

axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.95, f'Среднее: {mean} {rub_symbol}', color='black', fontsize=12, ha='right', va='top')
axbig.text(axbig.get_xlim()[1]*0.95, axbig.get_ylim()[1]*0.85, f'Количество вакансий: {count}', color='black', fontsize=12, ha='right', va='top')


# ГРАФИК ПО ОПЫТУ КОНЕЦ
# --------------------------------------------------------------------




fig.set_facecolor('#f0f0f0') # Фон
plt.subplots_adjust(hspace=0.65) # вертикальное расстояние между графиками
fig.suptitle('Создал Ланских Ярослав',y=0.86,x=0.8,color='grey')

plt.savefig('boss.png')
print('Created graph')