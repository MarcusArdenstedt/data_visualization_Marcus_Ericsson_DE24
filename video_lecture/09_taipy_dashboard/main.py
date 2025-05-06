import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRECTORY
import pandas as pd
from frontend.charts import create_municipality_bar

df = pd.read_excel(
    DATA_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)


def filter_df_municipality(df, educational_area="Data/IT"):
    return (
        df.query("Utbildningsområde == @educational_area")["Kommun"]
        .value_counts()
        .reset_index()
        .rename({"count": "Ansökta utbildningar"}, axis=1)
    )


def filter_data(state):
    df_municipality = filter_df_municipality(
        state.df, educational_area=state.selected_educational_area
    )

    state.municipality_chart = create_municipality_bar(
        df_municipality.head(state.number_municipalities),
        ylabel="KOMMUN",
        xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    state.educational_area_title = state.selected_educational_area
    state.municipality_title = state.number_municipalities


df_municipality = filter_df_municipality(df)
selected_educational_area = "Data/IT"
number_municipalities = 5
municipality_title = number_municipalities
educational_area_title = selected_educational_area

municipality_chart = create_municipality_bar(df_municipality.head(9))


with tgb.Page() as page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="card"):
            tgb.text("# MYH dashboard 2024", mode="md")
            tgb.text(
                "En dashboard för att visa statistik och information om ansökningsomgång 2024",
                mode="md",
            )

        with tgb.layout(column="2 1"):
            with tgb.part(class_name="card") as column_chart:
                tgb.text(
                    "## Antal ansökta YH utbildningar per kommun (topp {municipality_title}) för {educational_area_title}",
                    mode="md",
                )

                tgb.chart(figure="{municipality_chart}")

            with tgb.part(class_name="card") as column_filter:
                tgb.text("## Filtrera data", mode="md")
                tgb.text(" Filtrera antal kommuner", mode="md")

                tgb.slider(
                    value="{number_municipalities}",
                    min=5,
                    max=len(df_municipality),
                    continuous=False,
                )

                tgb.text("Välj utbildningsområde", mode="md")
                tgb.selector(
                    value="{selected_educational_area}",
                    lov=df["Utbildningsområde"].unique(),
                    dropdown=True,
                )

                tgb.button("FILTRERA DATA", class_name="plain", on_action=filter_data)

        with tgb.part(class_name= "card"):
            tgb.text("## Rådata", mode= "md")
            tgb.table("{df}")
            
            
Gui(page, css_file="assets/main.css").run(
    dark_mode=False, use_reloader=False, port=8080
)
