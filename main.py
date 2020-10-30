from pathlib import Path
from notion.client import NotionClient
from notion.block import TodoBlock, PageBlock
import random as r



def unpack_words_file(path):
    with open(path, 'r', encoding='UTF-8') as words_file:
        words_list = words_file.read()
        words_list = words_list.split('\n')
        return words_list


def fill_to_do(stop_count, link):
    x = 0
    page = client.get_block(link)
    while x < stop_count:
        x += 1
        new_page = page.children.add_new(PageBlock, title=words_list[r.randint(1, 1500000)])
        new_page_link = new_page.get_browseable_url()
        page_to_fill = client.get_block(new_page_link)

        count_of_strings = 0
        one_string = ''

        while count_of_strings < r.randint(10, 20):
            count_of_strings += 1

            while x < r.randint(1, 10):
                one_string += words_list[r.randint(1, 1500000)] + ' '

            page_to_fill.children.add_new(TodoBlock, title=one_string)
            one_string = ''



client = NotionClient(
    token_v2="060fa7fee36649f13bf681e9b432a20f2df71fd68a1724b39c55d37ca4546c04c08e8fd79d4c85446be96257adcfb9d2c5f3924361b648691b38b8f6701ec2b474fbb8fa7c30e71be7c038c89a78")

words_list = unpack_words_file(Path('russian-words', 'russian.txt'))

fill_to_do(10, 'https://www.notion.so/To-do-9aaa96e7ef3c4a71a65cf5384e636a42')
