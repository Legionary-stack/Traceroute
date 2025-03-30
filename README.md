# Утилита Traceroute

## Автор

Банников Максим КН-203

## Описание

Программа выполняет трассировку маршрута до указанного хоста с дополнительной информацией о каждом узле:

- Номер хопа
- IP-адрес
- Номер автономной системы (AS)
- Страна
- Провайдер/организация

## Особенности

- Работает на Windows и Unix-системах
- Использует API ip-api.com
- Определяет локальные IP-адреса
- Форматирует вывод в виде таблицы

## Установка

1. Убедитесь, что установлен Python 3.6+
2. Установите зависимости:

```bash
pip install requests
```

## Использование

Запустите программу

```bash
python traceroute.py
```

Пример вывода к example.com:

```text
Результаты трассировки:
№  | IP-адрес      | AS       | Страна | Провайдер
---|---------------|----------|--------|-----------
1  | 192.168.0.1   | Локальная | N/A    | Маршрутизатор                 
2  | 94.50.136.1   | AS12389  | RU     | OJSC Uralsvyazinform          
3  | 79.133.87.242 | AS12389  | RU     | PJSC Rostelecom               
7  | 154.54.75.86  | AS174    | SE     | Cogent Communications         
8  | 154.54.61.241 | AS174    | SE     | Cogent Communications         
9  | 154.54.61.221 | AS174    | DK     | Cogent Communications         
10 | 154.54.38.205 | AS174    | DE     | Cogent Communications         
11 | 154.54.77.246 | AS174    | GB     | Cogent Communications         
12 | 154.54.44.166 | AS174    | CA     | Cogent Communications         
13 | 154.54.47.141 | AS174    | GB     | Cogent Communications         
14 | 154.54.31.233 | AS174    | CA     | Cogent Communications         
15 | 154.54.7.129  | AS174    | US     | Cogent Communications         
16 | 154.54.166.73 | AS174    | US     | Cogent Communications         
17 | 154.54.165.77 | AS174    | US     | Cogent Communications         
18 | 154.54.167.137 | AS174    | US     | Cogent Communications         
20 | 154.54.43.10  | AS174    | US     | Cogent Communications         
21 | 154.54.43.14  | AS174    | US     | Cogent Communications         
22 | 23.203.158.19 | AS20940  | US     | Akamai International B.V.
```


