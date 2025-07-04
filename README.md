# RPG-Neuro
Проект по М.О., который использует перетренированный чат gpt-2 для создания аутентичного и осознаваемого описания/чата с различными вариациями фентези историй и персонажей.

Ссылка на модель: https://huggingface.co/DevidCipher/RPG-Neuro

Ссылка на docker: https://hub.docker.com/r/devidcipher/rpg-neuro

Инструкция по разворачиванию проекта через docker: 

1. Pull докер образ с docker hub:
   
```shell
docker pull devidcipher/rpg-neuro:latest
```

2. Run докер образ, который вы загрузили:
   
```shell
docker run -d -p 5000:5000 --name rpg-neuro
```

(При первом запуске, рекомендую не использовать аргумент -d)

3. Проверьте что контейнер работает:

```shell
docker ps
```

4. Зайдите на сайт приложения и пользуйтесь:
   
http://127.0.0.1:5000 или http://192.168.0.xxx:5000
(где xxx - ваше положение в сети)

Для остановки приложения:

```shell
docker stop rpg-neuro
```

Пример работы rpg-neuro:

![cc6f7a23-df3a-4b64-a839-25940f5886cc](https://github.com/user-attachments/assets/ae606659-4694-4345-a6de-19cba8784418)


Kafka официально DeD/404/502. Попытки её воскресить не удались. 

