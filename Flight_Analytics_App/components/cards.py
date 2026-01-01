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
    # have had to hardcode 90 here as the extent of the dataset
    (90, "MAX"),
]


# function to draw the airport card
def airports_card() -> rx.Component:
    return gradient_border_card(
        rx.vstack(
            rx.heading("Origin Airport", size="6"),
            rx.input(
                placeholder="e.g., ONT",
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
            rx.cond(
                # we can literally use the same pi chart flag for the network graph
                RouteState.show_pie_flag,  # wont run while false. the analyze button makes it true in the last line after validating inputs then we can run the rendering function
                rx.box(
                    rx.image(
                        src=RouteState.network_graph_src,  # weight of the edge in the network graph
                        width="100%",
                        height="auto",
                    )
                ),
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
                on_click=RouteState.analyze,  # we first checking input, Pi chart runs after yielding "success" after checking inputs
                variant="solid",
                border_radius="9999px",
                height="2.5rem",
                padding_x="1.25rem",
                spacing="3",
                align="stretch",
            ),
            # conditional rendering.
            rx.cond(
                # we make below variable available to the method? -> might be unnecessary
                RouteState.show_pie_flag,  # wont run while false. the analyze button makes it true in the last line after validating inputs then we can run the rendering function
                rx.recharts.pie_chart(
                    rx.recharts.pie(
                        data=RouteState.pie_data,
                        data_key="value",
                        name_key="name",
                        label=True,
                        padding_angle=5,
                    ),
                    rx.recharts.legend(),
                    width="100%",
                    height=350,
                ),
            ),
            spacing="3",
            align="stretch",
        ),
        width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
    )
