import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
from utils.constants import DATA_DIRECTORY
from frontend.charts import create_municipality_bar

df = pd.read_excel(
    DATA_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)


def filter_municipality(df, educational_area="Data/IT"):
    return (
        df.query("Utbildningsområde == @educational_area")["Kommun"]
        .value_counts()
        .reset_index()
        .rename({"count": "Ansökta utbildningar"}, axis=1)
    )


def filter_data(state):

    df_municipality = filter_municipality(state.df, state.selected_educational_area)

    state.municipality_chart = create_municipality_bar(
        df_municipality.head(state.number_municipalities),
        xalabel="# ANSÖKTA UTBILDNINAGR",
        ylabel="KOMMUN"
    )

    state.municipalities_chart_title = state.number_municipalities
    state.educational_area_title = state.selected_educational_area



number_municipalities = 5
selected_educational_area = "Data/IT"




municipalities_chart_title = number_municipalities
educational_area_title = selected_educational_area 




df_municipality = filter_municipality(df, selected_educational_area).head(
    number_municipalities
)

municipality_chart = create_municipality_bar(
    df_municipality, xlabel="# ANSÖKTA UTBILDNINGSOMRÅDE", ylabel="KOMMNUN"
)


with tgb.Page() as page:
    with tgb.part(class_name="container card stack-large"):
        tgb.text("# MYH dashboard 2024", mode="md")

        with tgb.layout(columns=("2 1")):
            with tgb.part(class_name="card"):
                tgb.text(
                    "## Antalet ansökta YH utbildningar per kommun (topp {municipalities_chart_title}) för  {educational_area_title}",
                    class_name="title-chart",
                    mode="md",
                )
                tgb.chart(figure="{municipality_chart}")

            with tgb.part(class_name="card left-margin-md"):
                tgb.text("## Filtrera data", mode="md")
                tgb.text(" Filtrera antalet kommuner", mode="md")

                tgb.slider(
                    value="{number_municipalities}",
                    min=5,
                    max=len(filter_municipality(df)),
                    continuous=False,
                )

                tgb.text("Välj utbildningsområde", mode="md")
                tgb.selector(
                    "{selected_educational_area}",
                    lov=df["Utbildningsområde"].unique(),
                    dropdown=True,
                )

                tgb.button("FILTRERA DATA", class_name="buttom-color", on_action=filter_data)

        with tgb.part(class_name="card"):
            tgb.text("Raw data")
            tgb.table("{df}")


if __name__ == "__main__":
    Gui(page, css_file= "assets/main.css").run(dark_mode=False, use_reloader=False, port=8080)
