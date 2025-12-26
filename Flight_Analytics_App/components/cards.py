import reflex as rx

from ..data.airport_list import AIRPORT_DATALIST_ID
from ..state import RouteState
from .gradients import delayed_gradient_border_card, gradient_border_card


# display all our "cards"
# returns an rx component -> flex which contains the 4 cards (+ their border components)
# This finally gets passed into page_shell function (the background function) right before
# getting returned into the index() to get displayed
def all_cards() -> rx.Component:
    return rx.flex(
        # this implementation has a downside of the borders gradients width being the controller for
        # the cards width and breakpoints for md
        # card to get "delayed Flight" (defined below)
        delayed_gradient_border_card(
            rx.heading("Delayed flight?", size="8"),
            width=rx.breakpoints(initial="100%", md="50%"),
            text_align="center",
        ),
        gradient_border_card(
            # card to get the top right text
            rx.heading(
                "Check route metrics and our predictions",
                size="6",
            ),
            width=rx.breakpoints(initial="100%", md="50%"),
            text_align="center",
        ),
        airports_card(),
        time_horizon_card(),
        width="100%",
        max_width="72rem",
        margin_top=rx.breakpoints(initial="1rem", md="2rem"),
        margin_x="auto",
        gap="1rem",
        flex_wrap="wrap",
        align="stretch",
        justify="center",
    )


HORIZON_PRESETS = [
    (1, "1M"),
    (3, "3M"),
    (6, "6M"),
    (12, "1Y"),
    (24, "2Y"),
    # have had to hardcode 96 here as the extent of the dataset (will have 96 months available soon,)
    # otherwise its 90 as the dataset only has until half of this year
    (96, "MAX"),
]


# function to draw the airport card
def airports_card() -> rx.Component:
    return gradient_border_card(
        rx.vstack(
            rx.heading("Origin Airport", size="6"),
            rx.input(
                placeholder="e.g., LAX",
                value=RouteState.source_airport,
                on_change=RouteState.set_source_airport,
                width="100%",
                height="3rem",
                font_size="1.1rem",
                max_length=3,
                pattern="[A-Za-z]{3}",
                list=AIRPORT_DATALIST_ID,
            ),
            rx.box(height="0.75rem"),
            rx.heading("Destination Airport", size="6"),
            rx.input(
                placeholder="e.g., DFW",
                value=RouteState.dest_airport,
                on_change=RouteState.set_dest_airport,
                width="100%",
                height="3rem",
                font_size="1.1rem",
                max_length=3,
                pattern="[A-Za-z]{3}",
                list=AIRPORT_DATALIST_ID,
            ),
            spacing="3",
            align="stretch",
        ),
        width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
    )


# function to draw the time horizon card
def time_horizon_card() -> rx.Component:
    return gradient_border_card(
        rx.vstack(
            rx.heading(
                "Time Horizon",
                size="6",
                text_align="center",
            ),
            rx.flex(
                *[
                    rx.button(
                        label,
                        on_click=RouteState.set_months_back(months),
                        variant=rx.cond(
                            RouteState.months_back == months,
                            "solid",
                            "outline",
                        ),
                        border_radius="9999px",
                        height="2.5rem",
                        padding_x="1.1rem",
                    )
                    for months, label in HORIZON_PRESETS
                ],
                gap="1rem",  # reduces the gap between the times (1M, 3M, 6M ...)
                flex_wrap="wrap",
                justify="center",
            ),
            # analyze button
            rx.box(height="1rem"),
            rx.button(
                rx.heading("Analyze", size="6"),
                on_click=RouteState.analyze,  # add this handler in RouteState
                variant="solid",
                border_radius="9999px",
                height="2.5rem",
                padding_x="1.25rem",
                spacing="3",
                align="stretch",
            ),
            spacing="3",
            align="stretch",
        ),
        width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
    )
