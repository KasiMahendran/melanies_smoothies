# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f" :cup_with_straw: Customize your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in custom smoothie!
  """
)


name_on_order = st.text_input('Name on Smoothie')
st.write('The Name on Smoothie is :', name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake");
session = cnx.session();
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

#editable_df = st.data_editor(my_dataframe)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop();

pd_df = my_dataframe.to_pandas();
#st.dataframe(pd_df);
#st.stop();

ingredients_list = st.multiselect('Choose upto 5 ingredients', my_dataframe)

if ingredients_list:
    st.write(ingredients_list);
    st.text(ingredients_list);

    ingredients_string =''

    for fruit_chosen in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        ingredients_string += fruit_chosen + ' '  
        st.subheader(fruit_chosen + ' Nutrition information');
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True);

    #st.write(ingredients_string);

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order');

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


#st.text(smoothiefroot_response.json())
                             

#option = st.selectbox('How would you like to be contacted? ',
#                      ('Email','Home Phone','Mobile Phone'))

#st.write('You selected :', option)

#option = st.selectbox('What is your favourite fruit? ',
#                      ('Banana','Strawberries','Peaches'))

#st.write('You selected :', option)


# title = st.text_input('Movie title','Life of Brian')
# st.write('The current movie title is :', title)















