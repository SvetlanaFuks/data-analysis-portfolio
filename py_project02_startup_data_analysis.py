#!/usr/bin/env python
# coding: utf-8

# # Проект. Исследование стартапов

# ## Введение

# Дата: 08.10.2025 <br>
# Автор: Светлана Фукс
# 
# ### Цель проекта
# Финансовая компания, работающая с венчурными инвестициями, хочет понять закономерности финансирования стартапов и оценить перспективы выхода на рынок с покупкой и развитием компаний.
# 
# #### Задачи проекта
# - Выделить группы компаний по срокам финансирования и сравнить их по количеству и объёму инвестиций.
# - Классифицировать сегменты рынка на массовые, средние и нишевые и учесть это в дальнейшем анализе.
# - Определить типичные и аномальные значения объёмов финансирования, исключить выбросы и ограничить период исследования.
# - Сравнить популярность и объёмы разных типов финансирования.
# - Проанализировать динамику раундов и объёмов инвестиций по годам, а также изменения в массовых сегментах рынка.
# - Рассчитать долю возврата средств для разных типов финансирования и оценить её устойчивость.
# 
# #### План работы
# - Ознакомление с данными
# - Предобработка: выявление пропусков и их обработка; приведения к общему формату (стандартизация регистров, удаление пробелов); приведение данных к нужному формату.
# - Иследовательский анализ данных и работа с выбросами
# - Анализ динамики
# - Итоги и Рекомендации
# 

# ## Шаг 1. Знакомство с данными: загрузка и предобработка
# 
# Датасет получен из базы данных стартапов.
# 
# Название основного датасета — `cb_investments.zip`. Внутри архива один файл — `cb_investments.csv`.
# 
# Описание данных:
# * `name` — название компании.
# * `homepage_url` — ссылка на сайт компании.
# * `category_list` — категории, в которых работает компания. Указываются через `|`.
# * `market` — основной рынок или отрасль компании.
# * `funding_total_usd` — общий объём привлечённых инвестиций в долларах США.
# * `status` — текущий статус компании, например `operating`, `closed` и так далее.
# * `country_code` — код страны, например USA.
# * `state_code` — код штата или региона, например, CA.
# * `region` — регион, например, SF Bay Area.
# * `city` — город, в котором расположена компания.
# * `funding_rounds` — общее число раундов финансирования.
# * `participants` — число участников в раундах финансирования.
# * `founded_at` — дата основания компании.
# * `founded_month` — месяц основания в формате `YYYY-MM`.
# * `founded_quarter` — квартал основания в формате `YYYY-QN`.
# * `founded_year` — год основания.
# * `first_funding_at` — дата первого финансирования.
# * `mid_funding_at` — дата среднего по времени раунда финансирования.
# * `last_funding_at` — дата последнего финансирования.
# * `seed` — сумма инвестиций на посевной стадии.
# * `venture` — сумма венчурных инвестиций.
# * `equity_crowdfunding` — сумма, привлечённая через долевой краудфандинг.
# * `undisclosed` — сумма финансирования нераскрытого типа.
# * `convertible_note` — сумма инвестиций через конвертируемые займы.
# * `debt_financing` — сумма долгового финансирования.
# * `angel` — сумма инвестиций от бизнес-ангелов.
# * `grant` — сумма полученных грантов.
# * `private_equity` — сумма инвестиций в виде прямых (частных) вложений.
# * `post_ipo_equity` — сумма финансирования после IPO.
# * `post_ipo_debt` — сумма долгового финансирования после IPO.
# * `secondary_market` — сумма сделок на вторичном рынке.
# * `product_crowdfunding` — сумма, привлечённая через продуктовый краудфандинг.
# * `round_A` — `round_H` — сумма инвестиций в соответствующем раунде.
# 
# Название дополнительного датасета — `cb_returns.csv`. Он содержит суммы возвратов по типам финансирования в миллионах долларов по годам.
# 
# Описание данных:
# * `year` — год возврата средств.
# * `seed` — сумма возвратов от посевных инвестиций.
# * `venture` — сумма возвратов от венчурных инвестиций.
# * `equity_crowdfunding` — сумма, возвращённая по долевому краудфандингу.
# * `undisclosed` — сумма возвратов нераскрытого типа.
# * `convertible_note` — сумма возвратов через конвертируемые займы.
# * `debt_financing` — сумма возвратов от долгового финансирования.
# * `angel` — сумма возвратов бизнес-ангелам.
# * `grant` — сумма возвратов по грантам.
# * `private_equity` — сумма возвратов прямых (частных) вложений.
# * `post_ipo_equity` — сумма возвратов от IPO.
# * `post_ipo_debt` — сумма возвратов от долгового IPO.
# * `secondary_market` — сумма возвратов от сделок на вторичном рынке.
# * `product_crowdfunding` — сумма возвратов по продуктовому краудфандингу.
# 
# ### 1.1. Вывод общей информации

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[2]:


