import json
import os

from loguru import logger
from notifiers import get_notifier
from notion.block import PageBlock
from notion.client import NotionClient

# TODO: попробовать ориентироваться по последнему элементу
from py_files.some_functions import set_logger


# TODO: cкладывать все страницы в отдельный файлик
# TODO: постоянно перебирать страницы
# TODO: при появлении новой, обновляем файлик, складываем в него новую страницу, ее же отправляем в хром-плагин
# TODO: пройтись одним циклом, собрав все страницы для первичного добавления в закладки
# TODO: отслеживать появление новых страниц
# TODO: отслеживать изменения ссылок существующий страниц
# TODO: попробовать пройти хотя бы одну цепочку до конца
# TODO: доходим до самого нижнего уровня, потом уже начинаем двигаться обратно


def get_childs(page):
    children_pages = page.children.filter(type=PageBlock)
    return children_pages


def get_key(dict):
    key = [key for key in dict.keys()][0]
    return key


def compare_depth_to_length(depth):
    if len(get_key(path[-1]).split("/")) < depth + 1:
        return 'depth_more_than_length'

    elif len(get_key(path[-1]).split("/")) == depth + 1:
        return 'length_and_depth_are_equal'

    else:
        return 'length_more_than_depth'


# TODO: переименовать
def recursively_print_titles(block, depth=0, file=None):
    if depth == 0:
        path.append({block.title: block.get_browseable_url()})
    else:

        # TODO: cделать словарь с тем, что будем аппендить
        # TODO: добавить именованный аргумент для проверки различий между файлами
        # TODO: структура массива должна быть другой. name: 'name', url: 'url'
        # TODO: прихуярить уведомление в тг о вновь созданной странице

        _dict = {
            'depth_more_than_length': {f'{get_key(path[-1])}/{block.title}': block.get_browseable_url()},
            'length_and_depth_are_equal': {
                f"{'/'.join(get_key(path[-1]).split('/')[0:-1])}/{block.title}": block.get_browseable_url()},
            'length_more_than_depth': {
                f"{'/'.join(get_key(path[-1]).split('/')[0:depth])}/{block.title}": block.get_browseable_url()}
        }

        page_name_and_bread_crumbs = _dict[compare_depth_to_length(depth)]
        page_name = get_key(page_name_and_bread_crumbs)
        path.append(page_name_and_bread_crumbs)

        if not page_name in pages_names_from_file_data:
            logger.critical(get_key(page_name_and_bread_crumbs))

            telegram = get_notifier('telegram')
            telegram.notify(
                message=get_key(page_name_and_bread_crumbs), token=os.environ['TELEGRAM_KEY'], chat_id=199965889)

            new_pages.append(page_name_and_bread_crumbs)
            # TODO: cделать нормально елоггирование и подсчет страниц
            # TODO: создать массив значений, которые не существовали ранее
            # TODO: !!!После завершения!!! цикла поиска страниц заново сдампить file
            # TODO:  Отправить новые страницы на добавление в Chrome

    for child in block.children:
        if child.type in ["page", "collection"]:
            recursively_print_titles(child, depth=depth + 1)


# TODO: должно быть два файла: один для однократного парсинга и вывода в json, второй - для перманентного чекинга

if __name__ == '__main__':

    set_logger()

    while True:
        with open('notion_pages_for_tracking.json') as file:
            file_data = json.load(file)

        pages_names_from_file_data = [get_key(page) for page in file_data]

        client = NotionClient(token_v2=os.environ.get('TOKEN'))
        link = os.environ['LINK']
        page = client.get_block(link)
        child_pages = get_childs(page)
        path = []
        new_pages = []

        for block in child_pages:
            recursively_print_titles(block)

        with open('/home/valera/PycharmProjects/keep_transfer/notion_pages_for_tracking.json', 'w') as file:
            json.dump(path, file, ensure_ascii=False, indent=4)

        # TODO: возможно эту часть можно перенести выше, чтоб после обнаружения файлы перезапись шла сразу
        with open('/home/valera/PycharmProjects/keep_transfer/new_pages.json', 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            print(file_data)
            print(file_data == True)

        with open('/home/valera/PycharmProjects/keep_transfer/new_pages.json', 'w') as file:
            if file_data:
                json.dump(file_data + new_pages, file, ensure_ascii=False, indent=4)

            else:
                json.dump(new_pages, file, ensure_ascii=False, indent=4)

        logger.debug('Цикл завершен')
