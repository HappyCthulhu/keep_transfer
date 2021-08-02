import json

from notion.block import PageBlock
from notion.client import NotionClient
import os

# TODO: пройтись одним циклом, собрав все страницы для первичного добавления в закладки
# TODO: отслеживать появление новых страниц
# TODO: отслеживать изменения ссылок существующий страниц
# TODO: попробовать пройти хотя бы одну цепочку до конца
# TODO: доходим до самого нижнего уровня, потом уже начинаем двигаться обратно
# TODO: склонировать эту репу заново (по ssh, а не http)



# TODO: попробовать ориентироваться по последнему элементу

def get_childs(page):
    children_pages = page.children.filter(type=PageBlock)
    return children_pages

def get_key(dict):
    key = [key for key in dict.keys()][0]
    return key


def recursively_print_titles(block, depth=0):
    if depth == 0:
        path.append({block.title: block.get_browseable_url()})
    else:
        # Все нахер порушится из-за того, что глубина отличается не на 1 значение
        print(f'Название блока: {block.title}')
        print(f'Глубина: {depth + 1}')
        print(f'Длинна последнего элемента: {len(get_key(path[-1]).split("/"))}')

        if len(get_key(path[-1]).split("/")) < depth + 1:
            print('Глубина больше длинны')
            path.append({
                f'{get_key(path[-1])}/{block.title}': block.get_browseable_url()
            })

        elif len(get_key(path[-1]).split("/")) == depth + 1:
            print('Глубина равна длинне')
            path.append({
                f"{'/'.join(get_key(path[-1]).split('/')[0:-1])}/{block.title}": block.get_browseable_url()
            })

        else:
            print('Глубина меньше длинны')
            path.append({
                f"{'/'.join(get_key(path[-1]).split('/')[0:depth])}/{block.title}": block.get_browseable_url()
            })


    with open('/home/valera/PycharmProjects/keep_transfer/notion_pages.json', 'w') as file:
        json.dump(path, file, ensure_ascii=False, indent=4)

    print(f'Путь: {path[-1]}\n')
    for child in block.children:
        if child.type in ["page", "collection"]:
            # print(child.title)
            recursively_print_titles(child, depth=depth + 1)


client = NotionClient(
    token_v2=os.environ['TOKEN'])

link = os.environ['LINK']
page = client.get_block(link)
child_pages = get_childs(page)


path = []

for block in child_pages:
    recursively_print_titles(block)

print('Готово')