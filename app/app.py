import reflex as rx
from app.components.sidebar import sidebar
from app.components.main_content import main_content_area
from app.pages.home import home as home_page_func


def dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Dashboard Technique Interactif – GPTA",
                    class_name="text-2xl font-bold text-white",
                ),
                class_name="container mx-auto px-4 py-4 flex items-center justify-between",
            ),
            class_name="bg-indigo-800 shadow-md fixed top-0 left-0 right-0 z-50 h-16",
        ),
        rx.el.div(
            sidebar(),
            main_content_area(),
            class_name="flex flex-row",
        ),
        class_name="font-sans antialiased text-gray-900 bg-gray-100",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/style.css"],
)
app.add_page(dashboard_page, route="/")
app.add_page(home_page_func, route="/home")