class BM_StringSearch:
    """
    Класс для поиска подстроки в тексте с использованием алгоритма Бойера-Мура.

    """

    def __init__(self, pattern, array_size: int = 128) -> None:
        """
        Инициализация класса BM_StringSearch.

        Параметры:
        - pattern (str): Шаблон (подстрока), которую необходимо найти.
        - array_size (int): Размер алфавита (по умолчанию 128).
        """
        self.pattern = pattern
        self.array_size = array_size
        self.symbol_indexes = self._bad_character_heuristic()
        self.shifts = self._good_suffix_heuristic()

    def _bad_character_heuristic(self) -> list:
        """
        Вычисляет эвристику плохого символа для алгоритма Бойера-Мура.

        Возвращает:
        - list: Список индексов плохих символов.
        """
        result = [-1] * self.array_size

        for i in range(len(self.pattern)):
            result[ord(self.pattern[i]) % self.array_size] = i

        return result

    def _good_suffix_heuristic(self) -> list:
        """
        Вычисляет эвристику хорошего суффикса для алгоритма Бойера-Мура.

        Возвращает:
        - list: Список сдвигов для хороших суффиксов.
        """
        shifts = [0] * (len(self.pattern) + 1)
        border_positions = [0] * (len(self.pattern) + 1)
        self._find_shifts_and_borders(shifts, border_positions)
        self._set_shifts_for_prefix(shifts, border_positions)
        return shifts

    def _find_shifts_and_borders(self, shifts: list, border_positions: list) -> None:
        """
        Вычисляет сдвиги и позиции границ для эвристики хорошего суффикса.

        Параметры:
        - shifts (list): Список для хранения сдвигов.
        - border_positions (list): Список для хранения позиций границ.
        """
        i = len(self.pattern)
        j = len(self.pattern) + 1
        border_positions[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]:
                if shifts[j] == 0:
                    shifts[j] = j - i
                j = border_positions[j]
            i -= 1
            j -= 1
            border_positions[i] = j

    def _set_shifts_for_prefix(self, shifts: list, border_positions: list) -> None:
        """
        Устанавливает сдвиги для префиксов в эвристике хорошего суффикса.

        Параметры:
        - shifts (list): Список для хранения сдвигов.
        - border_positions (list): Список для хранения позиций границ.
        """
        prefix_border = border_positions[0]
        for i in range(len(self.pattern) + 1):
            if shifts[i] == 0:
                shifts[i] = prefix_border
            if i == prefix_border:
                prefix_border = border_positions[prefix_border]

    def get_substring_bm_bad_character(self, text: str) -> list:
        """
        Находит все вхождения подстроки в тексте с использованием алгоритма Бойера-Мура
        с эвристикой плохого символа.

        Параметры:
        - text (str): Текст, в котором ищется подстрока.

        Возвращает:
        - list: Список индексов начала вхождений подстроки в текст.
        """
        result = []
        shift = 0

        while shift <= (len(text) - len(self.pattern)):
            current_index = len(self.pattern) - 1

            while current_index >= 0 and self.pattern[current_index] == text[shift + current_index]:
                current_index -= 1

            if current_index == -1:
                result.append(shift)

                indent = len(self.pattern) - (self.symbol_indexes[ord(text[shift + len(
                    self.pattern)]) % self.array_size] if shift + len(self.pattern) < len(text) else -1)
                shift += indent if shift + len(self.pattern) < len(text) else 1
            else:
                indent = self.symbol_indexes[ord(
                    text[shift + current_index]) % self.array_size] if shift + current_index < len(text) else -1
                shift += max(1, current_index - indent)

        return result

    def get_substring_bm_good_suffix(self, text: str) -> list:
        """
        Находит все вхождения подстроки в тексте с использованием алгоритма Бойера-Мура
        с эвристикой хорошего суффикса.

        Параметры:
        - text (str): Текст, в котором ищется подстрока.

        Возвращает:
        - list: Список индексов начала вхождений подстроки в текст.
        """
        result = []
        shift = 0

        while shift <= (len(text) - len(self.pattern)):
            current_index = len(self.pattern) - 1

            while current_index >= 0 and self.pattern[current_index] == text[shift + current_index]:
                current_index -= 1

            if current_index == -1:
                result.append(shift)
                shift += self.shifts[0]
            else:
                shift += self.shifts[current_index + 1]

        return result