df_invest = pd.read_csv("https://code.s3.yandex.net/datasets/cb_investments.zip", sep=';', low_memory=False)


# In[3]:


def explore(df):
    '''
    функция выводит резюме датафрейма
    '''
    print("Первые 5 строк:")
    display(df.head())

    print("Общая информация:")
    df.info()

    print("Доля пропусков по столбцам (%):")
    na_ratio = round(df.isna().mean() * 100, 2).sort_values(ascending=False)
    display(na_ratio)
    
    print("Количество явных дубликатов: ")
    print(df.duplicated().sum())

    return na_ratio 


# In[4]:


explore(df_invest)


# In[5]:


df_invest_na_ratio= round(df_invest.isna().mean() * 100, 2).sort_values(ascending=False)#относительное кол-во пропусков
print(df_invest_na_ratio)


# Датасет содержит 40 столбцов и 54294 строки. Данные двух типов float64(24 столбца), object(16 столбцов). <br>
# Замеченные проблемы: 
# - названия столбцов содержат пробелы
# - в данных есть пробелы (Nan). ольше всего пропусков в столбцах paticipants (43%), mid_funding_at (44%)
# - неверные форматы: funding_total_usd (object->float/int);founded_at;last_funding_at;founded_month;founded_quarter;first_funding_date;mid_funding_date(object->date);
# - Пропуски mid_funding_at, founded_at, founded_month,founded_quarter,founded_year  в  можно отнести к категории MAR. 
# - Пропуски в столбцах last_funding_at, first_funding_at,name,funding_total_usd (+ все колонки сотавляющие итогую сумму финансирования) относятся к MNAR
# 
# Гипотеза по пропускам: "Скорее всего ввиду того, что данные исторические и наверно собирались в разные отрезки времени,какие-то данные просто не публиковались или отсутствовали вовсе на момент публикации." 
# 

# In[6]:


df_returns= pd.read_csv('https://code.s3.yandex.net/datasets/cb_returns.csv',index_col='year')


# In[7]:


explore(df_returns)


# In[8]:


start_df_invest = df_invest.shape[0]


# In[9]:


start_df_returns = df_returns.shape[0]


# Датасет содержит 14 столбцов и 15 строк. Данные двух типов float64(13 столбца), int64(1 столбeц).
# Никаких проблем с форматом не замечено.

# При знакомстве с датасетами, мы видим что df_invest содержит пропущенные значения, а также неверные форматы. df_returns не содержит пропущенных строк и проблем с форматом не выявлено. Количество данных в датасете не совпадает,и пока не понятно является ли df_returns агрегированной базой, и если да, по чему (какому признаку) ее агрегировали. 

# ### 1.2. Предобработка данных

# In[10]:


df_invest.columns= df_invest.columns.str.lower().str.strip() #стандартизируем название столбцов


# In[11]:


df_invest['funding_total_usd'] = df_invest['funding_total_usd'].str.replace(',', '')#убираем разряды
df_invest['funding_total_usd'] = pd.to_numeric(df_invest['funding_total_usd'],errors='coerce') #меняем формат


# In[12]:


df_invest[['founded_at','last_funding_at','first_funding_at','mid_funding_at']]= (df_invest[['founded_at','last_funding_at',
                                                                                             'first_funding_at','mid_funding_at']]
                                                                                 .apply(pd.to_datetime,errors='coerce'))#привели в формат даты

df_invest[['founded_month','founded_quarter']]= (df_invest[['founded_month','founded_quarter']]
                                                .apply(pd.to_numeric, errors='coerce'))#привели в формат числа


# In[13]:


df_invest[['founded_month']]=(df_invest['founded_month']
                              .fillna(df_invest['founded_at'].dt.month))#заполняем пробелы

df_invest[['founded_quarter']]=(df_invest['founded_month']
                              .fillna(df_invest['founded_at'].dt.quarter))#заполняем пробелы


# In[14]:


df_invest = df_invest.apply(
    lambda col: col.fillna('NaN') if col.dtype == 'object' else col
)  # ставим заглушки в колонки с текстом


# In[15]:


df_invest.apply(
    lambda col: print(f"\n{col.name}: {col.unique()} ({col.nunique()})")
    if col.dtype == 'object' else None
)#проверяем уникальные значения в текстовых колонках


# In[16]:


df_invest = df_invest.apply(
    lambda col: col.str.lower()
                   .str.strip()
                   .str.replace(r'(&|\+)', 'and', regex=True)
    if col.dtype == 'object' else col
)#стандартизируем и очищаем колонки с текстом


# In[17]:


df_invest['funding_total_usd'] = df_invest.loc[:, 'seed':].sum(axis=1) #заполняем пустые ячейки


