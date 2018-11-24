import requests
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
import random
import statistics
import matplotlib.pyplot as plt
import networkx as nx


config = {
    'VK_ACCESS_TOKEN': 'Tокен доступа для ВК',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 100
    jitter = 0.1
    for i in range(max_retries):
        try:
            error = requests.get(url, params=params, timeout=timeout)
            return error
        except requests.exceptions.ConnectTimeout as err:
            error = f'ConnectTimeout: {err}'
        except requests.exceptions.ReadTimeout as err:
            error = f'ReadTimeout: {err}'
        except requests.exceptions.ConnectionError as err:
            error = f'ConnectionError: {err}'
        except requests.exceptions.HTTPError as err:
            error = f'HTTPError: {err}'
        except Exception as err:
            error = err
        time.sleep(delay*0.001)
        delay = delay*(1+backoff_factor)
        delay = delay + random.normalvariate(delay, jitter)
    return error


def get_friends(user_id, fields='bdate'):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    url = "https://api.vk.com/method/friends.get"
    access_token = config['VK_ACCESS_TOKEN']
    params = {
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'v': '5.92'
    }
    items = get(url, params=params).json()['response']['items']
    return items



def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id)
    dates = [i['bdate'] for i in friends if ('bdate' in i.keys())]
    items = [int(i.split('.')[-1]) for i in [j for j in dates if j.count('.')>1]]
    year = datetime.now().year
    age = year - statistics.median(items)
    return age


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    url = "https://api.vk.com/method/messages.getHistory"
    access_token = config['VK_ACCESS_TOKEN']
    cycles = (count//200*200+200)//200
    items = []
    params = {
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': 200,
        'v': '5.92'
    }
    for i in range(cycles):
        try:
            response = get(url, params=params).json()['response']['items']
            if response:
                items += response
            else:
                break
            offset += 200
            params['offset'] = offset
            time.sleep(0.4)
        except:
            break
    return items[:count]

def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    dates = [datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d") for message in messages]
    uniq_dates = [i for i in set(dates)]
    uniq_dates.sort()
    counts = [dates.count(i) for i in uniq_dates]
    return {'dates':uniq_dates, 'counts':counts}


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    plotly.tools.set_credentials_file(username=config['PLOTLY_USERNAME'], api_key=config['PLOTLY_API_KEY'])
    data = [go.Scatter(x=freq_list['dates'],y=freq_list['counts'])]
    py.iplot(data)


def get_network(users_ids, as_edgelist=True):
    if as_edgelist:
        edges = set()
        for user in users_ids:
            friends = get_friends(user)
            ids = [i['id'] for i in friends]
            for i in ids:
                if i in users_ids:
                    sorted_edge = sorted([user,i])
                    edges.add(tuple(sorted_edge))
        edges = list(edges)
        return edges
    elif not as_edgelist:
        edges = []
        for user in users_ids:
            friends = get_friends(user)
            ids = [i['id'] for i in friends]
            row = [1 if i in ids else 0 for i in users_ids]
            edges.append(row)
        return edges

def plot_graph(graph):
    G = nx.Graph() # создание объекта графа
    G.add_edges_from(graph) # добавление групп в граф
    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == "__main__":
    # Проверка функции get()
    print(get("https://httpbin.org/get"))
    print(get("https://httpbin.org/delay/2", timeout=1))
    print(get("https://httpbin.org/status/500"))
    print(get("https://noname.com", timeout=1))
    # Проверка функции age_predict()
    print('Predicted age: ', age_predict(400008940))
    # Построение и отрисовка графика частоты сообщений
    messages = messages_get_history(400008940, count=1000000)
    print('Count messages: ',len(messages))
    freq_list = count_dates_from_messages(messages)
    plotly_messages_freq(freq_list)
    # Построение графа смежности
    graph = get_network([128397748,  400008940, 68908334])
    plot_graph(graph)
