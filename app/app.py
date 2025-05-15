import reflex as rx
from app.states.gpta_state import GptaState
from app.components.organ_selector import organ_selector
from app.components.organ_detail_card import (
    organ_detail_card,
)


def index() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.h1(
                "Dashboard de Performance du Système GPTA",
                class_name="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 py-4 text-center",
            ),
            class_name="bg-white shadow-md mb-6",
        ),
        rx.el.main(
            rx.el.div(
                organ_selector(),
                organ_detail_card(),
                class_name="max-w-6xl mx-auto p-4 space-y-6",
            )
        ),
        class_name="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-indigo-100",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)