# Так как 'funding_total_usd' является суммой колонок от seed до round_h мы просуммируем все результаты

# In[18]:


df_invest = df_invest[df_invest['funding_total_usd'] != 0] #удаляем ячейки с нулевым значением


# Удаляем строки, которые не содержат данных, то есть равны нулю.Эти данные полезной информации для инвесторов не носят

# In[19]:


cols_to_check = ['name', 'funding_total_usd'] + list(df_invest.loc[:, 'seed':].columns)#лист для фильтра
mask_dups = df_invest.duplicated(subset=cols_to_check, keep=False)#ищем явные дубликаты по фильтру
duplicates_view = df_invest.loc[mask_dups, cols_to_check]#создаем таблицу чтобы сравнить строки
display(duplicates_view)


# In[20]:


df_invest = df_invest.drop_duplicates(subset=cols_to_check).reset_index(drop=True)#удаляем дубликаты


# Названия в столбце 'name', 'funding_total_usd' и столбец формирующий 'funding_total_usd' полностью совпадают Итак, мы обнаружили 6 явных дубликатов, которые нужно удалить, чтобы не искажать результаты последующего анализа.

# In[21]:


df_invest['mid_funding_at'] = df_invest['first_funding_at'] + (
    (df_invest['last_funding_at'] - df_invest['first_funding_at']) / 2
)#заполняем столбец mid_funding_at


# In[22]:


df_invest_new_ratio= round((df_invest.isna().sum()/len(df_invest))*100,2)
print(df_invest_new_ratio)#проверим финальный датафрем на количество данных 


# In[23]:


new_def_invest = df_invest.shape[0]
difference = new_def_invest/start_df_invest
print(difference)#находим относительную разницу в размере исходного и финального датафрейма


# <b>Итоги предобработки:</b>
# 
# По итогу предобработки мы сохранили 75% датафрейма (40901 строка).Были исключены строки не содержащие данные по сумме инвестиций и явные дубликаты (всего 6 строк), так как они не несли ценности для дальнейшего анализа. Тем самым мы отсекли пропуски во всех столбцах от seed до round_h <br>
# Тем самым количество пропусков в колонке founded_month и founded_quarter сократилось с 29% до 21% (8% данных восстановлено); <br>
# В столбцах содержащий текст мы пустые строки заменили заглушками, поэтому пропуски равны 0. Отсекать мы эти данные пока не будем, возможно он пригодятся для дальнейшего аанализа.

# ## Шаг 2. Инжиниринг признаков

# ### 2.1. Группы по срокам финансирования
# 
# Разделите все компании на три группы:
# 
# * Единичное финансирование — был всего один раунд финансирования.
# 
# * Срок финансирования до года — между первым и последним раундом финансирования прошло не более года.
# 
# * Срок финансирования более года.
# 
# Визуализируйте соотношение этих групп, создав два графика:
# 
# * По количеству компаний: Покажите, какой процент от общего числа компаний относится к каждой из трёх групп.
# * По объёму инвестиций: Отобразите, какую долю от общего объёма привлечённых средств получила каждая группа.
# 

# In[24]:


def define_funding_type(df):
    """
    Присваивает каждой компании категорию по длительности и количеству раундов.
    Возвращает Series с текстовыми категориями.
    """
    group_types = []
    
    # вычисляем разницу в днях
    difference_time = (df['last_funding_at'] - df['first_funding_at']).dt.days

    for fun_round, days in zip(df['funding_rounds'], difference_time):
        if fun_round == 1:
            group_types.append('единичное финансирование')
        elif days <= 365:
            group_types.append('финансирование до года')
        elif days > 365:
            group_types.append('финансирование больше года')
        else:    
            return pd.Series(group_types)

# применение:
df_invest['group_funding'] = define_funding_type(df_invest)


# In[25]:


grouped_types = df_invest.groupby('group_funding',as_index=False).agg({'name': 'count',
                                                        'funding_total_usd': 'sum'})

grouped_types['name']=                      round(grouped_types['name']/grouped_types['name'].sum(),2)*100#относительное значение кол-ва компаний
grouped_types['funding_total_usd']= (round(grouped_types['funding_total_usd']/grouped_types['funding_total_usd']
                                           .sum(),2))*100#относительное значение финансирования
print(grouped_types)


# In[26]:


plt.figure(figsize =(12,8))

sns.barplot (data=grouped_types,
             x='group_funding',
             y='name',
             palette= 'viridis'
)
plt.title('Количество компаний по группам финансирования', size=20)
plt.xlabel ('Группа финансирования', size =15)
plt.ylabel('Количество компаний (%)',size =15)
plt.show()


