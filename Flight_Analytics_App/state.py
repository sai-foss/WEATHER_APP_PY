import reflex as rx
import duckdb as ddb
from .data.network_graph import ab_graph_png_data_url  # the network graph func
from .data.database import (
    route_query_scheduled,
    route_query_delayed,
    route_query_weather_delayed,
    route_query_cancelled,
)


from .data.airport_list import AIRPORT_CODE_SET


class RouteState(rx.State):
    source_airport: str = ""
    dest_airport: str = ""
    months_back: int = 3

    pie_data: list[dict] = []  # the pie data
    network_graph_weight: int = 0  # the initial weight of the edge in the network graph
    show_pie_flag: bool = False  # flag to wait on pie

    @rx.var
    def network_graph_src(self) -> str:
        return ab_graph_png_data_url(self.network_graph_weight)

    # event to make the chart un-render on page reload
    # we can keep adding new charts to turn off here on reload
    @rx.event
    def on_page_load(self):
        self.show_pie_flag = False
        # more charts to un-render
        self.pie_data = []

    @rx.event
    def show_pie_chart_func(self):
        self.show_pie_flag = True

    @rx.event
    def set_months_back(self, months: int):
        self.months_back = max(1, int(months))

    # this method isn't an event so don't use the event decorator
    def _norm_code(self, value: str) -> str:
        v = (value or "").upper().strip()
        return v[:3]

    @rx.event
    def set_source_airport(self, value: str):
        v = self._norm_code(value)
        self.source_airport = v

        if len(v) == 3 and v not in AIRPORT_CODE_SET:
            # self.source_airport = ""
            yield rx.toast.error("Unknown origin airport code. Pick one from the list.")
            return

    @rx.event
    def set_dest_airport(self, value: str):
        v = self._norm_code(value)
        self.dest_airport = v

        if len(v) == 3 and v not in AIRPORT_CODE_SET:
            # self.dest_airport = ""
            yield rx.toast.error(
                "Unknown destination airport code. Pick one from the list."
            )
            return

    @rx.event
    def analyze(self):

        if not self.source_airport or not self.dest_airport:
            yield rx.toast.warning(
                "Enter both origin and destination before analyzing."
            )
            return

        if (self.source_airport not in AIRPORT_CODE_SET) or (
            self.dest_airport not in AIRPORT_CODE_SET
        ):
            yield rx.toast.error("Please select valid airport codes from the list.")
            return

            # defensive checks (when both origin = destination)
        if (
            (self.source_airport in AIRPORT_CODE_SET)
            and (self.dest_airport in AIRPORT_CODE_SET)
            and (self.source_airport == self.dest_airport)
        ):
            yield rx.toast.error("Origin and destination cannot be the same.")
            return

        # bring in the data from user input we just checking user input in console log

        yield rx.console_log(self.source_airport)

        yield rx.console_log(self.dest_airport)

        yield rx.console_log(str(self.months_back))

        yield rx.toast.success("Generating Graphs")

        # pi chart data starting here

        # paths
        cloud_path = "/var/data/combinedv2.parquet"
        local_path = "/home/sai/Downloads/combinedv2.parquet"

        self.pie_data = [
            {
                "name": "Total Delayed",
                "value": route_query_delayed(
                    ddb=ddb,
                    parquet_path=cloud_path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
                    month_count=str(
                        self.months_back
                    ),  # for cloud path use "/var/data/combinedv2.parquet"
                    source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
                    dest_airport=self.dest_airport,
                ),
                "fill": "#3e63dd",
            },
            {
                "name": "Weather Delayed",
                "value": route_query_weather_delayed(
                    ddb=ddb,
                    parquet_path=cloud_path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
                    month_count=str(
                        self.months_back
                    ),  # for cloud path use "/var/data/combinedv2.parquet"
                    source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
                    dest_airport=self.dest_airport,
                ),
                "fill": "yellow",
            },
            {
                "name": "Cancelled",
                "value": route_query_cancelled(
                    ddb=ddb,
                    parquet_path=cloud_path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
                    month_count=str(
                        self.months_back
                    ),  # for cloud path use "/var/data/combinedv2.parquet"
                    source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
                    dest_airport=self.dest_airport,
                ),
                "fill": "red",
            },
        ]

        # putting this in the network graph
        self.network_graph_weight = route_query_scheduled(
            ddb=ddb,
            parquet_path=cloud_path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        yield self.show_pie_chart_func()
