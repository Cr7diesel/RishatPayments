Web приложение RishatPayments:

Описание проекта: 

Пиложение интегрируется по api с платежной системой Stripe для покупки различных товаров.

Запуск приложения:

    Клонируйте репозиторий:

git clone https://github.com/Cr7diesel/RishatPayments.git

    Перейдите в склонированный каталог проекта:

git cd RishatPayments

Создание переменной окружения:

    Создайте файл .env и внесите данные из .env.example

Запуск приложения:

    Откройте терминал => перейдите в каталог проекта =>
    запустите приложение с помощью команды:

docker-compose up --build

Создание суперпользователя:

    Выполните команду:

docker-compose run payments python3 manage.py createsuperuser 

    Введите все необходимые данные