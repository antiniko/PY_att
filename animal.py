import argparse
import logging
import traceback
import inspect


class LogData:
    def __init__(self, args, result, error_message):
        self.args = args
        self.result = result
        self.error_message = error_message


logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(levelname)s | %(asctime)s | %(funcName)s | LogData: %(log_data)s | Message: %(message)s',
                    encoding='utf-8')


def logging_decorator(func):
    def wrapper(*args, **kwargs):
        log_data = LogData(args=args, result=None, error_message=None)
        try:
            if inspect.isclass(func):
                instance = func(*args, **kwargs)
                result = None
            else:
                instance = None
                result = func(*args, **kwargs)

            log_data.result = result
            return result
        except argparse.ArgumentError as e:
            log_data.error_message = f"Ошибка в аргументах командной строки: {e}"
            logging.error(f"{log_data.error_message}\n{traceback.format_exc()}", extra={'log_data': log_data})
            raise argparse.ArgumentError(None, "Ошибка в аргументах командной строки.")
        except Exception as e:
            log_data.error_message = f"Ошибка: {e} (Аргументы: {args})"
            logging.error(f"{log_data.error_message}\n{traceback.format_exc()}", extra={'log_data': log_data})
            raise argparse.ArgumentError(None, "Ошибка выполнения программы.")

    return wrapper


def parse_args():
    try:
        parser = argparse.ArgumentParser(description='Создание экземпляров животных и получение информации о них.')
        parser.add_argument('--animal', choices=['bird', 'fish', 'mammal'], help='Тип животного (bird, fish, mammal)')
        parser.add_argument('--name', required=True, help='Имя животного')
        parser.add_argument('--wingspan', type=float, help='Размах крыльев птицы (только для птиц)')
        parser.add_argument('--max_depth', type=float, help='Максимальная глубина рыбы (только для рыбы)')
        parser.add_argument('--weight', type=float, help='Вес млекопитающего (только для млекопитающих)')
        args = parser.parse_args()

        if args.max_depth is not None and args.max_depth < 0:
            raise argparse.ArgumentError(None, "Максимальная глубина должна быть неотрицательным числом.")
        if args.weight is not None and args.weight < 0:
            raise argparse.ArgumentError(None, "Вес должен быть неотрицательным числом.")
        if args.wingspan is not None and args.wingspan < 0:
            raise argparse.ArgumentError(None, "Размах крыльев должен быть неотрицательным числом.")

        return args
    except SystemExit:
        raise argparse.ArgumentError(None, "Отсутствуют или неверные аргументы командной строки.")
    except Exception as e:
        raise argparse.ArgumentError(None, f"Ошибка в аргументах командной строки: {e}")


@logging_decorator
def main():
    args = parse_args()

    if args.animal == 'bird':
        animal_instance = Bird(name=args.name, wingspan=args.wingspan)
    elif args.animal == 'fish':
        animal_instance = Fish(name=args.name, max_depth=args.max_depth)
    elif args.animal == 'mammal':
        animal_instance = Mammal(name=args.name, weight=args.weight)
    else:
        print("Недопустимый тип животного. Пожалуйста, выберите 'bird', 'fish' или 'mammal'.")
        exit(1)

    print(f"Тип животного: {args.animal.capitalize()}")
    print(f"Имя: {animal_instance.name}")

    if args.animal == 'bird':
        print(f"Размах крыльев: {animal_instance.wing_length()}")
    elif args.animal == 'fish':
        print(f"Категория глубины: {animal_instance.depth()}")
    elif args.animal == 'mammal':
        print(f"Категория веса: {animal_instance.category()}")


class Animal:
    def __init__(self, name):
        self.name = name


class Bird(Animal):
    def __init__(self, name, wingspan):
        super().__init__(name)
        self.wingspan = wingspan

    def wing_length(self):
        return self.wingspan / 2


class Fish(Animal):
    def __init__(self, name, max_depth):
        super().__init__(name)
        self.max_depth = max_depth

    def depth(self):
        if self.max_depth < 10:
            return "Мелководная рыба"
        elif self.max_depth > 100:
            return "Глубоководная рыба"
        else:
            return "Средневодная рыба"


class Mammal(Animal):
    def __init__(self, name, weight):
        super().__init__(name)
        self.weight = weight

    def category(self):
        if self.weight < 1:
            return "Малявка"
        elif self.weight > 200:
            return "Гигант"
        else:
            return "Обычный"


if __name__ == '__main__':
    main()
