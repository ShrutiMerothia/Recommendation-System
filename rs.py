# Importing required libraries
import pandas as pd
import streamlit as st
import textdistance



#Read dataset of available products from csv file
data=pd.read_csv("cellphones data.csv")

#define a function to calculate similarity score between user input and brand.
def get_similarity_score(input_string,target_string):
    return textdistance.levenshtein.normalized_similarity(input_string,target_string)


#define a function to filter the products based on user input & similarity score

def get_filterd_products(brand,storage,ram,m_camera):
    filtered_products=data[(data['RAM']>=ram)&(data['internal memory']>=storage)&(data['main camera']>=m_camera)]
    filtered_products['similarity_score']=filtered_products['brand'].apply(lambda x:get_similarity_score(brand,x))
    filtered_products=filtered_products[filtered_products['similarity_score']>=0.5]
    return filtered_products.sort_values(by=['model'])


#creating a streamlit app
def app():
    #set app title & icon
    st.set_page_config(page_title="Smartphone Recommendation System",page_icon=":iphone:")

    #background
        
    page_bg_img="""
        <style>
            [data-testid="stAppViewContainer"]{
            background-image:url("https://images.unsplash.com/photo-1483478550801-ceba5fe50e8e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8c21hcnRwaG9uZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=600&q=60");
            background-size:cover;
            

            }
            [data-testid="stHeader"]{
            background-color:rgba(0,0,0,0);
            }

            [data-testid="stToolbar]{
            right:2rem;
            }
            </style>
        """
    st.markdown(page_bg_img,unsafe_allow_html=True)
    #set app heading
    st.title("Smartphone Recommendation System")

    #taking user input from the required specifications
    #brand
    brand=st.selectbox("Brand",data['brand'].unique())

    #RAM
    ram=st.selectbox("RAM",[3,4,6,8,12])

    #Storage
    storage=st.selectbox("Internal Storage",[32,64,128,256,512])

    #main camera
    m_camera=st.selectbox("Main Camera",[12,13,48,50,64,108])

    #filter products on the basis on user input
    filtered_products=get_filterd_products(brand,storage,ram,m_camera)

    #display recommended products
    if st.button("Show Recommendation"):
        if filtered_products.empty:
            st.warning("Sorry, no product match your requirements!")
        else:
            st.success("Here are your recommended products:")
            st.write(filtered_products[['brand','model']])

if __name__ == '__main__':
    app()