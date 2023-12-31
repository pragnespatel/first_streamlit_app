import streamlit
import snowflake.connector
import requests
import pandas
from urllib.error import URLError


streamlit.title("My Parents New Healthy Diner")
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
# streamlit.dataframe(my_fruit_list)

streamlit.header('Fruityvice Fruit Advice')

def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized



try:
  #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  #streamlit.write('The user entered ', fruit_choice)
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice :
      streamlit.error("Please select a fruit to get some information")
  else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # streamlit.text(fruityvice_response.json())
      # write your own comment -what does the next line do? 
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # write your own comment - what does this do?
      #streamlit.dataframe(fruityvice_normalized)
    
#streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error()

#def insert_row_snowflake(new_fruit):
#      with my_cnx.cursor() as my_cur:
#            my_cur.execute("insert into fruit_load_list values ('from streamlist')")
#            return "Thanks for adding " + new_fruit





# streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


# my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
# Snowflake-related functions
def get_fruit_load_list():
       with my_cnx.cursor() as my_cur:
             my_cur.execute("SELECT * from fruit_load_list")
             return my_cur.fetchall()


streamlit.header("View Our Fruit List - Add your Favorites!")
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows=get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)
             
             
# streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('"+new_fruit+ "')")
            return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add ?')
if streamlit.button('Add a Fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function=insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)
      
      
streamlit.write('Thanks for adding', add_my_fruit)

#my_cur.execute("Insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")


