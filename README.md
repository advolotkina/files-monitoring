# Simple files monitoring

Консольное приложение для мониторинга событий, связанных с созданием, удалением и изменение файлов.

Клиентское приложение следит за изменениями в определенной папке и посылает сообщения серверу.
Сервер обрабатывает сообщения клиентов и выводит на экран информацию о событии:

````
{Время получения сообщения}| {путь до файла}                                    |{размер}    |{тип события}
2020-04-29 17:22:14.370767 | ./test_dir/sds/wgrr                                | 20         | MODIFIED
2020-04-29 17:22:14.370814 | ./.idea/workspace.xml                              | 6734       | MODIFIED
2020-04-29 17:22:24.549601 | ./test_dir/dhdhdd/dDdD.py                          | 0          | CREATED
2020-04-29 17:22:28.638154 | ./test_dir/dhdhdd/dDdD.py                          | 16         | MODIFIED
2020-04-29 17:22:28.638203 | ./.idea/workspace.xml                              | 6734       | MODIFIED
2020-04-29 17:22:36.793983 | ./test_dir/dhdhdd/dxgrdg.py                        |            | DELETED
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
