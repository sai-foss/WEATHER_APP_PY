import reflex as rx

config = rx.Config(
    app_name="Flight_Analytics_App",
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://flight-analytics-app.onrender.com",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    show_built_with_reflex=False,
)
