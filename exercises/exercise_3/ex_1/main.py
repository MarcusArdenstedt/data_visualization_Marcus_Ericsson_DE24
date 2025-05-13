
from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import random


# Global variable 
df = pd.DataFrame()
slider1= 5
slider2= 30001

# Creating a simulation for dices throw. Function to put in how many diceses and how many throws
# using for-loop where the argument decides how many times the diceses throws 
# roll is initialized with list comprehension and random.randint simulate between 1 to 6
# initialized df with Dataframe where throw is all the data that simulated and named the columns dice and multiply 
# with dice to name all new column dice
def throw_dices(dice= 5, roll= 30001):
    throw = []
    for _ in range(roll):
        roll = [random.randint(1, 6) for _ in range(dice)]
        throw.append(roll)
        
    df = pd.DataFrame(throw, columns= [f"dice_{i +1}" for i in range(dice)])

    df.index.name = "Throw"
    
    return df


df = throw_dices(slider1, slider2)
print(throw_dices(1, 1))
# Function to invoked state 
def update_data(state):
    
    state.df = throw_dices(state.slider1, state.slider2)
    

with tgb.Page() as page:
    with tgb.part(class_name= "card"):
        tgb.text("# Dices simulations", mode= "md")
        
    tgb.html("br")
    with tgb.layout(columns="1 1"):
        with tgb.part(class_name= "card"):
            tgb.table(data= "{df}")
            
            tgb.html("br")
            tgb.text("SLIDER1 NUMBER DICES CHOSEN")
            tgb.slider(value= "{slider1}", min= 1, max= 10)
            
            tgb.html("br")
            tgb.text("SLIDER2 NUMBER THROWS")
            tgb.slider(value= "{slider2}", min= 1, max= 100000)
            
            tgb.html("br")
            tgb.button("Simulate", on_action= update_data)
            
        with tgb.part(class_name= "card"):
            with tgb.layout(columns= "1 1 1" ):
                with tgb.part(class_name= "card"):
                    tgb.text("Theoretical mean", mode= "md")
                with tgb.part(class_name= "card"):
                    tgb.text("Calculated mean", mode= "md")
                with tgb.part(class_name= "card"):
                    tgb.text("Difference", mode= "md")
                    
            tgb.html("br")
            with tgb.part(class_name= "text-center"):
                tgb.text("**chart**", mode= "md")
                    
            
        


if __name__=="__main__":
    Gui(page).run(dark_mode=False, use_reloader=False, port=8080)