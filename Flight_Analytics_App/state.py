import reflex as rx
import duckdb as ddb
from pathlib import Path
import httpx


from .data.network_graph import ab_graph_png_data_url  # the network graph func
from .data.database import (
    route_query_scheduled,  # used for network graph
    on_time_count,
    cancelled_count,
    delayed_count,
    diverted_count,
    ICAO_conversion,
)


from .data.airport_list import AIRPORT_CODE_SET


class RouteState(rx.State):
    source_airport: str = ""
    dest_airport: str = ""
    months_back: int = 3

    pie_data: list[dict] = []  # the pie data
    network_graph_weight: int = 0  # the initial weight of the edge in the network graph
    show_pie_flag: bool = False  # flag to wait on pie

    # similar to how we bringing in self.network_graph_weight variable we gotta do it for the other 2 elements in the
    # network graph -> source airport and destination airport so that we can use them in the graph generation function
    @rx.var
    def network_graph_src(self) -> str:
        return ab_graph_png_data_url(
            self.network_graph_weight, self.source_airport, self.dest_airport
        )

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
    # removes whitespaces and make input upper case only
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

    source_fltCat = ""
    dest_fltCat = ""
    source_weather_explanation = ""
    source_card_color = ""
    dest_weather_explanation = ""
    dest_card_color = ""

    # METAR get current weather data -> put here due to circular import issue

    def current_weather_status(self) -> tuple[str, str]:

        src_icao = ICAO_conversion(ddb, self.source_airport)
        dst_icao = ICAO_conversion(ddb, self.dest_airport)

        origin_resp = httpx.get(
            "https://aviationweather.gov/api/data/metar",
            params={"ids": src_icao, "format": "json"},
            headers={"User-Agent": "wx-test"},
            timeout=5,
        )
        dest_resp = httpx.get(
            "https://aviationweather.gov/api/data/metar",
            params={"ids": dst_icao, "format": "json"},
            headers={"User-Agent": "wx-test"},
            timeout=5,
        )

        origin_status = origin_resp.json()
        dest_status = dest_resp.json()

        return (
            (origin_status[0]["fltCat"]),
            (dest_status[0]["fltCat"]),
        )

    # function to convert colors and explanation
    # same if statements for both fltCats for the tooltip

    def get_popup_explanation_and_color(self):

        if self.source_fltCat == "VFR":
            self.source_weather_explanation = "GOOD: Visibility is generally clear and low clouds are not expected to be a problem."
            self.source_card_color = "green"

        elif self.source_fltCat == "MVFR":
            self.source_weather_explanation = "CAUTION: Visibility and/or low clouds may start to cause minor limitations or delays."
            self.source_card_color = "gold"

        elif self.source_fltCat == "IFR":
            self.source_weather_explanation = "POOR: Visibility and/or low clouds are likely to cause disruptions and require extra caution."
            self.source_card_color = "orange"

        elif self.source_fltCat == "LIFR":
            self.source_weather_explanation = "VERY POOR: Visibility and/or low clouds are very limited, and significant impacts are likely."
            self.source_card_color = "red"

        elif self.source_fltCat == "VLIFR":
            self.source_weather_explanation = "EXTREME: Conditions are extremely limited and this is the most restrictive category on this scale."
            self.source_card_color = "purple"

        else:
            self.source_weather_explanation = "Unknown category."
            self.source_card_color = "gray"

        # for destination if statements

        if self.dest_fltCat == "VFR":
            self.dest_weather_explanation = "GOOD: Visibility is generally clear and low clouds are not expected to be a problem."
            self.dest_card_color = "green"

        elif self.dest_fltCat == "MVFR":
            self.dest_weather_explanation = "CAUTION: Visibility and/or low clouds may start to cause minor limitations or delays."
            self.dest_card_color = "gold"

        elif self.dest_fltCat == "IFR":
            self.dest_weather_explanation = "POOR: Visibility and/or low clouds are likely to cause disruptions and require extra caution."
            self.dest_card_color = "orange"

        elif self.dest_fltCat == "LIFR":
            self.dest_weather_explanation = "VERY POOR: Visibility and/or low clouds are very limited, and significant impacts are likely."
            self.dest_card_color = "red"

        elif self.dest_fltCat == "VLIFR":
            self.dest_weather_explanation = "EXTREME: Conditions are extremely limited and this is the most restrictive category on this scale."
            self.dest_card_color = "purple"

        else:
            self.dest_weather_explanation = "Unknown category."
            self.dest_card_color = "gray"

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
        cloud_path = Path("/var/data/combinedv2.parquet")
        local_path = Path("/home/sai/Downloads/combinedv2.parquet")
        path = ""
        if local_path.exists() == True:
            path = str(local_path)
        elif cloud_path.exists() == True:
            path = str(cloud_path)
        else:
            print("Please set the correct path for your parquet dataset")

        # computing this outside so we can reuse it
        on_time_count_var = on_time_count(
            ddb=ddb,
            parquet_path=path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        cancelled_count_var = cancelled_count(
            ddb=ddb,
            parquet_path=path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        delayed_count_var = delayed_count(
            ddb=ddb,
            parquet_path=path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        diverted_count_var = diverted_count(
            ddb=ddb,
            parquet_path=path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        # literally the worst way to do this
        # but if a value is zero we can make it none so it wont render
        if on_time_count_var == 0:
            on_time_count_var = None

        if delayed_count_var == 0:
            delayed_count_var = None

        if cancelled_count_var == 0:
            cancelled_count_var = None

        if diverted_count_var == 0:
            diverted_count_var = None

        # here we are rendering the pie chart
        self.pie_data = [
            {
                "name": "On Time Flights",
                "value": on_time_count_var,
                "fill": "#9B5DE5",
            },
            {
                "name": "Delayed",
                "value": delayed_count_var,
                "fill": "#F15BB5",
            },
            {
                "name": "Cancelled",
                "value": cancelled_count_var,
                "fill": "#FEE440",
            },
            {
                "name": "Diverted",
                "value": diverted_count_var,
                "fill": "#00BBF9",
            },
        ]

        # putting this in the network graph
        self.network_graph_weight = route_query_scheduled(
            ddb=ddb,
            parquet_path=path,  # for local path use this "/home/sai/Downloads/combinedv2.parquet"
            month_count=str(
                self.months_back
            ),  # for cloud path use "/var/data/combinedv2.parquet"
            source_airport=self.source_airport,  # prefer absolute paths for ease of use when hardcoding
            dest_airport=self.dest_airport,
        )

        yield self.show_pie_chart_func()

        self.source_fltCat, self.dest_fltCat = self.current_weather_status()

        self.get_popup_explanation_and_color()

        ### TO DO: MAKE WEATHER FETCH -> ASYNC I JUST PUT A 5s TIMEOUT + its the last thing that gets populated
