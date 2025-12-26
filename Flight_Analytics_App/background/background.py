import reflex as rx

from ..data.airport_list import airport_datalist
from .particles import particles_background


# function to render background: particles.js + image
def page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        particles_background(),
        rx.box(
            airport_datalist(),  # add this once
            *children,
            position="relative",
            z_index="0",
            min_height="100vh",
            width="100%",
            background_image="url('./theme_type.svg')",
            background_repeat="no-repeat",
            background_size="cover",
            background_position="center",
        ),
        position="relative",
        width="100%",
    )
