from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    id = request.query.id
    label = request.query.label
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    s = session()
    row = s.query(News).filter(News.id == id).first()
    # 3. Изменить значение метки записи на значение label
    row.label = label
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    s = session()
    for item in get_news('https://news.ycombinator.com/'):
        rows_count = len(s.query(News).filter(News.title == item['title'], News.author == item['author']).all())
        if rows_count != 0:
            continue
        news = News(title=item['title'],
                    author=item['author'],
                    url=item['url'],
                    comments=item['comments'],
                    points=item['points'])
        s.add(news)
    # 3. Сохранить в БД те новости, которых там нет
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
