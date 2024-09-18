import os

file = os.path.join(r'C:\Users\Public\python\skypro_diploma\advertisement\services', 'words.txt')
bad_words = []


def return_bad_words():
    """Функция для извлечения слов из файла"""
    with open(file) as f:
        words = f.readlines()
        for word in words:
            w = word.replace('\n', '')
            bad_words.append(w)
        return bad_words
