import reflex as rx

# variable we are using to design colored borders for all boxes in the app
BORDER_GRADIENT = "linear-gradient(90deg, #5b4e77, #55d6be)"

# variable we are using to design colored borders for all boxes in the app
DELAYED_BORDER_GRADIENT = "linear-gradient(90deg, #55d6be, #5b4e77)"


# function definition that draws the gradient for the "Delayed?" card. this UI element is refined as it utilizes the DELAYED_BORDER_GRADIENT macro to produce the reverse color scheme (or different color scheme)
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


# function to draw the gradient border for a card. this card is utilized for the remaining cards 
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
