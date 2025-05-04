import taipy.gui.builder as tgb
from taipy.gui import Gui
import plotly.express as px 

df = px.data.gapminder()
fig = px.line(df.query("country == 'Sweden'"), x= "year", y= "pop", title= "Sweden population")


slider_value = 5
select_fruit = "apple"
number1= 5
number2= 3

sum_ = number1 + number2
product = number1 * number2
difference = number1 - number2
quotient = number1 / number2




def perform_calculation(state):
    state.sum_ = int(state.number1) + int(state.number2)
    state.difference = int(state.number1) - int(state.number2)
    state.product = int(state.number1) * int(state.number2)
    state.quotient = int(state.number1) / int(state.number2)
    
def clear_result(state):
    state.sum_ = ""
    state.difference = ""
    state.product = ""
    state.quotient = ""


with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        with tgb.layout(columns="1 1 1"):
            with tgb.part() as column_fruit:
                tgb.text("# Hello taipy", mode="md")
                tgb.text("Welcome to the world of reactive programming")

                # slider value is now dynamic
                tgb.text("This is value from my slider {slider_value}")
                tgb.slider("{slider_value}", min=1, max=20)

                tgb.text("Select your favorite fruit")
                tgb.selector(
                    value="{select_fruit}",
                    lov=["apple", "tomato", "avocado", "banana"],
                    dropdown=True,
                )

                tgb.text("So it seems that you like **{select_fruit}**", mode="md")
                tgb.image("assets/{select_fruit}.jpg")
                
            with tgb.part() as column_calculator:
                tgb.text("## Coolu calculatoru", mode= "md")
                tgb.text("Type in a number")
                tgb.input("{number1}", on_change=clear_result)
                
                tgb.text("Type in another number")
                tgb.input("{number2}", on_change=clear_result)
                
                tgb.text(
                    "You've typed in number **{number1}** and **{number2}**", mode="md"
                )
                
                
                tgb.button(label= "Calculato", class_name= "plain", on_action= perform_calculation)
                
                tgb.text("**{number1}** + **{number2}** = **{sum_}**", mode= "md")
                tgb.text("**{number1}** - **{number2}** = **{difference}**", mode= "md")
                tgb.text("**{number1}** * **{number2}** = **{product}**", mode= "md")
                tgb.text("**{number1}** / **{number2}** = **{quotient}**", mode= "md")
                
            with tgb.part() as column_data:
                tgb.table("{df.head()}")
                
                tgb.chart(figure="{fig}")

if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)
