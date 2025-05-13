
from taipy.gui import Gui
import taipy.gui.builder as tgb
import time 

word= ""
result= ""

number_stars = 0
stars = "🌟" * number_stars
picture_url= ""
    


def check_palindrome(state):

    if state.word.lower() == state.word[::-1].lower() or state.word.lower() == "":
        state.picture_url = "https://github.com/kokchun/assets/blob/main/data_visualization/fake_cat.png?raw=true"
        time.sleep(1)
        state.result = f"'{state.word}': is a palindrome!"
        state.number_stars += 1
        state.stars =  "🌟" * state.number_stars
    
    else:
        state.picture_url = "https://github.com/kokchun/assets/blob/main/data_visualization/fake_sad_rabbit.png?raw=true"
        time.sleep(1)
        state.result = f"'{state.word}': is not a palindrome!"
        state.number_stars -= 1
        state.stars =  "🌟" * state.number_stars
        
    
         

with tgb.Page() as page:
    with tgb.part(class_name= "container card stack"):
            tgb.text("# Palindrome game", mode= "md")
            
            with tgb.layout(columns= ("1 1")):
                with tgb.part(class_name="container card"):
                    tgb.input(value="{word}", label= "Type palindrome")
                    tgb.button(label="CONTROLE", on_action=check_palindrome)
                    
                with tgb.part(class_name= "container car"):
                    tgb.image("{picture_url}")
                    tgb.text("{result}")
                    tgb.text("{stars}")
                    
               
          
    

if __name__=="__main__":
    Gui(page, css_file= "assets/main.css").run(dark_mode=False, use_reloader=False, port=8080)