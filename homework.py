"""Александр Лощилов, Когорта 10+, бэкенд-факультет Python, Rev 1.0"""

from typing import Union

SWM_STEP: float = 1.38
LEN_STEP: float = 0.65
M_IN_KM: int = 1000


class InfoMessage:
    """Класс InfoMessage предназначен для создания сообщений и их отоброжения
    """
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """Возвращает сообщение, содержащее детали тренировки"""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.'
                        )
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = LEN_STEP
    M_IN_KM: int = M_IN_KM

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах), которую преодолел
        пользователь за время тренировки.
        """
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время тренировки, исходя
        из числа совершенных действий (шагов, гребков и т.д.), длины
        шага и количества метров в километре.
        """
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Класс Running предназначен для создания записей тренировок типа 'Бег'
    """
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при беге"""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        mean_speed: float = super().get_mean_speed()
        calories: float = (
            (coeff_calorie_1 * mean_speed - coeff_calorie_2)
            * self.weight / self.M_IN_KM * self.duration * 60
        )
        return calories


class SportsWalking(Training):
    """Класс SportsWalking предназначен для создания записей
    тренировок типа 'Спортивная ходьба'"""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при спортивной ходьбе"""
        coeff_activity_1: float = 0.035
        coeff_activity_2: float = 0.029
        mean_speed: float = super().get_mean_speed()
        calories: float = (
            (coeff_activity_1 * self.weight + (mean_speed**2 // self.height)
             * coeff_activity_2 * self.weight) * self.duration * 60
        )
        return calories


class Swimming(Training):
    LEN_STEP = SWM_STEP

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает дистанцию, пройденную во время плавания, исходя
        из длины бассейна и количества его проходов
        """
        mean_speed: float = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self):
        """Вернуть число калорий, сожженных при плавании"""
        coeff_activity_1: float = 1.1
        coeff_activity_2: int = 2
        mean_speed: float = self.get_mean_speed()
        calories: float = (
            (mean_speed + coeff_activity_1) * coeff_activity_2 * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    workout_record = training_codes[workout_type](*data)
    return workout_record


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages_datatype = list[tuple[str, list[Union[int, float]]]]
    packages: packages_datatype = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
