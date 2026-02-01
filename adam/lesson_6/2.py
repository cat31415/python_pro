from flask import Flask

app = Flask(__name__)

@app.route('/')
def presentation():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Колледж строительства и дизайна г. Махачкала</title>
    </head>
    <body>
        <h1>Колледж строительства и дизайна г. Махачкала</h1>
        <p>Приветствуем Вас!</p>
        <ul>
            <li>Специальности: Строительство, Архитектура, Дизайн интерьеров</li>
            <li>Адрес: г. Махачкала, улица Ленина, дом 15</li>
            <li>Телефон: +7 (999) 123-45-67</li>
        </ul>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)