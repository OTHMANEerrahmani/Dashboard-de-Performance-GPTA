import reflex as rx
from typing import TypedDict, List, Optional
from datetime import datetime, timezone
import math

DEFAULT_IMAGE = "/favicon.ico"
GPA1_IMAGE = "/screw_technical_professional.png"


class OrganData(TypedDict):
    id: str
    name: str
    function: str
    image_url: str


class MaintenanceInterventionData(TypedDict):
    date: str
    organ_id: str
    type: str
    duration_h: float
    action: str
    remarks: str


ORGANS_LIST: List[OrganData] = [
    {
        "id": "GPA1",
        "name": "GPA1 - Groupe à vis",
        "function": "Compresse l'air du système.",
        "image_url": GPA1_IMAGE,
    },
    {
        "id": "GPA2",
        "name": "GPA2 - Dessiccateur",
        "function": "Assèche l'air comprimé.",
        "image_url": DEFAULT_IMAGE,
    },
    {
        "id": "GPA3",
        "name": "GPA3 - ADCU",
        "function": "Unité de contrôle et de surveillance.",
        "image_url": DEFAULT_IMAGE,
    },
    {
        "id": "GPA4",
        "name": "GPA4 - Ventilateur",
        "function": "Refroidit les composants du système.",
        "image_url": DEFAULT_IMAGE,
    },
    {
        "id": "GPA5",
        "name": "GPA5 - Capteurs / Pressostats",
        "function": "Mesure la pression et d'autres paramètres.",
        "image_url": DEFAULT_IMAGE,
    },
    {
        "id": "GPA6",
        "name": "GPA6 - Soupape de sécurité",
        "function": "Prévient les surpressions.",
        "image_url": DEFAULT_IMAGE,
    },
    {
        "id": "GPA7",
        "name": "GPA7 - Système de graissage",
        "function": "Lubrifie les parties mobiles.",
        "image_url": DEFAULT_IMAGE,
    },
]
MAINTENANCE_HISTORY_DATA: List[
    MaintenanceInterventionData
] = [
    {
        "date": "2024-02-10",
        "organ_id": "GPA1",
        "type": "Corrective",
        "duration_h": 2.5,
        "action": "Remplacement roulements",
        "remarks": "Bruit",
    },
    {
        "date": "2024-03-15",
        "organ_id": "GPA1",
        "type": "Changement",
        "duration_h": 1.0,
        "action": "Alumine",
        "remarks": "RAS",
    },
    {
        "date": "2024-03-25",
        "organ_id": "GPA1",
        "type": "Graissage +",
        "duration_h": 2.5,
        "action": "Graissage + realignement",
        "remarks": "Fuite",
    },
    {
        "date": "2024-04-12",
        "organ_id": "GPA1",
        "type": "Graissage +",
        "duration_h": 1.0,
        "action": "",
        "remarks": "",
    },
    {
        "date": "2024-04-12",
        "organ_id": "GPA1",
        "type": "Fuite",
        "duration_h": 1.5,
        "action": "",
        "remarks": "",
    },
    {
        "date": "2024-02-25",
        "organ_id": "GPA2",
        "type": "Preventive",
        "duration_h": 1.0,
        "action": "Changement alumine",
        "remarks": "RAS",
    },
    {
        "date": "2024-03-15",
        "organ_id": "GPA3",
        "type": "Corrective",
        "duration_h": 3.0,
        "action": "Remplacement ADCU",
        "remarks": "EV HS",
    },
    {
        "date": "2024-03-30",
        "organ_id": "GPA4",
        "type": "Preventive",
        "duration_h": 1.0,
        "action": "Nettoyage",
        "remarks": "",
    },
    {
        "date": "2024-04-20",
        "organ_id": "GPA5",
        "type": "Corrective",
        "duration_h": 1.5,
        "action": "Remplacement capteur pression",
        "remarks": "Erreur P",
    },
    {
        "date": "2024-05-01",
        "organ_id": "GPA2",
        "type": "Corrective",
        "duration_h": 2.0,
        "action": "Remplacement valve dessiccateur",
        "remarks": "Bloquée",
    },
]


