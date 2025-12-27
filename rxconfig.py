import reflex as rx

config = rx.Config(
    app_name="Flight_Analytics_App",
    api_url="https://flight-analytics-app.onrender.com:8000",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
