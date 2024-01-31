import argparse
import datetime
import logging
import traceback

months = {'января': 1, 'февраля': 2, 'марта': 3,
          'апреля': 4, 'мая': 5, 'июня': 6,
          'июля': 7, 'августа': 8, 'сентября': 9,
          'октября': 10, 'ноября': 11, 'декабря': 12}

weekdays = {'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3,
            'пятница': 4, 'суббота': 5, 'воскресенье': 6}


class LogData:
    def __init__(self, args, result, error_message):
        self.args = args
        self.result = result
        self.error_message = error_message


logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(levelname)s | %(asctime)s | %(funcName)s | LogData: %(log_data)s | Message: %(message)s',
                    encoding='utf-8')  # Указываем кодировку


def logging_decorator(func):
    def wrapper(*args, **kwargs):
        log_data = LogData(args=args, result=None, error_message=None)
        try:
            result = func(*args, **kwargs)
            log_data.result = result
            return result
        except Exception as e:
            log_data.error_message = f"Такой даты не существует! (Введенная дата: {args[0]})"
            # Добавляем в лог информацию о введенной дате и стек вызовов
            logging.error(f"Error: {log_data.error_message}\n{traceback.format_exc()}", extra={'log_data': log_data})
            raise ValueError(log_data.error_message)

    return wrapper


@logging_decorator
def date_from_text(date):
    day, weekday, month = date.split()
    weeks = int(day.split('-')[0])
    month = months[month]
    weekday = weekdays[weekday]

    # Добавим вывод значений в лог
    logging.info(f"Day: {day}, Weekday: {weekday}, Month: {month}, Weeks: {weeks}")

    date_ = datetime.datetime(year=datetime.datetime.now().year, month=month, day=1)

    # В любой неделе не более 4-х дней, поэтому допустим только weeks от 1 до 4
    if 1 <= weeks <= 4:
        while date_.weekday() != weekday:
            date_ += datetime.timedelta(days=1)
        result = date_ + datetime.timedelta(weeks=weeks - 1)
    else:
        raise ValueError(f"Такой даты не существует! (Введенная дата: {date})")

    # Добавим дополнительный вывод в лог
    logging.info(f"Input date: {date}, Calculated date: {result}")

    if result.month != month:
        raise ValueError(f"Такой даты не существует! (Введенная дата: {date})")
    return result


def parse_args():
    parser = argparse.ArgumentParser(description='Converts text to a date in the current year.')
    parser.add_argument('date', nargs='?', default=None, help='Input date text in the format: "1-й четверг ноября"')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.date:
        try:
            print(date_from_text(args.date))
        except ValueError as ve:
            print(ve)
    else:
        print(date_from_text('1-й четверг ноября'))