class GptaState(rx.State):
    organs: List[OrganData] = ORGANS_LIST
    maintenance_history: List[
        MaintenanceInterventionData
    ] = MAINTENANCE_HISTORY_DATA
    selected_organ_id: str = ""
    t_slider_value: int = 100
    r0_slider_value: int = 88

    @rx.var
    def selected_organ(self) -> Optional[OrganData]:
        if not self.selected_organ_id:
            return None
        for organ in self.organs:
            if organ["id"] == self.selected_organ_id:
                return organ
        return None

    @rx.var
    def current_organ_interventions(
        self,
    ) -> List[MaintenanceInterventionData]:
        if not self.selected_organ_id:
            return []
        return [
            item
            for item in self.maintenance_history
            if item["organ_id"] == self.selected_organ_id
        ]

    @rx.var
    def _system_observation_period_hours(self) -> float:
        relevant_interventions = (
            self.current_organ_interventions
        )
        if not relevant_interventions:
            if not self.maintenance_history:
                return 8760.0
            all_dates = [
                datetime.strptime(
                    item["date"], "%Y-%m-%d"
                ).replace(tzinfo=timezone.utc)
                for item in self.maintenance_history
            ]
            min_system_date = (
                min(all_dates)
                if all_dates
                else datetime.now(timezone.utc)
            )
            duration = (
                datetime.now(timezone.utc) - min_system_date
            )
            return duration.total_seconds() / 3600
        organ_dates = [
            datetime.strptime(
                item["date"], "%Y-%m-%d"
            ).replace(tzinfo=timezone.utc)
            for item in relevant_interventions
        ]
        min_organ_date = min(organ_dates)
        max_observation_date = datetime.now(timezone.utc)
        duration = max_observation_date - min_organ_date
        return duration.total_seconds() / 3600

    @rx.var
    def num_failures(self) -> int:
        return len(
            [
                item
                for item in self.current_organ_interventions
                if item["type"] == "Corrective"
            ]
        )

    @rx.var
    def total_corrective_repair_duration_hours(
        self,
    ) -> float:
        return sum(
            (
                item["duration_h"]
                for item in self.current_organ_interventions
                if item["type"] == "Corrective"
            )
        )

    @rx.var
    def organ_total_operating_hours(self) -> float:
        if not self.selected_organ:
            return 0.0
        observation_period = (
            self._system_observation_period_hours
        )
        operating_hours = (
            observation_period
            - self.total_corrective_repair_duration_hours
        )
        return max(0.0, operating_hours)

    @rx.var
    def mtbf(self) -> str:
        if self.num_failures == 0:
            return "N/A"
        total_op_hours = self.organ_total_operating_hours
        if total_op_hours <= 0:
            return "N/A"
        val = total_op_hours / self.num_failures
        return f"{val:.2f}"

    @rx.var
    def mttr(self) -> str:
        if self.num_failures == 0:
            return "N/A"
        val = (
            self.total_corrective_repair_duration_hours
            / self.num_failures
        )
        return f"{val:.2f}"

    @rx.var
    def lambda_rate_value(self) -> Optional[float]:
        mtbf_str = self.mtbf
        try:
            mtbf_val = float(mtbf_str)
            if mtbf_val <= 0:
                return None
            return 1 / mtbf_val
        except ValueError:
            return None

    @rx.var
    def lambda_rate_display(self) -> str:
        val = self.lambda_rate_value
        if val is None:
            return "N/A"
        return f"{val:.5f}"

    @rx.var
    def availability_value(self) -> Optional[float]:
        mtbf_str = self.mtbf
        mttr_str = self.mttr
        try:
            mtbf_val = float(mtbf_str)
            mttr_val = float(mttr_str)
            if mtbf_val + mttr_val == 0:
                if (
                    self.num_failures == 0
                    and self.organ_total_operating_hours > 0
                ):
                    return 1.0
                return None
            return mtbf_val / (mtbf_val + mttr_val)
        except ValueError:
            if (
                self.num_failures == 0
                and self.organ_total_operating_hours > 0
            ):
                return 1.0
            return None

    @rx.var
    def availability_display(self) -> str:
        val = self.availability_value
        if val is None:
            return "N/A"
        return f"{val * 100:.2f}%"

    @rx.var
    def user_input_t(self) -> int:
        return self.t_slider_value

    @rx.var
    def user_input_r0(self) -> float:
        return self.r0_slider_value / 100.0

    @rx.var
    def reliability_rt_value(self) -> Optional[float]:
        lambda_val = self.lambda_rate_value
        if lambda_val is None or lambda_val < 0:
            if (
                self.num_failures == 0
                and self.organ_total_operating_hours > 0
            ):
                return 1.0
            return None
        t = self.user_input_t
        try:
            return math.exp(-lambda_val * t)
        except OverflowError:
            return None

    @rx.var
    def reliability_rt_display(self) -> str:
        val = self.reliability_rt_value
        if val is None:
            return "N/A"
        return f"{val:.2f}"

    @rx.var
    def preventive_periodicity_value(
        self,
    ) -> Optional[float]:
        lambda_val = self.lambda_rate_value
        r0 = self.user_input_r0
        if lambda_val is None or lambda_val <= 0:
            return None
        if not 0 < r0 < 1:
            return None
        try:
            return -math.log(r0) / lambda_val
        except (
            ValueError,
            ZeroDivisionError,
            OverflowError,
        ):
            return None

    @rx.var
    def preventive_periodicity_display(self) -> str:
        val = self.preventive_periodicity_value
        if val is None:
            return "N/A"
        return f"{val:.2f}"

    @rx.event
    def select_organ(self, organ_id: str):
        self.selected_organ_id = organ_id

    @rx.event
    def set_t_slider_value(self, value: str):
        try:
            self.t_slider_value = int(value)
        except ValueError:
            pass

    @rx.event
    def set_r0_slider_value(self, value: str):
        try:
            self.r0_slider_value = int(value)
        except ValueError:
            pass