# По графику видно, что чаще всего компании получают единичное финансирование (68%). 25% компаний получают финансирование с отрывом больше года от первого финансирования. Только 7% компаний получают повторное финансирование в рамках 1 года. 

# In[27]:


plt.figure(figsize =(12,8))

sns.barplot (data=grouped_types,
             x='group_funding',
             y='funding_total_usd',
             palette= 'viridis'
)
plt.title('Распределенние общей суммы привлеченных средств по группам', size= 20)
plt.xlabel ('Группа финансирования', size=15)
plt.ylabel('Объем средств(%)',size=15)
plt.show()


# Больше всего средств от общей скммы привлеченного финансирование приходится на компании, получившие повторные средства в разрезе больше года от первого финансирования (51%), 48% приходится на компании получившие финансирование всего лишь раз и 6% приходится на компании, которые получили повторное финансирование в течение года от первого финансирования.

# <b>Промежуточный итог:</b>
# 
# Вероятнее всего, что стартап получит финансирование всего один раз
# Повторное финанансирование приходится ждать дольше чем 1 год, и суммы там бывают больше чем при первом финансировании. Что возможно является сигналом, что инвесторы видят прогресс в работе стартапа и вливают больше денег.
# Малое количество компаний получает 2 финансирования в течении года, в таких случаях и суммы не высокие. Это может быть сигналом что деятельность стартапов "хайповая", но "с высоким риском" соотвественно инвестируют осторожно.

# ### 2.2 Выделение средних и нишевых сегментов рынка

# In[28]:


def segment_finder(df):
    
    """
    Функция рассчитывает, сколько компаний приходится на каждый сегмент рынка,
    и классифицирует сегменты как массовые, средние или нишевые.
    """

    market_counts = df['market'].value_counts()# сколько компаний в каждом сегменте рынка

    def classify(market):
        count = market_counts.get(market, 0)  # классифицируем каждый сегмент
        if count > 120:
            return 'массовые'
        elif count >= 35:
            return 'средние'
        else:
            return 'нишевые'

    return df['market'].apply(classify)


# In[29]:


df_invest['segment']=segment_finder(df_invest)


# In[30]:


display(df_invest.head())


# In[31]:


segment_group = (
      df_invest['segment']
      .value_counts()
      .rename_axis('segment')
      .reset_index(name='n_markets')
)#сколько сегментов попадает в каждую из категорий
print(segment_group)


# Больше всего компаний попадают в массовый сегмент (36 230), в среднем сегменте 3839 компаний, и только 830 в нишевом.

# In[32]:


graph_data= df_invest.groupby(['market','segment'])['name'].count().reset_index()
graph_data = graph_data.rename(columns={'name':'num_company'})
graph_data = graph_data.loc[(graph_data['segment']=='нишевые')| (graph_data['segment']=='средние')]
print(graph_data.head())


# In[33]:


plt.figure(figsize=(12, 8))

for i in graph_data['segment'].unique():
    subset = graph_data.loc[graph_data['segment'] == i, 'num_company']
    plt.hist(subset, bins=15, alpha=0.5, label=f'{i.capitalize()}')

plt.title('Распределение количества компаний по типам сегментов')
plt.xlabel('Количество компаний в сегменте')
plt.ylabel('Плотность')
plt.legend(title='Тип сегмента')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Большинство сегментов рынка — нишевые, они содержат мало компаний (часто менее 20).Средние сегменты встречаются реже, но охватывают значительно больше участников.

# In[34]:


df_invest['market'] = np.where(
    df_invest['segment'] == 'средние', 'mid',
    np.where(df_invest['segment'] == 'нишевые', 'niche', df_invest['market'])
) #оставляем только массовые, на остальные ставим заглушки
display(df_invest.head())


# ## Шаг 3. Работа с выбросами и анализ

# ### 3.1. Анализируем и помечаем выбросы в каждом из сегментов
# 
# Заказчика интересует обычный для рассматриваемого периода размер средств, который предоставлялся компаниям.
# 
# По предобработанному столбцу `funding_total_usd` графическим образом оцените, какой размер общего финансирования для одной компании будет типичным, а какой — выбивающимся. Укажите интервал, в котором лежат типичные значения.

# In[35]:


df_invest['funding_total_usd'].describe() #проверим сначала описательную статистику


# Среднее значение равно 22 279 890 долларов, при том что медиана равнв 2 250 000, что значит ассимитричное распределение данных. Стандартное отклонение тоже высокое 176 миллионов, указывает на высокую дисперсию. Построим боксплот чтобы проверить первичные выводы.

# In[36]:


plt.figure(figsize=(12, 6))
plt.boxplot(np.log10(df_invest['funding_total_usd']), vert=False)
plt.title('Распределение общего финансирования (логарифм по 10)')
plt.xlabel('log10(Funding total USD)')
plt.show()


