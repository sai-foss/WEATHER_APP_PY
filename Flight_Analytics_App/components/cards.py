import reflex as rx

from ..data.airport_list import AIRPORT_DATALIST_ID
from ..state import RouteState

from .gradients import delayed_gradient_border_card, gradient_border_card


# tooltip for mobile


def tip_button(
    label: str,
    content: str,
    color: str = "blue",
    variant: str = "soft",
) -> rx.Component:
    def make_btn():
        return rx.button(label, variant=variant, size="3", color_scheme=color)

    desktop_btn = make_btn()
    mobile_btn = make_btn()

    desktop = rx.box(
        rx.hover_card.root(
            rx.hover_card.trigger(desktop_btn),
            rx.hover_card.content(
                rx.text(
                    content,
                    size="4",
                    line_height="1",
                    weight="medium",
                ),
                side="top",
                align="center",
                size="1",  # hovercard padding scale
                style={"max_width": "25rem"},
            ),
        ),
        display=rx.breakpoints(initial="none", md="block"),
    )

    mobile = rx.box(
        rx.popover.root(
            rx.popover.trigger(mobile_btn),
            rx.popover.content(
                rx.text(
                    content,
                    size="5",
                    line_height="1",
                    weight="medium",
                ),
                side="top",
                align="center",
                padding="1rem",
                style={"max_width": "25rem"},
            ),
        ),
        display=rx.breakpoints(initial="block", md="none"),
    )

    return rx.box(desktop, mobile)


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
                "Check route metrics and weather information",
                size="6",
            ),
            width=rx.breakpoints(initial="100%", md="50%"),
            text_align="center",
        ),
        airports_card(),
        time_horizon_card(),
        # new weather cards
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
            rx.hstack(
                rx.heading("Origin Airport", size="6"),
                rx.icon(tag="plane_takeoff"),
                width="100%",
                justify="between",
                align="center",
            ),
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
            rx.hstack(
                rx.heading("Destination Airport", size="6"),
                rx.icon(tag="plane_landing"),
                width="100%",
                justify="between",
                align="center",
            ),
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
                    rx.vstack(
                        rx.image(
                            src=RouteState.network_graph_src,  # weight of the edge in the network graph
                            width="100%",
                            height="auto",
                        ),
                        # CURRENT WEATHER  here, FORECAST in TIME HORIZON CARD, uses the show_pie_flag to render
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading("Current Weather status", size="6"),
                                    rx.spacer(),
                                    rx.icon(tag="cloud_sun_rain"),
                                    width="100%",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.card(
                                        rx.text(RouteState.source_airport),
                                    ),
                                    rx.hstack(
                                        tip_button(
                                            RouteState.source_fltCat,
                                            RouteState.source_weather_explanation,
                                            RouteState.source_card_color,  # keep an eye on the color it might work (yet)
                                        ),
                                        rx.icon(tag="pointer"),
                                    ),
                                    width="100%",
                                    align="center",
                                    justify="between",
                                ),
                                rx.hstack(
                                    rx.card(
                                        rx.text(RouteState.dest_airport),
                                    ),
                                    rx.hstack(
                                        tip_button(
                                            RouteState.dest_fltCat,
                                            RouteState.dest_weather_explanation,
                                            RouteState.dest_card_color,
                                        ),
                                        rx.icon(tag="pointer"),
                                    ),
                                    width="100%",
                                    align="center",
                                    justify="between",
                                ),
                                spacing="3",
                                width="100%",
                                align="stretch",
                            ),
                            width="100%",
                        ),
                    ),
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
            rx.hstack(
                rx.heading("Time Horizon", size="6"),
                rx.icon(tag="calendars"),
                width="100%",
                justify="between",
                align="center",
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
                        outer_radius="73%",  # adhoc tweak
                        data_key="value",
                        stroke="transparent",  # removes the black borders
                        name_key="name",
                        label=True,
                        padding_angle=5,
                        label_line=False,
                    ),
                    rx.recharts.legend(),
                    width="100%",
                    height=300,
                ),
            ),
            spacing="3",
            align="stretch",
        ),
        width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
    )
