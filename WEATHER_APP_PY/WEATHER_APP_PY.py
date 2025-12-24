import json

import reflex as rx

BORDER_GRADIENT = "linear-gradient(90deg, #73BCE3, #E37383)"

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
    months_back: int = 12

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


HORIZON_PRESETS = [
    (1, "1M"),
    (3, "3M"),
    (6, "6M"),
    (12, "1Y"),
    (24, "2Y"),
]


def gradient_border_card(*children: rx.Component, **props) -> rx.Component:
    bg = rx.color("gray", 2)
    return rx.box(
        *children,
        border="2px solid transparent",
        background=f"linear-gradient({bg}, {bg}) padding-box, {BORDER_GRADIENT} border-box",
        border_radius="14px",
        padding="1.25rem",
        **props,
    )


def airports_card() -> rx.Component:
    return gradient_border_card(
        rx.vstack(
            rx.heading("SOURCE AIRPORT", size="7", weight="bold"),
            rx.input(
                placeholder="e.g., SFO",
                value=RouteState.source_airport,
                on_change=RouteState.set_source_airport,
                width="100%",
                height="3rem",
                font_size="1.1rem",
            ),
            rx.box(height="0.75rem"),
            rx.heading("DESTINATION AIRPORT", size="7", weight="bold"),
            rx.input(
                placeholder="e.g., JFK",
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


def time_horizon_card() -> rx.Component:
    return gradient_border_card(
        rx.vstack(
            rx.heading("TIME HORIZON", size="7", weight="bold"),
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
                gap="1rem",
                flex_wrap="wrap",
            ),
            rx.hstack(
                rx.text("Months back", size="4", weight="medium"),
                rx.input(
                    type="number",
                    min="1",
                    step="1",
                    value=RouteState.months_back,
                    on_change=RouteState.set_months_back,
                    width="8rem",
                    height="2.5rem",
                ),
                spacing="3",
                align="center",
            ),
            spacing="4",
            align="stretch",
        ),
        width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
    )


def top_cards() -> rx.Component:
    return rx.flex(
        gradient_border_card(
            rx.heading("Delayed flight?", size="8", weight="bold"),
            width=rx.breakpoints(initial="100%", md="calc(50% - 0.5rem)"),
            text_align="center",
        ),
        gradient_border_card(
            rx.text(
                "Check route metrics and our predictions", size="6", weight="medium"
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
