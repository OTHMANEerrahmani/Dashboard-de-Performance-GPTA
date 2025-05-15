import reflex as rx
from app.states.gpta_state import GptaState
from app.components.maintenance_history_table import (
    maintenance_history_table_component,
)


def _metric_card(
    icon: str,
    title: str,
    value: rx.Var | str,
    unit: str = "",
    card_class: str = "bg-sky-50 border-sky-200",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(icon, class_name="text-2xl mr-3"),
            rx.el.h4(
                title,
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="flex items-center mb-1",
        ),
        rx.el.p(
            value,
            rx.el.span(
                f" {unit}",
                class_name="text-xs text-gray-500",
            ),
            class_name="text-2xl font-semibold text-gray-800",
        ),
        class_name=f"p-4 rounded-lg shadow border {card_class}",
    )


def _slider_component(
    label: str,
    current_value_display: rx.Var | str,
    min_val: int,
    max_val: int,
    step: int,
    slider_value_state: rx.Var,
    on_change_event: rx.event.EventHandler,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            f"{label}: ",
            rx.el.span(
                current_value_display,
                class_name="font-semibold text-indigo-700",
            ),
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.input(
            type="range",
            min_=min_val,
            max_=max_val,
            step=step,
            on_change=on_change_event,
            class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600",
            default_value=slider_value_state,
        ),
        rx.el.div(
            rx.el.span(
                min_val, class_name="text-xs text-gray-500"
            ),
            rx.el.span(
                max_val, class_name="text-xs text-gray-500"
            ),
            class_name="flex justify-between mt-1",
        ),
    )


def main_content_area() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.cond(
                GptaState.selected_organ,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "⚙️ Fiche : ",
                            rx.el.span(
                                GptaState.selected_organ[
                                    "name"
                                ],
                                class_name="text-indigo-700",
                            ),
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            GptaState.selected_organ[
                                "function"
                            ],
                            class_name="text-md text-gray-600 mt-1",
                        ),
                        class_name="mb-6 pb-4 border-b border-gray-200",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.image(
                                    src=GptaState.selected_organ[
                                        "image_url"
                                    ],
                                    alt=GptaState.selected_organ[
                                        "name"
                                    ],
                                    class_name="w-full h-auto max-h-60 object-contain rounded-md",
                                ),
                                class_name="bg-white p-4 rounded-lg shadow mb-6 border border-gray-200",
                            ),
                            maintenance_history_table_component(),
                            class_name="flex flex-col space-y-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "📊 Indicateurs de Performance",
                                    class_name="text-lg font-semibold text-gray-700 mb-3",
                                ),
                                rx.el.div(
                                    _metric_card(
                                        "⏱️",
                                        "MTBF",
                                        GptaState.mtbf,
                                        "h",
                                        "bg-blue-50 border-blue-200",
                                    ),
                                    _metric_card(
                                        "🛠️",
                                        "MTTR",
                                        GptaState.mttr,
                                        "h",
                                        "bg-orange-50 border-orange-200",
                                    ),
                                    _metric_card(
                                        "📉",
                                        "λ (Lambda)",
                                        GptaState.lambda_rate_display,
                                        "h⁻¹",
                                        "bg-purple-50 border-purple-200",
                                    ),
                                    _metric_card(
                                        "✅",
                                        "Disponibilité",
                                        GptaState.availability_display,
                                        "",
                                        "bg-green-50 border-green-200",
                                    ),
                                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                                ),
                                class_name="bg-white p-4 rounded-lg shadow mb-6",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "🔧 Fiabilité et Maintenance préventive",
                                    class_name="text-lg font-semibold text-gray-700 mb-3",
                                ),
                                _slider_component(
                                    "Durée de fonctionnement (t)",
                                    GptaState.t_slider_value.to_string()
                                    + " h",
                                    0,
                                    5000,
                                    50,
                                    GptaState.t_slider_value,
                                    GptaState.set_t_slider_value,
                                ),
                                _metric_card(
                                    "📈",
                                    "R(t)",
                                    GptaState.reliability_rt_display,
                                    "",
                                    "bg-teal-50 border-teal-200 mt-3",
                                ),
                                rx.el.div(
                                    class_name="my-4 border-t border-gray-200"
                                ),
                                _slider_component(
                                    "Fiabilité minimale (R₀)",
                                    GptaState.r0_slider_value.to_string()
                                    + "%",
                                    1,
                                    99,
                                    1,
                                    GptaState.r0_slider_value,
                                    GptaState.set_r0_slider_value,
                                ),
                                _metric_card(
                                    "🎯",
                                    "Périodicité préventive",
                                    GptaState.preventive_periodicity_display,
                                    "h",
                                    "bg-pink-50 border-pink-200 mt-3",
                                ),
                                class_name="bg-white p-4 rounded-lg shadow",
                            ),
                            class_name="flex flex-col space-y-6",
                        ),
                        class_name="grid md:grid-cols-2 gap-6",
                    ),
                    class_name="p-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "👋 Bienvenue ! Veuillez sélectionner un organe dans la barre latérale pour afficher ses détails et indicateurs de performance.",
                        class_name="text-center text-gray-600 text-lg",
                    ),
                    class_name="min-h-[calc(100vh-10rem)] flex items-center justify-center p-6",
                ),
            ),
            class_name="flex-grow transition-all duration-300 ease-in-out ml-64",
        ),
        class_name="bg-gray-50 min-h-screen pt-16",
    )