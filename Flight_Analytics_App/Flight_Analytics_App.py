# its main.py but we putting all state and page (routing) stuff here

import reflex as rx

from .background.background import page_shell
from .components.cards import top_cards


def index() -> rx.Component:
    return page_shell(rx.box(top_cards(), padding="1.5rem"))


app = rx.App(theme=rx.theme(appearance="dark", has_background=False))
app.add_page(index)
