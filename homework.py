class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           distance,
                           speed,
                           calories)
        return info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calories = ((coeff_calorie_1 * Training.get_mean_speed(self)
                    - coeff_calorie_2) * self.weight / self.M_IN_KM
                    * self.duration * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    """Получить количество затраченных калорий."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        calories = ((coeff_calorie_1 * self.weight
                    + (Training.get_mean_speed(self)**2 // self.height)
                    * coeff_calorie_2 * self.weight) * self.duration
                    * self.MIN_IN_H)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    """Получить среднюю скорость движения."""
    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    """Получить количество затраченных калорий."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        calories = ((self.get_mean_speed() + coeff_calorie_1)
                    * coeff_calorie_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_train = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict_train[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
