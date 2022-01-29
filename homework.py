"""Александр Лощилов, Когорта 10+, бэкенд-факультет Python, Rev 2.0"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class InfoMessage:
    """Класс InfoMessage предназначен для создания сообщений и их отоброжения
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    # Вынос шаблона сообщения в константу
    MSG_TEMPLATE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {training_duration:.3f} ч.; '
        'Дистанция: {training_distance:.3f} км; '
        'Ср. скорость: {training_mean_speed:.3f} км/ч; '
        'Потрачено ккал: {training_spent_callories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает сообщение, содержащее детали тренировки"""
        return self.MSG_TEMPLATE.format(
            training_type=self.training_type,
            training_duration=self.duration,
            training_distance=self.distance,
            training_mean_speed=self.speed,
            training_spent_callories=self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    # Вывод названия типа тренировки. В прошлой версии для этого использовалось
    # имя класса instance.__class__.__name__
    def __str__(self):
        return 'Traning'

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах), которую преодолел
        пользователь за время тренировки.
        """
        # Удаление одноразовой переменной в соответствие с замечанием
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время тренировки, исходя
        из числа совершенных действий (шагов, гребков и т.д.), длины
        шага и количества метров в километре.
        """
        # Удаление одноразовой переменной в соответствие с замечанием
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__str__(),
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


@dataclass
class Running(Training):
    """Класс Running предназначен для создания записей тренировок типа 'Бег'
    """
    # Присвоение осмысленного имени константам и их вынос в тело класса
    RUNNING_MEAN_SPEED_MULTIPLIER = 18
    RUNNING_MEAN_SPEED_SUBTRACTED = 20

    # Вывод названия типа тренировки. В прошлой версии для этого использовалось
    # имя класса instance.__class__.__name__
    def __str__(self) -> str:
        """Возвращает тип тренировки"""
        return 'Running'

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при беге"""
        # Удаление одноразовой переменной в соответствие с замечанием
        return (
            (self.RUNNING_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
             - self.RUNNING_MEAN_SPEED_SUBTRACTED) * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Класс SportsWalking предназначен для создания записей
    тренировок типа 'Спортивная ходьба'"""
    height: float
    # Присвоение осмысленного имени константам и их вынос в тело класса
    WALKING_WEIGHT_MULTIPLIER = 0.035
    WALKING_MEAN_SPEED_MULTIPLIER = 0.029

    # Вывод названия типа тренировки. В прошлой версии для этого использовалось
    # имя класса instance.__class__.__name__
    def __str__(self) -> str:
        """Возвращает тип тренировки"""
        return 'SportsWalking'

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при спортивной ходьбе"""
        # Удаление одноразовой переменной в соответствие с замечанием
        return (
            (self.WALKING_WEIGHT_MULTIPLIER * self.weight
             + (super().get_mean_speed()**2 // self.height)
             * self.WALKING_MEAN_SPEED_MULTIPLIER * self.weight)
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class Swimming(Training):
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    # Присвоение осмысленного имени константам и их вынос в тело класса
    SWIMMING_MEAN_SPEED_ADDEND = 1.1
    SWIMMING_WEIGHT_MULTIPLIER = 2

    # Вывод названия типа тренировки. В прошлой версии для этого использовалось
    # имя класса instance.__class__.__name__
    def __str__(self) -> str:
        """Возвращает тип тренировки"""
        return 'Swimming'

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время плавания, исходя
        из длины бассейна и количества его проходов
        """
        # Удаление одноразовой переменной в соответствие с замечанием
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при плавании"""
        # Удаление одноразовой переменной в соответствие с замечанием
        return (
            (self.get_mean_speed() + self.SWIMMING_MEAN_SPEED_ADDEND)
            * self.SWIMMING_WEIGHT_MULTIPLIER * self.weight
        )


# Вынос в константу на уровне модуля в соответствии с замечанием
TRAINING_CODES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}
# Словарь с числом параметров каждого класса
PARAMETER_NUMBERS = {
    'SWM': len(Swimming.__dataclass_fields__),
    'RUN': len(Running.__dataclass_fields__),
    'WLK': len(SportsWalking.__dataclass_fields__)
}
# Шаблон ошибки для неверного числа аргументов
ERR_DATA_PACKAGE_TEMPLATE = (
    'Wrong package data. Incorrect number of parameters for {class_name}. '
    'Given: {given_args_number}, expected: {expected_args_number}.'
)
# Шаблон ошибки для неверного кода тренировки
ERR_TRAINING_TYPE_TEMPLATE = 'Error. Incorrect training code: {training_code}'


def read_package(workout_type: str, data) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    # Проверка числа аргументов и вывод ошибки
    if PARAMETER_NUMBERS[workout_type] != len(data):
        print(
            ERR_DATA_PACKAGE_TEMPLATE.format(
                class_name=TRAINING_CODES[workout_type].__name__,
                given_args_number=len(data),
                expected_args_number=PARAMETER_NUMBERS[workout_type]
            )
        )
        return

    # Удаление одноразовой переменной в соответствие с замечанием
    return TRAINING_CODES[workout_type](*data)


def main(training: Optional[Training]) -> None:
    """Главная функция."""
    if training is None:
        print('Empty class. Possible reason: wrong data package')
        return
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    # Удалена аннотация, имя соответствует константе
    PACKAGES = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in PACKAGES:
        # Проверка корректности кода тренировки
        if workout_type not in TRAINING_CODES:
            print(
                ERR_TRAINING_TYPE_TEMPLATE.format(
                    training_code=workout_type
                )
            )
            continue
        main(read_package(workout_type, data))
