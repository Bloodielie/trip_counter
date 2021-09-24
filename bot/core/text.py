START = "Привет, я бот для подсчета количества поездок."
MENU = "Меню"
BAD_INPUT = "Хм, попробуй ещё раз."
PERMISSION_ERROR = "Ошибка прав доступа."
CHOICE_HISTORY_TYPE = "Выберите тип истории: "

ADD_TRIP = "Добавить поездку"
ADD_BALANCE = "Добавить баланс"
BALANCE = "Баланс"
HISTORY = "История"
BACK = "Назад"
TRIP_HISTORY = "История поездок"
TRANSACTION_HISTORY = "История операций"

COMPLETE = "Завершить"
CONFIRM = "Подтвердить"
CANCEL = "Отменить"

INPUT_DISTANCE = "Введите расстояние: "
INPUT_USERS = "Введите пользователей: "
INPUT_AUTO = "Введите машину: "
USER_ALREADY_SELECT = "Пользователь уже выбран. Попробуйте ещё раз."
NOT_SELECTED_USERS = "Пользователи не выбранны."
SELECT_NEXT_USER = "Выберите следующего пользователя."
NOT_SELECTED_AUTO = "Машина не выбранна"
TRIP_INFO = """
*Поездка: *
Расстояние: `{distance}`;
Машина: `{auto}`;
Выбранные пользователи: `{select_users}`;
"""
CREATED_TRIP = "Поездка создана, цена для одного участника `{:.2f}р`"
USER_BALANCE = "Ваш текущий баланс: `{balance:.2f}р`"
USERS_BALANCES = "{}: `{:.2f}р`"

SELECT_USER = "Выберите пользователя:"
INPUT_AMOUNT = "Введите сумму:"
BALANCE_ADDED = "Баланс добавлен."
NO_DATA = "Данные отсутствуют."
USER_TRANSACTION = "{}: `{:.2f}р`"
USER_TRIP = """*Поездка №{id}: *
Дистанция: `{distance:.1f}км`;
Дата: `{date}`;
Машина: `{auto_identifier}`;
Создатель: `{creator_name}`;
Количество пассажиров: `{number_of_passengers}`;
Стоимость: `{cost:.2f}р`;
"""
