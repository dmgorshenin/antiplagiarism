#!/usr/bin/python
# -*- coding: utf8 -*-
from TextCanonization import CanonicalTextClass
from ClassBM import BM_StringSearch
from ClassKMP import KMP_StringSearch
from ClassRK import RK_StringSearch
from ReadWriteDatabase import read_json, write_json, read_txt_and_write_to_json


class AntiPlagiarismClass():

    def __init__(self) -> None:
        """Инициализация класса AntiPlagiarismClass.

        Читает базу канонических текстов и инициализирует переменные класса.
        """
        canonical_text_dict, self.size_dict = read_json(
            "canonicaldatabase.json")
        self.canonical_text = [text for text in canonical_text_dict.values()]

    def set_pattern(self, pattern: str) -> None:
        """
        Устанавливает образец для поиска.

        Args:
            pattern (str): Образец для поиска.
        """
        self.canonical_pattern_object = CanonicalTextClass(pattern, 3)
        self.canonical_pattern_object.make_canonical()

    def get_pattern(self) -> str:
        if self.canonical_pattern_object.text:
            return self.canonical_pattern_object.text

    def update_database_text(self, new_text: str) -> None:
        """
        Обновляет базу новым текстом.

        Args:
            new_text (str): Новый текст для добавления в базу.
        """
        write_json("database.json", f"text{self.size_dict + 1}", new_text)
        self.canonical_text.append(
            CanonicalTextClass(new_text).make_canonical())
        write_json("canonicaldatabase.json",
                   f"text{self.size_dict + 1}", self.canonical_text[-1])
        self.size_dict += 1

    def update_database_from_txt(self, txt_file_path: str) -> None:
        """
        Обновляет базу из текстового файла.

        Args:
            txt_file_path (str): Путь к текстовому файлу.
        """
        read_txt_and_write_to_json(
            txt_file_path, "database.json", f"text{self.size_dict + 1}")
        self.canonical_text.append(
            CanonicalTextClass(read_json("database.json")[0][f"text{self.size_dict + 1}"]).make_canonical())
        write_json("canonicaldatabase.json",
                   f"text{self.size_dict + 1}", self.canonical_text[-1])
        self.size_dict += 1

    def search_plagiarism_RK(self) -> float:
        """
        Поиск плагиата с использованием алгоритма Рабина-Карпа.

        Returns:
            float: Процент уникальности.
        """
        counter = []
        pattern_shingles = self.canonical_pattern_object.create_shingles()
        for shingle in pattern_shingles:
            for text in self.canonical_text:
                search_object = RK_StringSearch(shingle)
                search_list = search_object.get_substring_rk(text)
                if search_list:
                    counter.append(search_list)
        return abs(1 - (len(counter)/len(pattern_shingles))) * 100, counter

    def search_plagiarism_KMP(self) -> float:
        """
        Поиск плагиата с использованием алгоритма Кнута-Морриса-Пратта.

        Returns:
            float: Процент уникальности.
        """
        counter = []
        pattern_shingles = self.canonical_pattern_object.create_shingles()
        for shingle in pattern_shingles:
            for text in self.canonical_text:
                search_object = KMP_StringSearch(shingle)
                search_list = search_object.get_substring_kmp(text)
                if search_list:
                    counter.append(search_list)
        return abs(1 - (len(counter)/len(pattern_shingles))) * 100, counter

    def search_plagiarism_BM_bad(self) -> float:
        """
        Поиск плагиата с использованием алгоритма Бойера-Мура с эвристикой плохого символа.

        Returns:
            float: Процент уникальности.
        """
        counter = []
        pattern_shingles = self.canonical_pattern_object.create_shingles()
        for shingle in pattern_shingles:
            for text in self.canonical_text:
                search_object = BM_StringSearch(shingle)
                search_list = search_object.get_substring_bm_bad_character(
                    text)
                if search_list:
                    counter.append(search_list)
        return abs(1 - (len(counter)/len(pattern_shingles))) * 100, counter

    def search_plagiarism_BM_good(self) -> float:
        """
        Поиск плагиата с использованием алгоритма Бойера-Мура с эвристикой хорошего суффикса.

        Returns:
            float: Процент уникальности.
        """
        counter = []
        pattern_shingles = self.canonical_pattern_object.create_shingles()
        for shingle in pattern_shingles:
            for text in self.canonical_text:
                search_object = BM_StringSearch(shingle)
                search_list = search_object.get_substring_bm_good_suffix(text)
                if search_list:
                    counter.append(search_list)
        return abs(1 - (len(counter)/len(pattern_shingles))) * 100, counter
    

