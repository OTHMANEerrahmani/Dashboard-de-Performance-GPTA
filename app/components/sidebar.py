import reflex as rx
from app.states.gpta_state import (
    GptaState,
    ORGANS_LIST,
    OrganData,
)


def _sidebar_nav_link(text: str, href: str) -> rx.Component:
    is_active = rx.State.router.page.path == href
    base_class = "block w-full text-left px-4 py-2.5 text-sm rounded-md transition-colors duration-150 ease-in-out "
    active_class = (
        base_class
        + "bg-indigo-700 text-white shadow-md font-semibold"
    )
    inactive_class = (
        base_class
        + "text-indigo-100 hover:bg-indigo-800 hover:text-white"
    )
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            is_active, active_class, inactive_class
        ),
    )


def _render_organ_button_dashboard(
    organ: OrganData,
) -> rx.Component:
    is_active = GptaState.selected_organ_id == organ["id"]
    active_class = (
        "sidebar-button sidebar-button-active font-medium"
    )
    inactive_class = (
        "sidebar-button sidebar-button-inactive"
    )
    return rx.el.button(
        organ["name"],
        on_click=lambda: GptaState.select_organ(
            organ["id"]
        ),
        class_name=rx.cond(
            is_active, active_class, inactive_class
        ),
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            _sidebar_nav_link("Accueil", "/home"),
            _sidebar_nav_link("Dashboard GPTA", "/"),
            class_name="p-4 space-y-2 border-b border-indigo-700",
        ),
        rx.el.h2(
            "Organes du GPTA",
            class_name="text-md font-semibold text-gray-200 mt-4 mb-2 px-4 pt-2",
        ),
        rx.el.nav(
            rx.foreach(
                ORGANS_LIST, _render_organ_button_dashboard
            ),
            class_name="flex flex-col space-y-1 px-2 pb-4",
        ),
        class_name="w-64 bg-indigo-900 text-white h-screen fixed top-0 left-0 shadow-lg pt-16 flex flex-col",
    )