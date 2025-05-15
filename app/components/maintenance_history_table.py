import reflex as rx
from app.states.gpta_state import GptaState


def maintenance_history_table_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "🗓️ Historique d'interventions de maintenance",
                class_name="text-lg font-semibold text-gray-700 mb-3",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Date",
                            class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Durée (h)",
                            class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Action",
                            class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Remarques",
                            class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        GptaState.current_organ_interventions,
                        lambda item: rx.el.tr(
                            rx.el.td(
                                item["date"],
                                class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                item["type"],
                                class_name=rx.cond(
                                    item["type"]
                                    == "Corrective",
                                    "px-3 py-2 whitespace-nowrap text-sm text-red-600 font-medium",
                                    "px-3 py-2 whitespace-nowrap text-sm text-gray-600",
                                ),
                            ),
                            rx.el.td(
                                item[
                                    "duration_h"
                                ].to_string(),
                                class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-600 text-center",
                            ),
                            rx.el.td(
                                item["action"],
                                class_name="px-3 py-2 text-sm text-gray-600",
                            ),
                            rx.el.td(
                                item["remarks"],
                                class_name="px-3 py-2 text-sm text-gray-600",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50",
                        ),
                    ),
                    rx.cond(
                        GptaState.current_organ_interventions.length()
                        == 0,
                        rx.el.tr(
                            rx.el.td(
                                "Aucune intervention pour cet organe.",
                                col_span=5,
                                class_name="px-3 py-3 text-center text-gray-500",
                            )
                        ),
                        rx.fragment(),
                    ),
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="shadow border border-gray-200 rounded-lg overflow-x-auto",
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )