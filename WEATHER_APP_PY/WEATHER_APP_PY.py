import json

import reflex as rx

# function we are using to create colored borders for all boxes in the app
BORDER_GRADIENT = "linear-gradient(90deg, #5b4e77, #55d6be)"
DELAYED_BORDER_GRADIENT = "linear-gradient(90deg, #55d6be, #5b4e77)"  # example


# the particles packed is being brought in via npm's CDN
PARTICLES_CDN = "https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"

PARTICLES_CONFIG = {
    "particles": {
        "number": {"value": 120, "density": {"enable": True, "value_area": 900}},
        "color": {"value": "#ffffff"},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.5},
        "size": {"value": 2, "random": True},
        "line_linked": {
            "enable": True,
            "distance": 140,
            "color": "#ffffff",
            "opacity": 0.5,
            "width": 2,
        },
        "move": {"enable": True, "speed": 0.2},
    },
    "interactivity": {
        "events": {
            "onhover": {"enable": False},
            "onclick": {"enable": False},
            "resize": True,
        }
    },
    "retina_detect": True,
}


class RouteState(rx.State):
    source_airport: str = ""
    dest_airport: str = ""
    months_back: int = 3

    def set_source_airport(self, value: str):
        self.source_airport = (value or "").upper().strip()

    def set_dest_airport(self, value: str):
        self.dest_airport = (value or "").upper().strip()

    def set_months_back(self, value: str):
        try:
            v = int(value)
        except (TypeError, ValueError):
            return

        self.months_back = max(1, v)

    # method to trigger analysis pipeline here, its empty for now
    def analyze(self):
        pass


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


def delayed_gradient_border_card(*children: rx.Component, **props) -> rx.Component:
    bg = rx.color("gray", 2)
    return rx.box(
        *children,
        border="2px solid transparent",
        background=f"linear-gradient({bg}, {bg}) padding-box, {DELAYED_BORDER_GRADIENT} border-box",
        border_radius="14px",
        padding="1.25rem",
        **props,
    )


# function to draw the gradient border on all the top level box then have child boxes inherit that
def gradient_border_card(*children: rx.Component, **props) -> rx.Component:
    bg = rx.color("gray", 2)
    return rx.box(
        *children,
        border="2px solid transparent",
        # default accent for cards
        background=f"linear-gradient({bg}, {bg}) padding-box, {BORDER_GRADIENT} border-box",
        border_radius="14px",
        padding="1.25rem",
        **props,
    )


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
                        on_click=RouteState.set_months_back(str(months)),
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
                gap="0.8rem",  # reduces the gap between the times (1M, 3M, 6M ...)
                flex_wrap="wrap",
                justify="center",
                align="center",
                width="100%",
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


# first 2 cards the introduction type
def top_cards() -> rx.Component:
    return rx.flex(
        delayed_gradient_border_card(
            rx.heading("Delayed flight?", size="8"),
            width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
            text_align="center",
        ),
        gradient_border_card(
            rx.heading(
                "Check route metrics and our predictions",
                size="6",
            ),
            width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
            text_align="center",
        ),
        airports_card(),
        time_horizon_card(),
        width="100%",
        max_width="72rem",
        margin_x="auto",
        gap="1rem",
        flex_wrap="wrap",
        align="stretch",
        justify="center",
    )


# render the particles
def particles_background() -> rx.Component:
    cfg = json.dumps(PARTICLES_CONFIG)

    return rx.fragment(
        rx.box(
            id="particles-js",
            position="fixed",
            top="0",
            right="0",
            bottom="0",
            left="0",
            z_index="-1",
            pointer_events="none",
        ),
        rx.script(src=PARTICLES_CDN),
        rx.script(
            f"""
(function initParticles() {{
  const cfg = {cfg};
  function start() {{
    const el = document.getElementById("particles-js");
    if (!el || !window.particlesJS) return false;
    if (el.getAttribute("data-initialized") === "1") return true;
    window.particlesJS("particles-js", cfg);
    el.setAttribute("data-initialized", "1");
    return true;
  }}
  if (start()) return;
  let tries = 0;
  const t = setInterval(() => {{
    if (start() || ++tries > 50) clearInterval(t);
  }}, 100);
}})();
"""
        ),
    )


def page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        particles_background(),
        rx.box(
            *children,
            position="relative",
            z_index="0",
            min_height="100vh",
            width="100%",
        ),
        position="relative",
        width="100%",
    )


def index() -> rx.Component:
    return page_shell(rx.box(top_cards(), padding="1.5rem"))


app = rx.App(theme=rx.theme(appearance="dark", has_background=False))
app.add_page(index)
