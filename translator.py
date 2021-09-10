import requests
from bs4 import BeautifulSoup
import sys


class Languages:
    data = (
        'arabic',
        'german',
        'english',
        'spanish',
        'french',
        'hebrew',
        'japanese',
        'dutch',
        'polish',
        'portuguese',
        'romanian',
        'russian',
        'turkish'
    )


class RequestData:
    def __init__(self, words, phrases_source, phrases_target):
        self.words = words
        self.phrases_source = phrases_source
        self.phrases_target = phrases_target


def send_request(session, from_language, to_language, w):
    url = 'https://context.reverso.net/translation/'
    url += f'{from_language}-{to_language}/'
    url += word
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = session.get(url, headers=headers)
    if request.status_code == 404:
        print(f'Sorry, unable to find {w}')
        exit(0)
    if request.status_code != 200:
        print('Something wrong with your internet connection')
        exit(0)
    return request


def get_text(elements_list):
    return [el.text.strip() for el in filter(lambda x: x is not None, elements_list)]


def get_request_data(request):
    soup = BeautifulSoup(request.content, 'html.parser')
    words = soup.find_all('a', class_='translation')
    words_list = list(map(lambda x: x.text.strip(), words))
    phrases_source = [el.find('span', class_='text') for el in soup.find_all('div', class_=f'src')]
    phrases_target = [el.find('span', class_='text') for el in soup.find_all('div', class_=f'trg')]
    return RequestData(words_list, get_text(phrases_source), get_text(phrases_target))


def print_to_file(file, text=''):
    file.write(f'{text}\n')
    print(text)


def check_language(lang):
    if lang not in Languages.data and lang != 'all':
        print(f"Sorry, the program doesn't support {lang}")
        exit(0)


def check_words(words, w):
    if len(words) <= 1:
        print(f'Sorry, unable to find {w}')
        exit(0)


if __name__ == '__main__':
    from_lang = sys.argv[1]
    check_language(from_lang)

    all_languages = False
    to_lang = sys.argv[2]
    check_language(to_lang)
    if to_lang == 'all':
        all_languages = True

    word = sys.argv[3]

    my_session = requests.Session()
    with open(f'{word}.txt', mode='w', encoding='utf-8') as my_file:
        if all_languages:
            for language in Languages.data:
                if from_lang != language:
                    my_request = send_request(my_session, from_lang, language, word)
                    request_data = get_request_data(my_request)

                    check_words(request_data.words, word)

                    print_to_file(my_file, f'{language} Translations:')
                    print_to_file(my_file, request_data.words[1])
                    print_to_file(my_file)
                    print_to_file(my_file, f'{language} Example:')
                    print_to_file(my_file, request_data.phrases_source[0])
                    print_to_file(my_file, request_data.phrases_target[0])
                    print_to_file(my_file)
                    print_to_file(my_file)
        else:
            my_request = send_request(my_session, from_lang, to_lang, word)
            request_data = get_request_data(my_request)

            check_words(request_data.words, word)

            print_to_file(my_file, f'{to_lang} Translations:')
            for word in request_data.words[1:6]:
                print_to_file(my_file, word)
            print_to_file(my_file)
            print_to_file(my_file, f'{to_lang} Examples:')
            for i in range(5):
                print_to_file(my_file, request_data.phrases_source[i])
                print_to_file(my_file, request_data.phrases_target[i])
                print_to_file(my_file)
