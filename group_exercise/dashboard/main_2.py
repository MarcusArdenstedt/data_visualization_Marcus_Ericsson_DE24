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






company_number = 1
company_dropdown_label = "Visa företag (7 tillgängliga)"

chart_data = (
    df[["Company", selected_metric]]
    .dropna()
    .sort_values(by=selected_metric, ascending=False)
    .head(company_number)
    .rename(columns={"Company": "x", selected_metric: "y"})
    .reset_index(drop=True)
)

layout = {
    "yaxis": {"title": selected_metric},
    "title": f"Topp {company_number} företag – {selected_metric}",
    "xaxis": {"title": "Company"},
}

# initialisera dynamiska varibel utan att påverka grund data (df). chart_ data ändras helt för att man har state.df
def update_data(state):
    
    state.df = df[df["Industry"] == state.selected_industry]

    state.company_range = list(
        state.df["Company"].dropna().unique()
    )

    state.company_dropdown_label = (
        f"Visa företag ({len(state.company_range)} tillgängliga)"
    )
    
    state.company_number_options = list(range(1, len(state.company_range) + 1))

    top_n = min(state.company_number, len(state.df))

   
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



with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Nordic companies ranking", mode="md")
        with tgb.layout(column="(1 2)"):
            with tgb.part(class_name="text-center"):
                tgb.text("**Filter industry**", mode="md")
                tgb.selector(
                    value="{selected_industry}",
                    lov=categories_industry,
                    dropdown=True,
                )

                tgb.text("**Filter metric**", mode="md")
                tgb.selector(
                    value="{selected_metric}",
                    lov=metric_options,
                    dropdown=True,
                )

                tgb.html("br")
                tgb.text("**{company_dropdown_label}**", mode="md")
                tgb.selector(
                    value="{company_number}",
                    lov="{company_number_options}",
                    dropdown=True,
                )

                tgb.button(
                    label="UPDATE VIEW", on_action=update_data, class_name="plain"
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