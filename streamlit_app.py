import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title("My Mom's New Healthy Diner")
streamlit.header("Breakfast favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard Boiled Free-Range Egg")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index("Fruit")
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruity Vice Advice!")

def Fruity_vice_response_fun(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  fruityvice_normalized = fruityvice_normalized.set_index("name")
  return streamlit.dataframe(fruityvice_normalized)

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit of choice")
  else:
    fruitvice_normalized=Fruity_vice_response_fun(fruit_choice)
    streamlit.write('The user entered ', fruit_choice)
    
    
except URLerror as e:
  streamlit.error()
    

streamlit.stop()



# write your own comment -what does the next line do? 

# write your own comment - what does this do?



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("FRUIT LOAD LIST CONTAINS :")
streamlit.dataframe(my_data_row)

fruit_to_add = streamlit.text_input('Which fruit would you like add?','jackfruit')
streamlit.write('Thank you for adding  ', fruit_to_add)
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES (%s)",fruit_to_add)
