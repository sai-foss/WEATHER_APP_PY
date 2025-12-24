import reflex as rx

config = rx.Config(
    app_name="WEATHER_APP_PY",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)