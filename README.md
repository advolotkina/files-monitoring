# Simple files monitoring

Консольное приложение для мониторинга событий, связанных с созданием, удалением и изменение файлов.

Клиентское приложение следит за изменениями в определенной папке и посылает сообщения серверу.
Сервер обрабатывает сообщения клиентов и выводит на экран информацию о событии:

````
{Время получения сообщения}| {путь до файла}                                    |{размер}    |{тип события}
2020-04-29 17:43:50.925681 | /home/zhblnd/PycharmProjects/file-monitor/test_dir/sds/wgrr            |            | DELETED
2020-04-29 17:43:50.925730 | /home/zhblnd/PycharmProjects/file-monitor/.idea/workspace.xml          | 8159       | MODIFIED
2020-04-29 17:43:50.925751 | /home/zhblnd/PycharmProjects/file-monitor/dir_monitor_server.py        | 3718       | MODIFIED
2020-04-29 17:44:07.223176 | /home/zhblnd/PycharmProjects/file-monitor/test_dir/dhdhdd/fasAAA.py    | 0          | CREATED
````
## Requirements

```
python 3.x, virtualenv, pip
watchdog library
jsonchema library
```

##Setup

```
virtualenv venv
pip install -r requirements.txt
```

## Usage

```
$ ./dir_monitor.py -h
usage: dir_monitor.py [-h] -dir DIR -host HOST -port PORT

optional arguments:
  -h, --help           show this help message and exit
  -dir DIR, -d DIR     Определяет директорию, файлы которой, необходимо отслеживать
  -host HOST           Определяет IP адрес сервера, на который необходимо посылать сообщения
  -port PORT, -p PORT  Определяет порт сервера, на который необходимо посылать сообщения

$ ./dir_monitor.py -d . -host 127.0.0.2 -p 8888
```
```
$ ./dir_monitor_server.py -h
usage: dir_monitor_server.py [-h] [-host HOST] [-port PORT]

optional arguments:
  -h, --help  show this help message and exit
  -host HOST  Определяет IP адрес данного сервера, по умолчанию - 127.0.0.2
  -port PORT  Определяет порт данного сервера, по умолчанию - 8888

$ ./dir_monitor_server.py 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
