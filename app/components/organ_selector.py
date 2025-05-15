import reflex as rx
from app.states.gpta_state import GptaState, OrganData


def _render_organ_option(organ: OrganData) -> rx.Component:
    return rx.el.option(organ["name"], value=organ["id"])


def organ_selector() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Sélectionner un organe:",
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.select(
            rx.el.option(
                "--- Choisir un organe ---", value=""
            ),
            rx.foreach(
                GptaState.organs, _render_organ_option
            ),
            value=GptaState.selected_organ_id,
            on_change=GptaState.select_organ,
            class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 bg-white",
        ),
        class_name="p-4 bg-gray-50 rounded-lg shadow",
    )