# its main.py but we putting all state and page (routing) stuff here

import reflex as rx

from .background.background import page_shell
from .components.cards import all_cards


def index() -> rx.Component:
    # page_shell the function we defined to first give us a background, takes a layout component-> rx.container
    #  as input which is again passed the all_cards() function that basically has all our UI components (cards, borders)
    # side note: toasts are defined in state as its interactive
    return page_shell(
        rx.container(
            all_cards(),
            size="4",  # making the main constraint of the page the max size
        )
    )


# below basically the entry point for the app

app = rx.App(theme=rx.theme(appearance="dark", has_background=False))
app.add_page(index)
