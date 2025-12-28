# its main.py but we putting all state and page (routing) stuff here

import reflex as rx
import reflex_enterprise as rxe

from .background.background import page_shell
from .components.cards import all_cards
from .data.database import sql_output


def index() -> rx.Component:
    # page_shell the function we defined to first give us a background, takes a layout component-> rx.container
    #  as input which is again passed the all_cards() function that basically has all our UI components (cards, borders)
    # side note: toasts are defined in state as its interactive
    return rx.container(
        page_shell(
            rx.container(
                all_cards(),
                size="4",  # making the main constraint of the page the max size
            )
        ),
        ## we are testing if we can access the database on render cloud. expecting 2018 as a string output in console.log
        rx.button("Log", on_click=rx.console_log(sql_output[0][0])),
    )


# below is basically the entry point for the app
# removed "theme" setup. dark mode only
app = rxe.App()
app.add_page(index)
