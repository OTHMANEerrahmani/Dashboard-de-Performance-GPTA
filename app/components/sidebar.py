import reflex as rx
from app.states.gpta_state import (
    GptaState,
    ORGANS_LIST,
    OrganData,
)


def _render_sidebar_button(
    organ: OrganData,
) -> rx.Component:
    return rx.el.button(
        organ["name"],
        on_click=lambda: GptaState.select_organ(
            organ["id"]
        ),
        class_name=rx.cond(
            GptaState.selected_organ_id == organ["id"],
            "sidebar-button sidebar-button-active",
            "sidebar-button sidebar-button-inactive",
        ),
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.h2(
            "Organes du GPTA",
            class_name="text-lg font-semibold text-gray-100 mb-4 px-4 pt-4",
        ),
        rx.el.nav(
            rx.foreach(ORGANS_LIST, _render_sidebar_button),
            class_name="flex flex-col space-y-1",
        ),
        class_name="w-64 bg-indigo-900 text-white h-screen fixed top-0 left-0 shadow-lg pt-16",
    )