class KMP_StringSearch:
    """
    Класс для поиска подстроки в тексте с использованием алгоритма Кнута-Морриса-Пратта (KMP).

    """

    def __init__(self, pattern: str) -> None:
        """
        Инициализация класса KMP_StringSearch.

        Параметры:
        - pattern (str): Шаблон (подстрока), которую необходимо найти.
        """
        self.pattern = pattern
        self.borders = self._find_borders()

    def _find_borders(self) -> list:
        """
        Вычисляет массив граней (borders) для алгоритма KMP.

        Возвращает:
        - list: Массив граней для заданного шаблона.
        """
        borders = [0] * len(self.pattern)
        current_index = 0
        for i in range(1, len(self.pattern)):
            while current_index > 0 and self.pattern[current_index] != self.pattern[i]:
                current_index = borders[current_index - 1]
            if self.pattern[current_index] == self.pattern[i]:
                current_index += 1
            borders[i] = current_index
        return borders

    def get_substring_kmp(self, text: str) -> list:
        """
        Находит все вхождения подстроки в тексте с использованием алгоритма KMP.

        Параметры:
        - text (str): Текст, в котором ищется подстрока.

        Возвращает:
        - list: Список индексов начала вхождений подстроки в текст.
        """
        result = []
        compare_index = 0
        for i in range(len(text)):
            while compare_index > 0 and text[i] != self.pattern[compare_index]:
                compare_index = self.borders[compare_index - 1]
            if text[i] == self.pattern[compare_index]:
                compare_index += 1
            if compare_index == len(self.pattern):
                result.append(i - compare_index + 1)
                compare_index = self.borders[len(self.pattern) - 1]
        return result