# Типичной суммой общего финансирования (50%) это 1000 000 долларов на компанию. Редкие компании получают 1 млрд долларов. 

# In[37]:


df_niche = df_invest.loc[df_invest['segment'] == 'нишевые', :]
display(df_niche.tail())


# In[38]:


Q1_n= df_niche['funding_total_usd'].quantile(0.25)
Q3_n =df_niche['funding_total_usd'].quantile (0.75)
IQR_n= Q3_n-Q1_n


# In[39]:


upper_bound_n= Q3_n+1.5*IQR_n
lower_bound_n= Q1_n-1.5*IQR_n

print(f'Верхний порог выбросов для компаний в нишевых сегментов: {upper_bound_n}, нижний порог: {lower_bound_n}' )


# Для компаний в нишевых сегментах характерен диапазон общего финансирования от 0 до примерно 17,27 млн USD. Значения выше этой границы можно рассматривать как выбросы

# In[40]:


anomaly_niche = (
    df_niche.groupby('name', as_index=False)['funding_total_usd']
    .sum()
    .query('funding_total_usd > 0 and funding_total_usd > 17275000').sort_values('funding_total_usd',ascending=False)
)

anomaly_size = round((len(anomaly_niche) / len(df_niche))*100,2)

print(anomaly_niche.head(5))
print(f'Доля компаний с аномально большим размером инвестиций: {anomaly_size}')


# Более 809 компаний получили аномально большое финансирование, что составляет 17% процентов всего сегмента.

# In[41]:


df_mid =df_invest.loc[(df_invest['segment']=='средние'),:]
display(df_mid.head())


# In[42]:


Q1_m= df_mid['funding_total_usd'].quantile(0.25)
Q3_m =df_mid['funding_total_usd'].quantile (0.75)
IQR_m= Q3_m-Q1_m


# In[43]:


upper_bound_m= Q3_m+1.5*IQR_m
lower_bound_m= Q1_m-1.5*IQR_m

print(f'Верхний порог выбросов для компаний в средних сегментах: {upper_bound_m}, нижний порог: {lower_bound_m}' )


# In[44]:


anomaly_mid = (
    df_mid.groupby('name', as_index=False)['funding_total_usd']
    .sum()
    .query("funding_total_usd > 0 and funding_total_usd > 29625000").sort_values('funding_total_usd',ascending=False)
)

anomaly_size_m = round((len(anomaly_mid) / len(df_mid))*100,2)

print(anomaly_mid.head(5))
print(f'Доля компаний с аномально большим размером инвестиций: {anomaly_size_m}')


# Более 555 компаний получили аномально большое финансирование, что составляет 14% процентов всего сегмента.

# <b> Заключение </b>
#     
# В нишевом сегмете больше компаний получили аномально высокое общее финансирования, чем в среднем сегменте. Скорее всего и обоих сегментах данные компании можно отнести к unicorn-ам.

# ### 3.2 Определяем границы рассматриваемого периода, отбрасываем аномалии
# 

# In[45]:


df_2024= df_invest.loc[df_invest['founded_year']==2014,:]  #создаем срез


# In[46]:


print(df_2024['founded_month'].unique()) #проверяем номера месяцев


# In[47]:


df_2024.info()# посмотрим есть ли пропуски в важных для анализа столбцах


# В 2014 году у нас 1014 записей, пропуски в participants. Столбец founded_month  содердит все месяца от 1 до 12. Данные можно считать полными.

# In[48]:


filter_list =list(anomaly_mid['name']+anomaly_niche['name']) #создаем единый лист аномальных компаний
clean_df_invest = df_invest.loc[~df_invest['name'].isin(filter_list)]# отфильтровываем их из датасета


# In[49]:


rounds_per_year = (clean_df_invest
                   .groupby(clean_df_invest ['mid_funding_at'].dt.year)['funding_rounds']
                   .sum())#рассчитываем сумму раудов по дате


target_dates = rounds_per_year[rounds_per_year >= 50].index # отфильтровываем все что больше 50


# In[50]:


filtered_df_invest = clean_df_invest.loc [~clean_df_invest['mid_funding_at'].isin(target_dates)]
print(filtered_df_invest.shape[0])


# ### 3.3. Анализ типов финансирования по объёму и популярности
# 
# Постройте график, который покажет, какие типы финансирования в сумме привлекли больше всего денег. Ориентируйтесь на значения в столбцах `seed`, `venture`, `equity_crowdfunding`, `undisclosed`, `convertible_note`, `debt_financing`, `angel`, `grant`, `private_equity`, `post_ipo_equity`, `post_ipo_debt`, `secondary_market` и `product_crowdfunding`.
# 
# Также постройте график, который покажет популярность разных типов финансирования — какие типы финансирования чаще всего используются компаниями, то есть встречаются в датасете наибольшее количество раз.
# 
# Сравните графики и выделите часто используемые типы финансирования, которые при этом характеризуются небольшими объёмами, и наоборот — те, что встречаются редко, но при этом характеризуются значительным объёмом предоставленных сумм.

