import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

import django  # noqa
django.setup()

from apps.core.models import Item, Price, Goal  # noqa


def create_or_update_item(name, image):
    i = Item.objects.filter(name=name).first()  # noqa
    if not i:
        Item.objects.create(name=name, image=image)  # noqa
    else:
        i.image = image
        i.save()


def create_or_update_price(item_name, buyer, seller):
    p = Price.objects.filter(item__name=item_name).first()  # noqa
    if not p:
        i = Item.objects.get(name=item_name)  # noqa
        Price.objects.create(item=i, buyer=buyer, seller=seller)  # noqa
    else:
        p.buyer = buyer
        p.seller = seller
        p.save()


def create_or_update_goal(difficulty, balance, rank, items):
    g = Goal.objects.filter(difficulty=difficulty).first()  # noqa
    if not g:
        Goal.objects.create(difficulty=difficulty, balance=balance, rank=rank, json=items)  # noqa
    else:
        g.balance = balance
        g.rank = rank
        g.json = items
        g.save()


def populate():
    for key, value in {
        'Apple': os.path.join('items', 'apple.png'),
        'Aubergine': os.path.join('items', 'aubergine.png'),
        'Banana': os.path.join('items', 'banana.png'),
        'Broccoli': os.path.join('items', 'broccoli.png'),
        'Cabbage': os.path.join('items', 'cabbage.png'),
        'Carrot': os.path.join('items', 'carrot.png'),
        'Cherries': os.path.join('items', 'cherries.png'),
        'Corn': os.path.join('items', 'corn.png'),
        'Cucumber': os.path.join('items', 'cucumber.png'),
        'Garlic': os.path.join('items', 'garlic.png'),
        'Grapes': os.path.join('items', 'grapes.png'),
        'Hazelnut': os.path.join('items', 'hazelnut.png'),
        'Orange': os.path.join('items', 'orange.png'),
        'Peach': os.path.join('items', 'peach.png'),
        'Pear': os.path.join('items', 'pear.png'),
        'Pineapple': os.path.join('items', 'pineapple.png'),
        'Pistachio': os.path.join('items', 'pistachio.png'),
        'Pomegranate': os.path.join('items', 'pomegranate.png'),
        'Potatoes': os.path.join('items', 'potatoes.png'),
        'Radish': os.path.join('items', 'radish.png'),
        'Raspberry': os.path.join('items', 'raspberry.png'),
        'Salad': os.path.join('items', 'salad.png'),
        'Strawberry': os.path.join('items', 'strawberry.png'),
        'Tomato': os.path.join('items', 'tomato.png'),
        'Watermelon': os.path.join('items', 'watermelon.png'),
    }.items():
        create_or_update_item(key, value)

    for key, value in {
        'Apple': (9, 4),
        'Aubergine': (28, 23),
        'Banana': (18, 13),
        'Broccoli': (104, 99),
        'Cabbage': (12, 7),
        'Carrot': (9, 4),
        'Cherries': (33, 28),
        'Corn': (19, 14),
        'Cucumber': (32, 27),
        'Garlic': (25, 20),
        'Grapes': (35, 30),
        'Hazelnut': (125, 120),
        'Orange': (21, 16),
        'Peach': (12, 7),
        'Pear': (17, 12),
        'Pineapple': (124, 119),
        'Pistachio': (91, 86),
        'Pomegranate': (25, 20),
        'Potatoes': (11, 6),
        'Radish': (13, 8),
        'Raspberry': (205, 200),
        'Salad': (68, 63),
        'Strawberry': (105, 100),
        'Tomato': (35, 30),
        'Watermelon': (16, 11),
    }.items():
        buyer, seller = value
        create_or_update_price(key, buyer, seller)

    for obj in (
        (1, 8, 'rookie', DIFFICULTY_FIRST_WITH_DISTRACTORS),          # Sell: Apple, Carrot
        (2, 12, 'experienced', DIFFICULTY_SECOND_WITH_DISTRACTORS),   # Buy: Carrot. Sell: Cabbage, Potatoes
        (3, 189, 'professional', DIFFICULTY_THIRD_WITH_DISTRACTORS),  # Buy: Cabbage, Potatoes. Sell: Raspberry
    ):
        difficulty, balance, rank, items = obj
        create_or_update_goal(difficulty, balance, rank, items)


DIFFICULTY_FIRST = {'items': {
    'seller': [
        {'name': 'apple'},
        {'name': 'carrot'},
    ],
}}

DIFFICULTY_FIRST_WITH_DISTRACTORS = {'items': {
    'seller': [
        *DIFFICULTY_FIRST.get('items', {}).get('seller', []),
    ],
    'buyer': [
        *DIFFICULTY_FIRST.get('items', {}).get('buyer', []),
        {'name': 'orange'},
    ]
}}

DIFFICULTY_SECOND = {'items': {
    'buyer': [
        {'name': 'carrot'},
    ],
    'seller': [
        {'name': 'cabbage'},
        {'name': 'potatoes'},
    ],
}}

DIFFICULTY_SECOND_WITH_DISTRACTORS = {'items': {
    'seller': [
        *DIFFICULTY_SECOND.get('items', {}).get('seller', []),
    ],
    'buyer': [
        *DIFFICULTY_SECOND.get('items', {}).get('buyer', []),
        {'name': 'orange'},
    ]
}}

DIFFICULTY_THIRD = {'items': {
    'buyer': [
        {'name': 'cabbage'},
        {'name': 'potatoes'},
    ],
    'seller': [
        {'name': 'raspberry'},
    ],
}}

DIFFICULTY_THIRD_WITH_DISTRACTORS = {'items': {
    'seller': [
        *DIFFICULTY_THIRD.get('items', {}).get('seller', []),
    ],
    'buyer': [
        *DIFFICULTY_THIRD.get('items', {}).get('buyer', []),
        {'name': 'orange'},
    ]
}}

DIFFICULTIES = [
    DIFFICULTY_FIRST,
    DIFFICULTY_SECOND,
    DIFFICULTY_THIRD,
]

if __name__ == '__main__':
    populate()
