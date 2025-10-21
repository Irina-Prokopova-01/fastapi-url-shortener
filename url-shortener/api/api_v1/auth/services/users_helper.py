from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    Что мне нужно от обертки:
    - получение пароля по username
    - совпадает ли пароль с переданным
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному username находит пароль.
        Возвращает пароль если есть.

        :param username: - имя пользователя
        :return: - пароль по пользователю, если найден.
        """

    @classmethod
    def check_passwords_math(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Проверка поролей на совпадение. Если совпадают, то True
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
         Проверить валиден ли пароль.
        :param username: - чей пароль проверить
        :param password: - переданный пароль сверить с тем что в BD
        :return: True если совпадают, иначе False
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_math(password1=db_password, password2=password)