# In[51]:


cols = [
    'seed','venture','equity_crowdfunding','undisclosed','convertible_note',
    'debt_financing','angel','grant','private_equity','post_ipo_equity',
    'post_ipo_debt','secondary_market','product_crowdfunding'
]

totals= df_invest[cols].sum().sort_values(ascending=False)

plt.figure (figsize=(12,10))
ax = totals.plot(kind='bar')
ax.set_title('Суммарно привлечённые средства по типам финансирования')
ax.set_xlabel('Тип финансирования')
ax.set_ylabel('Сумма, млрд $')
plt.tight_layout()
plt.show()


# In[52]:


print(totals)


# In[53]:


cols = [
    'seed','venture','equity_crowdfunding','undisclosed','convertible_note',
    'debt_financing','angel','grant','private_equity','post_ipo_equity',
    'post_ipo_debt','secondary_market','product_crowdfunding'
]

totals_p= (df_invest[cols]!= 0).sum().sort_values(ascending=False)#!= создает таблицу False/TRue

plt.figure (figsize=(12,10))
ax = totals_p.plot(kind='bar')
ax.set_title('Популярность по типам финансирования')
ax.set_xlabel('Тип финансирования')
ax.set_ylabel('Количество')
plt.tight_layout()
plt.show()


# In[54]:


print(totals_p)


# Venture как тип финансирования привлекли больше всего средств (около 371 млрд долларов), далее private equity (102 млрд), меньше всего привлек product crowdfunding (350 млн).Venture самый популярный тип финансирования (более 20000), далее идет seed (~15000),самый не популярный secondary market.
# 
# <b>Итог</b> <br>
# Несмотря на что seed является вторым по популярности типом финансирования, объем финансирования от него не большой.Debt financing по популярности и объему финансирования на третьем месте.Private equity на втором месте по объему финансирования, но не является популярным типом, что можно объяснить тем, что данный тип финансирования подходит более зрелым компаниям, а таких среди стартапов не много и суммы бывают весомые. Angel популярный тип финансирования, но суммы маленькие, потому что обычно такие средства выделяются стартам на очень ранней стадии, когда не известно схлопнется он или нет. 

# In[55]:


cols = [
    'seed','venture','equity_crowdfunding','undisclosed','convertible_note',
    'debt_financing','angel','grant','private_equity','post_ipo_equity',
    'post_ipo_debt','secondary_market','product_crowdfunding'
]

totals_r= (df_returns[cols]).sum().sort_values(ascending=False)

plt.figure (figsize=(12,10))
ax = totals_r.plot(kind='bar')
ax.set_title('Возвраты с разных типов финансирования')
ax.set_xlabel('Тип финансирования')
ax.set_ylabel('Сумма возврата, млн$')
plt.tight_layout()
plt.show()


# In[56]:


print(totals_r)


# Venture абсолютный лидер по объему возвратов (40+ млрд $). Эти типично, так как венчурные сделки имеют высокий риск, но и огромный потенциал доходности. Debt financing и private equity имеют стабильный возраст, хотьь и меньше чем венчурные. Seed и Angel (2.3-1.5 млрд) для стартапов на ранней стадии не плохо. Успешные стартапы могут компенсировать множество неудачных.

# ## Шаг 4. Анализ динамики

# ### 4.1 Динамика предоставления финансирования по годам
# 
# Используя столбцы `funding_total_usd` и `funding_rounds`, рассчитайте для каждой компании средний объём одного раунда финансирования.
# 
# На основе получившейся таблицы постройте графики, отражающие:
# * динамику типичного размера средств, которые стартапы получали в рамках одного раунда финансирования;
# 
# * динамику общего количества раундов за каждый год, то есть насколько активно происходили инвестиции на рынке (чем больше раундов, тем выше активность).
# 
# На основе полученных данных ответьте на вопросы:
# * В каком году типичный размер средств, собранных в рамках одного раунда, был максимальным?
# 
# * Какая тенденция наблюдалась в 2014 году по количеству раундов и средств, выделяемых в рамках каждого раунда?

# In[57]:


filtered_df_invest['fund_year']=filtered_df_invest['mid_funding_at'].dt.year

fund_avg_company = (
    filtered_df_invest
    .groupby(['name', 'fund_year'], as_index=False)
    .agg({
        'funding_total_usd': 'sum',
        'funding_rounds': 'sum'
    })
    .assign(
        avg_fund_per_round=lambda x: x['funding_total_usd'] / x['funding_rounds']
    )
)


# In[58]:


