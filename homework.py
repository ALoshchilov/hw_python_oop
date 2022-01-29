"""Александр Лощилов, Когорта 10+, бэкенд-факультет Python, Rev 3.0"""
from dataclasses import dataclass, fields, asdict
from logging import exception


@dataclass
class InfoMessage:
    """Класс InfoMessage предназначен для создания сообщений и их отоброжения.
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEMPLATE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает сообщение, содержащее детали тренировки."""
        return self.TEMPLATE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах), которую преодолел
        пользователь за время тренировки.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время тренировки, исходя
        из числа совершенных действий (шагов, гребков и т.д.), длины
        шага и количества метров в километре.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
            )


@dataclass
class Running(Training):
    """Класс Running предназначен для создания записей тренировок типа 'Бег'.
    """
    MEAN_SPEED_MULTIPLIER = 18
    MEAN_SPEED_SUBTRACTED = 20

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при беге."""
        return (
            (self.MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             - self.MEAN_SPEED_SUBTRACTED) * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Класс SportsWalking предназначен для создания записей
    тренировок типа 'Спортивная ходьба'."""
    height: float
    WEIGHT_MULTIPLIER = 0.035
    MEAN_SPEED_MULTIPLIER = 0.029

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при спортивной ходьбе."""
        return (
            (self.WEIGHT_MULTIPLIER * self.weight +
             (super().get_mean_speed()**2 // self.height)
             * self.MEAN_SPEED_MULTIPLIER * self.weight)
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class Swimming(Training):
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    MEAN_SPEED_ADDEND = 1.1
    WEIGHT_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время плавания, исходя
        из длины бассейна и количества его проходов.
        """
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при плавании."""
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_ADDEND)
            * self.WEIGHT_MULTIPLIER * self.weight
        )


TRAINING_CODES = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

# Шаблон ошибки для неверного числа аргументов
ERR_LEN_DATA_PACKAGE_TEMPLATE = (
    'Wrong package data. Incorrect number of parameters for {class_name}. '
    'Given: {given_args_number}, expected: {expected_args_number}.'
)
# Шаблон ошибки для неверного типа данных в последовательности
ERR_TYPE_DATA_PACKAGE_TEMPLATE = (
    'Wrong data type detected: {data}. '
    'Data should be a list of ints or floats.'
)
# Шаблон ошибки для неверного кода тренировки
ERR_TRAINING_TYPE_TEMPLATE = 'Error. Incorrect training code: {training_code}.'


def is_correct_package(workout_type: str, data):
    """Проверяет наличие типа тренировки в допустимых кодах
    и соответствие переданного числа аргументов числу аргументов,
    требуемых для создания экземпляра класса.
    Проверятся соответствие числа параметров в пакете, тип тренировки и
    тип данных параметров.
    В случае несоответствия создает исключения, не прерывающие
    обработку дальнейших пакетов"""
    # Страховка неожиданного типа тренировки
    try:
        if workout_type not in TRAINING_CODES:
            raise ValueError
    except ValueError:
        exception(ERR_TRAINING_TYPE_TEMPLATE.format(
            training_code=workout_type
            )
        )
        return False

    # Страховка неверного числа параметров
    try:
        if TRAINING_CODES[workout_type][1] != len(data):
            raise ValueError
    except ValueError:
        exception(ERR_LEN_DATA_PACKAGE_TEMPLATE.format(
                    class_name=TRAINING_CODES[workout_type][0].__name__,
                    given_args_number=len(data),
                    expected_args_number=TRAINING_CODES[workout_type][1]
            )
        )
        return False

    # Страховка неверного типа данных в data
    try:
        if not all(isinstance(i, (int, float)) for i in data):
            raise ValueError
    except ValueError:
        exception(ERR_TYPE_DATA_PACKAGE_TEMPLATE.format(data=data))
        return False

    return True


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TRAINING_CODES[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    PACKAGES = [
        ('SWM', [720, 1, 80, 25, 4]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in PACKAGES:
        # Проверка корректности пакета
        if is_correct_package(workout_type, data):
            main(read_package(workout_type, data))
