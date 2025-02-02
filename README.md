### Суть задачи :
- Создать примитивный web-клиент к существующему jsonrpc-сервису, пройти авторизацию на нём, получать и отображать ответы.
### Запуск
- Получить .env file, положить его в корень проекта;
- Если запускать на винде, то нужно поменять CA_PATH на то, что должно быть на винде, для линукса по идее будет работать с тем, что в дефолтном;
- Далее задача каким-то образом сделать виртуальное окружение в .venv, для примера в Makefile есть команды `make init-deps`, `make install-deps`, которые будут работать если есть venv. Для случае когда есть venv есть шорткат `make start`, который по идее сделает все, что надо;
- Далее запускаем - `make start`. В первый раз он соберет миграции дефолтные, статику. Далее можно запускать через make up, либо привычным вам способом, не забыв поставить переменные из .env в окружение (в случае make команд сделается само).
- Запустить тесты `make test`
### Инфа:
- Сервис запустится по дефолту на 8100 порте, если нужно поменять либо сами, когда запускаем руками без make, либо меняем соотв. переменную в Makefile
- http://localhost:8100/ -- сама форма
- http://localhost:8100/send_request/ -- эндпоинт в который она ходит