by_year = (fund_avg_company
           .groupby('fund_year')['avg_fund_per_round']
           .median()
           .sort_index()) #считаем медиану для определения типичного размера

by_year= by_year[by_year.index >= 1995]

by_year=by_year / 1e6 #переведём в млн $

plt.figure(figsize=(10,6))
plt.plot(by_year.index, by_year.values, marker='o', linewidth=1.5, label='Среднее по году')
plt.title('Динамика среднего размера раунда финансирования', fontsize=14)
plt.xlabel('Год')
plt.ylabel('Средний размер раунда, млн $')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()


# In[59]:


round_num= fund_avg_company.groupby('fund_year')['funding_rounds'].sum().reset_index()


# In[60]:


filtered_year = round_num[round_num['fund_year'] >= 2000]

plt.figure (figsize=(12,10))
filtered_year.plot(
    x='fund_year',
    y='funding_rounds',
    kind='line',
    marker='o',
    linewidth=1.5,
    title='Динамика общего количества раундов финансирования',
    grid=False
)
plt.xlabel('Год')
plt.ylabel('Общее количество раундов')
plt.show()


# Начиная с 1995 года типичные суммы инвестиции на раунд растут, пик приходится на 2004 год, равный 10 млн. После 2004 года сумма инвестиции на раунд падает вплоть до 2014 года. Данное явления можно описать, появлением большего количество стартапов, теперь инвесторы могли инвестировать разные суммы в большое количество стартапов в зависимости от их риска. Также возможно появились новые каналы инвестирования, что повлияло на диверсификацию инвестиционного портфеля.Стартапы перестали быть единственным видом инвестирования. 
# 
# Начиная с 2012 года количество инвестиционных раундов также сокращалось. Меньшее количество приходится на 2014 год. Однако сумма инвестирования 2014 года выше чем в 2013 году, что говорит о том, что типичная сумма за раунд в 2014 году увеличилась по сравнению с предыдущем годом.

# ### 4.2 Динамика размера общего финансирования по массовым сегментам рынка для растущих в 2014 году сегментов
# 
# Составьте сводную таблицу, в которой указывается суммарный размер общего финансирования `funding_total_usd` по годам и сегментам рынка. Отберите из неё только те сегменты, которые показывали рост размера суммарного финансирования в 2014 году по сравнению с 2013.
# 
# На графике отразите, как менялся суммарный размер общего финансирования в каждом из отобранных сегментов по годам, за которые у вас достаточно данных. Рассматривайте только массовые сегменты, а средние и нишевые исключите.
# 
# На основе графика сделайте вывод о том, какие сегменты показывают наиболее быстрый и уверенный рост.

# In[61]:


pivot_df=filtered_df_invest[filtered_df_invest['segment']=='массовые']


# In[62]:


pivot_table=pd.pivot_table (pivot_df,
                            values='funding_total_usd',
                            columns=['fund_year'],
                            index='market',
                            aggfunc={'funding_total_usd':'sum'},
                            fill_value=0
                )
filtered_pt = pivot_table.loc[:, (pivot_table.columns > 2005)]
filtered_pt=  filtered_pt[filtered_pt[2014] > filtered_pt[2013]]
display(filtered_pt)


# In[63]:


plt.figure(figsize=(12, 7))


top_markets = filtered_pt.sum(axis=1).sort_values(ascending=False).head(10).index # топ 10 сегментов
filtered_pt_top = filtered_pt.loc[top_markets]
filtered_pt_top.T.plot(kind='line', figsize=(12,7))

plt.title('Динамика суммарного финансирования по сегментам', fontsize=14)
plt.xlabel('Год')
plt.ylabel('Сумма финансирования, $')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
    


# Я оставила топ-10 сегментов, потому что сегментов было много и график плохо читался. Лидер по росту сегмент, который нам к сржалению не известен ("nan'), на втором месте с уверенным ростом сегмент финансов, далее технологии, несмотря на то , что с 2009 суммарное финансирование в этом сегменте снижается, он все равно в тройке лидеров.Производство напротив с 2009 года ушло в плато до 2012 и только с 2013 немного упало, но опятьь- таки в четверке лидеров. 

# ### 4.3 Годовая динамика доли возвращённых средств по типам финансирования

# Заказчик хочет знать, какая часть вложенных или выданных денег со временем возвращается обратно инвесторам или финансистам. Ваша цель — для каждого года и каждого вида финансирования рассчитать нормированные значения возврата средств: то есть какую долю возвращённые средства составляют от предоставленных. При этом слишком большие аномальные значения, то есть неадекватные выбросы, нужно заменить на пропуски.
# 

# In[64]:


clean_df_invest['year'] = clean_df_invest['mid_funding_at'].dt.year

