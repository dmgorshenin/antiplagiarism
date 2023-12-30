import re
import pymorphy2
import string
from unidecode import unidecode


class CanonicalTextClass:
    """
    Класс для обработки и создания канонического текста и шинглов на основе входного текста.

    """

    def __init__(self, text: str, shingle_size: int = 5) -> None:
        """
        Инициализация класса CanonicalTextClass.

        Параметры:
        - text (str): Входной текст для обработки.
        - shingle_size (int): Размер шингла для создания (по умолчанию 5).
        """
        self.morph = pymorphy2.MorphAnalyzer()
        self.text = text
        self.shingles = []
        self.shingle_size = shingle_size

    def _clear_garbage(self, text: str) -> str:
        """
        Удаляет шум, приводит к нижнему регистру и очищает текст.

        Параметры:
        - text (str): Входной текст.

        Возвращает:
        - str: Очищенный текст.
        """
        words = text.split()
        words = [word for word in words if word.lower() not in self.STOP_WORDS]
        text = ' '.join(words)
        text = unidecode(text)
        text = re.sub(r'["“”„”«»’‘<…>\'\"]', '', text)
        text = re.sub(r'[-—–―]+', '', text)
        text = re.sub(r"''", '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'[^\x20-\x7E\n]+', '', text)
        return text

    def _remove_unnecessary(self, text: str) -> str:
        """
        Удаляет прилагательные, причастия, наречия и предлоги из текста.

        Параметры:
        - text (str): Входной текст.

        Возвращает:
        - str: Текст с удаленными прилагательными, причастиями, наречиями и предлогами.
        """
        sentence_without_punctuation = ''.join(char if char not in string.punctuation else '' for char in text)
        words = sentence_without_punctuation.split()
        filtered_words = [word for word in words if self.morph.parse(word)[0].tag.POS not in {'ADJF', 'ADJS', 'PRTF', 'PRTS', 'GRND', 'ADVB'} and not any(char.isdigit() for char in word)]
        return ' '.join(filtered_words)

    def _singularize_nouns_and_verbs(self, text: str) -> str:
        """
        Приводит существительные и глаголы в русском тексте к форме единственного числа.

        Параметры:
        - text (str): Входной текст.

        Возвращает:
        - str: Текст с приведенными к единственному числу существительными и глаголами.
        """
        words = text.split()
        singularized_words = []
        for word in words:
            parsed_word = self.morph.parse(word)[0]
            if parsed_word.tag.POS in {'NOUN'}:
                try:
                    singularized_word = parsed_word.inflect({'nomn', 'sing'}).word
                    singularized_words.append(singularized_word)
                except Exception:
                    singularized_words.append(word)
                    continue
            elif parsed_word.tag.POS in {'VERB'}:
                try:
                    singularized_word = parsed_word.normal_form
                    singularized_words.append(singularized_word)
                except Exception:
                    singularized_words.append(word)
                    continue
            else:
                singularized_words.append(word)
        return ' '.join(singularized_words)

    def create_shingles(self) -> list[str]:
        """
        Создает шинглы из канонического текста.

        Возвращает:
        - list[str]: Список шинглов.
        """
        # text = self.make_canonical()
        words = self.text.split()
        shingles = [words[i:i + self.shingle_size]
                    for i in range(len(words) - self.shingle_size + 1)]
        return [' '.join(shingle) for shingle in shingles]

    def make_canonical(self) -> str:
        """
        Создает каноническую форму входного текста.

        Возвращает:
        - str: Каноническая форма текста.
        """
        without_adjectives = self._remove_unnecessary(
            self.text)
        singularized_sentence = self._singularize_nouns_and_verbs(
            without_adjectives)
        self.text = self._clear_garbage(singularized_sentence)
        return self.text

    STOP_WORDS = {'и', 'в', 'не', 'на', 'с', 'по', 'за', 'к',
                  'от', 'из', 'до', 'у', 'для', 'о', 'перед',
                  'через', 'ох', 'ой', 'пли', 'ух', 'фу', 'фи',
                  'ага', 'ах', 'апчхи', 'увы', 'тьфу', 'да',
                  'пусть', 'пускай', 'давайте', 'давай', 'бы',
                  'б', 'бывало', 'нет', 'вовсе', 'отнюдь', 'никак',
                  'неужели', 'разве', 'вон', 'именно', 'прямо',
                  'точь-в-точь', 'только', 'лишь', 'исключительно',
                  'почти', 'единственно', 'даже', 'ни', 'же', 'ведь',
                  'уж', 'всё-таки', 'всё', 'ка', 'то', 'я', 'ты',
                  'он', 'она', 'оно', 'они', 'себя', 'что', 'кто',
                  'некто', 'нечто', 'никто', 'ничто', 'мой', 'моя',
                  'моё', 'мои', 'ваш', 'наш', 'чей', 'который',
                  'никакой', 'некий', 'какой', 'как', 'будто',
                  'все', 'весь', 'всяк', 'всякий', 'любой', 'каждый'
                  'сам', 'самый', 'другой', 'иной', 'но', 'под', 'так'}