class RK_StringSearch:
    """
    Класс для поиска подстроки в тексте с использованием алгоритма Рабина-Карпа.

    """

    def __init__(self, pattern: str) -> None:
        """
        Инициализация класса RK_StringSearch.

        Параметры:
        - pattern (str): Шаблон (подстрока), которую необходимо найти.
        """
        self.pattern = pattern

    def get_substring_rk(self, text: str) -> list:
        """
        Находит все вхождения подстроки в тексте с использованием алгоритма Рабина-Карпа.

        Параметры:
        - text (str): Текст, в котором ищется подстрока.

        Возвращает:
        - list: Список индексов начала вхождений подстроки в текст.
        """
        result = []
        alphabet_size = 256
        mod = 9973
        pattern_hash = ord(self.pattern[0]) % mod
        text_hash = ord(text[0]) % mod
        first_index_hash = 1
        for i in range(1, len(self.pattern)):
            pattern_hash = (pattern_hash * alphabet_size +
                            ord(self.pattern[i])) % mod
            text_hash = (text_hash * alphabet_size + ord(text[i])) % mod
            first_index_hash = (first_index_hash * alphabet_size) % mod
        for i in range(len(text) - len(self.pattern) + 1):
            if pattern_hash == text_hash and self._compare_text(text, i):
                result.append(i)
            if i == len(text) - len(self.pattern):
                break
            text_hash = (
                text_hash - (ord(text[i]) * first_index_hash) % mod + mod) % mod
            text_hash = (text_hash * alphabet_size +
                         ord(text[i + len(self.pattern)])) % mod
        return result

    def _compare_text(self, text: str, index: int) -> bool:
        """
        Сравнивает подстроку с текстом начиная с заданного индекса.

        Параметры:
        - text (str): Текст.
        - index (int): Индекс начала сравнения в тексте.

        Возвращает:
        - bool: True, если подстрока совпадает с текстом, False в противном случае.
        """
        for i in range(len(self.pattern)):
            if self.pattern[i] != text[index + i]:
                return False
        return True