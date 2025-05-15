import reflex as rx
from app.states.gpta_state import GptaState
from app.components.maintenance_history_table import (
    maintenance_history_table,
)
from app.components.metrics_display import metrics_display


def organ_detail_card() -> rx.Component:
    return rx.el.div(
        rx.cond(
            GptaState.selected_organ,
            rx.el.div(
                rx.el.h2(
                    GptaState.selected_organ["name"],
                    class_name="text-2xl font-bold text-indigo-700 mb-2",
                ),
                rx.el.p(
                    GptaState.selected_organ["function"],
                    class_name="text-md text-gray-600 mb-4",
                ),
                rx.el.image(
                    src=GptaState.selected_organ[
                        "image_url"
                    ],
                    alt=GptaState.selected_organ["name"],
                    class_name="w-full h-48 object-contain rounded-lg shadow-md mb-6 bg-gray-100 p-2",
                ),
                metrics_display(),
                maintenance_history_table(),
                class_name="p-6 bg-white rounded-xl shadow-xl",
            ),
            rx.el.div(
                rx.el.p(
                    "Veuillez sélectionner un organe pour afficher les détails.",
                    class_name="text-center text-gray-500 py-10",
                ),
                class_name="p-6 bg-white rounded-xl shadow-lg min-h-[300px] flex items-center justify-center",
            ),
        ),
        class_name="w-full",
    )