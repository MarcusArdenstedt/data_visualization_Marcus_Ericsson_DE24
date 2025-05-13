import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import DATA_DIRICTORY


df = pd.read_csv(DATA_DIRICTORY / "filter_nordic_company_ranking.csv")


metric_options = [
    "Revenue (billion $)",
    "Profits (billion $)",
    "Assets (billion $)",
    "Market value (billion $)",
]
categories_industry = list(df["Industry"].unique())
selected_industry = "Banking"
selected_metric = metric_options[0]
number_company = len(df[df["Industry"] == "Banking"])

filtered_data = df[df["Industry"] == selected_industry]
chart_data = (
    filtered_data[["Company", selected_metric]]
    .rename(columns={"Company": "x", selected_metric: "y"})
    .dropna()
    .reset_index(drop=True)
)


layout = {
    "yaxis": {"title": metric_options[0]},
    "title": f"Companies {metric_options[0]}",
    "xaxis": {"title": "Company"},
}


# initialisera dynamiska varibel utan att påverka grund data (df). chart_ data ändras helt för att man har state.df
def update_data(state):

    state.df = df[df["Industry"] == state.selected_industry]

    top_n = min(state.number_company, len(state.df))
    
    

    state.chart_data = (
        state.df[["Company", state.selected_metric]]
        .dropna()
        .sort_values(by=state.selected_metric, ascending=False)
        .head(top_n)
        .rename(columns={"Company": "x", state.selected_metric: "y"})
        .reset_index(drop=True)
    )

    state.layout = {
        "yaxis": {"title": state.selected_metric},
        "title": f"Companies {state.selected_metric}",
        "xaxis": {"title": "Company"},
    }

    # Uppdatera möjliga värden för antal företag om du vill ha dynamisk val
    state.company_range = list(range(0, len(state.df) + 1))


with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Nordic companies ranking", mode="md")
        with tgb.layout(column="(1 2)"):
            with tgb.part(class_name="text-center"):
                tgb.text("**Filter industry**", mode="md")
                tgb.selector(
                    value="{selected_industry}",
                    lov=categories_industry,
                    on_change=update_data,
                    dropdown=True,
                )

                tgb.text("**Filter metric**", mode="md")
                tgb.selector(
                    value="{selected_metric}",
                    lov=metric_options,
                    on_change=update_data,
                    dropdown=True,
                )

                tgb.html("br")
                tgb.text("**Number company**", mode="md")
                tgb.slider(
                    value="{number_company}", min=0, max=20, on_change=update_data
                )

            with tgb.part():
                tgb.chart(
                    data="{chart_data}",
                    x="x",
                    y="y",
                    type="bar",
                    layout="{layout}",
                )
        tgb.html("br")
        with tgb.part(class_name="card"):

            tgb.table(data="{df}")


if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=False, port=8080)
