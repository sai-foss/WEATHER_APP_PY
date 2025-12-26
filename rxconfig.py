import reflex as rx

config = rx.Config(
    app_name="Flight_Analytics_App",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
