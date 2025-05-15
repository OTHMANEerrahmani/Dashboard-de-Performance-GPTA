import reflex as rx
from app.states.gpta_state import GptaState


def metric_item(
    label: str, value: rx.Var | str, unit: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.dt(
            label,
            class_name="text-sm font-medium text-gray-500",
        ),
        rx.el.dd(
            rx.el.span(
                value,
                class_name="text-lg font-semibold text-indigo-700",
            ),
            rx.cond(
                unit,
                rx.el.span(
                    f" {unit}",
                    class_name="text-sm text-gray-600",
                ),
                "",
            ),
            class_name="mt-1",
        ),
        class_name="p-3 bg-indigo-50 rounded-md",
    )


def input_item(
    label: str,
    state_var: rx.Var,
    on_change_event: rx.EventChain,
    placeholder: str,
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-700",
        ),
        rx.el.input(
            default_value=state_var,
            on_change=on_change_event,
            placeholder=placeholder,
            type=type,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
        ),
        class_name="col-span-1",
    )


def formulas_display() -> rx.Component:
    formula_style = "text-sm text-gray-700 py-1"
    return rx.el.div(
        rx.el.h4(
            "Formules Utilisées:",
            class_name="text-md font-semibold text-gray-700 mb-2",
        ),
        rx.el.p(
            "MTBF = Temps total de fonctionnement / Nb de pannes",
            class_name=formula_style,
        ),
        rx.el.p(
            "MTTR = Durée totale des réparations / Nb d’interventions correctives",
            class_name=formula_style,
        ),
        rx.el.p(
            "λ (Lambda) = 1 / MTBF",
            class_name=formula_style,
        ),
        rx.el.p(
            "Disponibilité (A) = MTBF / (MTBF + MTTR)",
            class_name=formula_style,
        ),
        rx.el.p(
            "Fiabilité R(t) = e^(-λ × t)",
            class_name=formula_style,
        ),
        rx.el.p(
            "Périodicité Préventive = –ln(R0) / λ",
            class_name=formula_style,
        ),
        class_name="p-4 bg-gray-100 rounded-lg mt-4",
    )


def metrics_display() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Calculs de Performance",
            class_name="text-xl font-semibold text-gray-800 mb-3",
        ),
        rx.el.dl(
            metric_item(
                "MTBF (Mean Time Between Failures)",
                GptaState.mtbf,
                "heures",
            ),
            metric_item(
                "MTTR (Mean Time To Repair)",
                GptaState.mttr,
                "heures",
            ),
            metric_item(
                "Taux de défaillance (λ)",
                GptaState.lambda_rate,
            ),
            metric_item(
                "Disponibilité (A)",
                GptaState.availability_display_str,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            input_item(
                "Temps 't' pour R(t) (heures):",
                GptaState.user_input_t_str,
                GptaState.set_user_input_t_str,
                "e.g., 1000",
            ),
            metric_item(
                "Fiabilité R(t)",
                GptaState.reliability_rt_display_str,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 p-4 border border-gray-200 rounded-lg",
        ),
        rx.el.div(
            input_item(
                "Fiabilité cible R0 pour Périodicité:",
                GptaState.user_input_r0_str,
                GptaState.set_user_input_r0_str,
                "e.g., 0.9",
            ),
            metric_item(
                "Périodicité Préventive Opt.",
                GptaState.preventive_periodicity,
                "heures",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 border border-gray-200 rounded-lg",
        ),
        formulas_display(),
        class_name="mt-6",
    )