group_list = [
    'seed','venture','equity_crowdfunding','undisclosed','convertible_note',
    'debt_financing','angel','grant','private_equity','post_ipo_equity',
    'post_ipo_debt','secondary_market','product_crowdfunding'
]

new_funding_df = (clean_df_invest
                  .groupby('year')[group_list]
                  .sum()
                  .sort_index())

display(new_funding_df)


# In[65]:


df_returns  = df_returns * 1e6 #переводим в миллионы


# In[66]:


joined_df = new_funding_df.join(
    df_returns,
    how='inner',
    lsuffix='_fund',   # суммы привлечения
    rsuffix='_ret'     # суммы возвратов (или др. метрика)
)


# In[67]:


fund_types = [c.replace('_fund', '') for c in joined_df.columns if c.endswith('_fund')]

ratios = np.round(
    (joined_df.filter(like='_ret').values / (joined_df.filter(like='_fund').values + 1e-60)) * 100,
    2
)

ratio_df = pd.DataFrame(ratios, columns=fund_types, index=joined_df.index)

print(ratio_df)


# In[68]:


cols_to_plot= ['venture','debt_financing','private_equity','seed','angel']

ratio_df[cols_to_plot].plot(figsize=(10, 6))
plt.title("Сравнение возратов по типу финансирования")
plt.ylabel("Return-to-Fund Ratio (%)")
plt.xlabel("Год")
plt.legend(title="Фонды")
plt.grid(True)
plt.show()


# На графике нет ни одного типа финансирования, который бы показывал устойчивый рост. Максимум, можно говорить о стабилизации и низкой волатильности у некоторых категорий (venture, debt financing).

# 
# ## Шаг 5. Итоговый вывод и рекомендации

# #### Основные выводы:</br>
# 
# - 68% стартапов получают единичное финансирование, что отражает высокий риск и слабую выживаемость.
# - 25% компаний проходят раунды длительностью >1 года, что связано с устойчивым развитием.
# - Средняя сумма инвестиций  около 2,25 млн $, медианная 1 млн $.
# - Венчурное финансирование — ключевой драйвер роста рынка, особенно в массовых сегментах (финансы, технологии).
# - В 2014 году рынок инвестиций начал сокращать количество раундов, но рост среднего чека на раунд увеличился — инвесторы стали избирательнее и осторожнее.
# - Доля возврата средств по основным типам (venture, debt, equity) показывает стабильность и предсказуемость, что привлекательно для инвесторов.
# 
# #### Итоговый отчёт (2015 год)</br>
# 
# Анализ данных о стартапах показал, что основное развитие и интерес инвесторов сосредоточены в двух направлениях — финансы и технологии. Эти отрасли показывают стабильный рост суммарного финансирования и высокий интерес со стороны венчурных фондов. Именно сюда стоит направлять инвестиции в 2015 году.</br>
# 
# Наиболее подходящий тип финансирования — венчурное. Оно остаётся самым крупным по объёму вложенных средств и по возвратам. Да, венчурные инвестиции связаны с рисками, но они обеспечивают максимальный потенциал прибыли. Второй по значимости тип — private equity, он подходит для более зрелых компаний, где риск меньше, но и доходность скромнее.</br>
# 
# Большинство стартапов получают финансирование только один раз. Те, кто привлекает деньги повторно, делают это обычно через год или дольше — значит, инвесторы готовы вкладываться снова только после того, как видят реальные результаты.</br>
# 
# Средний размер инвестиций на один раунд — около двух миллионов долларов, но медианное значение ближе к одному миллиону, что говорит о большом разбросе и о том, что отдельные сделки бывают очень крупными.</br>
# 
# К 2014 году стало меньше инвестиционных раундов, зато увеличился средний чек. Это значит, что рынок зрел, инвесторы стали осторожнее и выбирают более перспективные проекты.</br>
# 
# Возвратность вложений по венчурным, долговым и прямым инвестициям остаётся стабильной. Это делает их наиболее надёжными формами вложений в стартапы.</br>
# 
# #### Шаги, выполненные в исследовании:</br>
# 
# - Предобработка данных — очистка, коррекция форматов, удаление дубликатов и пропусков. Сохранено 75% исходного датасета (~41 тыс. строк).
# - Формирование признаков : группировка по длительности финансирования и выделение рыночных сегментов.
# - Удаление выбросов:  устранены компании с аномально высоким общим финансированием (≈15% выборки).
# - Анализ типов финансирования, оценка объемов и популярности различных форм инвестиций.
# - Динамический анализ (по годам): исследована активность рынка, рост финансирования и возвратность.
# - Построение рекомендаций по отраслям и видам инвестирования.
# 
# #### Рекомендация:</br>
# 
# В 2015 году стоит инвестировать в финансовые и технологические стартапы, используя венчурное финансирование как основной инструмент. Это сочетание показывает оптимальный баланс между риском и прибылью.
