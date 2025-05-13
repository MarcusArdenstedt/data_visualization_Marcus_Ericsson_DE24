import taipy.gui.builder as tgb
from backend.updates import filter_data
from backend.data_processing import filter_df_municipality, df
from frontend.charts import create_municipality_bar



df_municipality = filter_df_municipality(df)
selected_educational_area = "Data/IT"
number_municipalities = 5
municipality_title = number_municipalities
educational_area_title = selected_educational_area

municipality_chart = create_municipality_bar(df_municipality.head(9), ylabel= "KOMMUN", xlabel= "# ANSÖKTA UTBILDNINGAR")


with tgb.Page() as dashboard_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
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
                    class_name= "title-chart"
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

    
            