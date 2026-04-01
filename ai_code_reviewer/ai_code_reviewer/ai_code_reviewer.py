import reflex as rx
from .pages.index import index
from .pages.analyzer import analyzer
from .pages.about import about

FONT_URL = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Syne:wght@400;600;700;800&display=swap"

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="medium",
        accent_color="blue",
    ),
    stylesheets=[FONT_URL],
    style={
        "font_family": "'Syne', sans-serif",
        "background_color": "#0a0a0f",
        "margin": "0",
        "padding": "0",
    },
)

app.add_page(index, route="/")
app.add_page(analyzer, route="/analyzer")
app.add_page(about, route="/about")