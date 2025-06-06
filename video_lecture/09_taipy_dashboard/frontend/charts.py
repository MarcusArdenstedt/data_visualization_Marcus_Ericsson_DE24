import plotly.express as px

 


def create_municipality_bar(df, **options):
    df["Ansökta_label"] = df["Ansökta utbildningar"].apply(lambda row: " " * 2 + f"{row}")
    
    
    fig = px.bar(df, y="Kommun", x="Ansökta utbildningar", text= "Ansökta_label")

    fig.update_layout(
        plot_bgcolor="white",
        yaxis=dict(
            autorange="reversed",
            ticklabelposition="outside left",
            showline=True,
            linecolor="light grey",
            title=dict(text=f"<b>{options.get('ylabel')}</b>")
        ),
        xaxis= dict(
            linecolor= "lightgrey",
            showticklabels= False,
            title= f"<b>{options.get('xlabel')}</b>"
            )
        )
    
    fig.update_traces(
        textposition= "outside",
        hovertemplate= "<b>%{y}</b><br>Ansöka utbildningar: %{x}"
    )
    

    return fig
