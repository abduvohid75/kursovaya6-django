# Курсовая 6 - Джанго

## Как запустить проект
1. Первым делом необходимо создать свою базу данных <b>PostgreSQL</b> и ввести ее значения в файл [.env](.env) в поля:<br><b>NAME</b><br><b>USER</b><br><b>DB_PASSWORD</b>
2. При необходимости можно изменить почту, с которой будут отправляться рассылки. За это в файле [.env](.env) отвечают поля
<b>EMAIL_HOST</b> <br>
<b>EMAIL_HOST_USER</b> <br>
<b>EMAIL_HOST_PASSWORD</b> <br>
<b>DEFAULT_FROM_EMAIL</b><br>
3. После ввода в консоль команды ```python3 manage.py runserver``` сервер должен успешно запуститься