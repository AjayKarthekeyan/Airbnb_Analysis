import pandas as pd
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import mysql.connector as sql
from PIL import Image
import plotly.express as px 
import plotly.graph_objects as go                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from plotly.subplots import make_subplots
import millify
import warnings
warnings.filterwarnings("ignore")

#connect the database
conn = sql.connect(host="localhost",user="root",password="",database="airbnb")
mydb = conn.cursor()

# set up page configuration for streamlit
icon = 'D:\\pythoncode\\Proj\\Airbnb\\images\\logo.png'
st.set_page_config(page_title='AIRBNB',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide',menu_items={"about":'This streamlit application was developed by AJAY'})
col1,col2 = st.columns([1,3])
with col1:
    st.image('D:\\pythoncode\\Proj\\Airbnb\\images\\logo1.png',width=150)
with col2:
    title_text = '''<h1 style='font-size: 40px;color:#FF5A5F;text-align: left;'>AirBnB - Air Bed and Breakfast!</h1>'''
    st.markdown(title_text, unsafe_allow_html=True)

#set up home page and optionmenu 
selected = option_menu(None,
                        options=["HOME","DISCOVER","INSIGHTS","ABOUT"],
                        icons=["house-fill", "globe-central-south-asia", "lightbulb", "info-circle-fill"],
                        default_index=0,
                        orientation="horizontal",
                        styles={"container": {"width": "100%","border": "1px ridge  ","background-color": "#6e5353","primaryColor": "#FF5A5F"},
                                "icon": {"color": "#F5B7B1", "font-size": "20px"}})

if selected == "ABOUT":
        st.subheader(":red[Project Title :]")
        st.markdown("AIRBNB Data Analysis - A data app using Python,MySQL and Streamlit",unsafe_allow_html=True)
        st.subheader(":violet[Domain :]")
        st.markdown("Travel Industry, Property Management and Tourism")
        st.subheader(":violet[Skills Employed :]")
        st.markdown("Python scripting, Data Pre-processing, Visualization, EDA, Streamlit, MySQL, PowerBI",unsafe_allow_html=True)
        st.subheader(":violet[Overview :]")
        st.markdown('''##### In this project, we aim to use the :red[Airbnb data] that is shared to us as a JSON file (originally stored in MongoDB Atlas) and visualise it on the streamlit app using the plotly library in python. In addition to this, we are going to also be developing a :red[Power BI dashboard] to provide end users with colourful charts and stats in a single page view.''',unsafe_allow_html=True)
        st.write('')
        st.markdown('''
                    :violet[Pandas:] Leveraged the powerful Pandas library to transform the dataset from JSON format into a structured dataframe. Pandas facilitated data manipulation, cleaning, and preprocessing, ensuring the data was ready for analysis.<p>
                    :violet[MySQL Connector:] (Not a mandatory step) Utilized MySQL Connector to establish a connection to MySQL database, enabling seamless integration of the transformed dataset and the data was efficiently inserted into relevant tables for storage and retrieval.<p>
                    :violet[Streamlit:] Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and geo-analysis of the airbnb data.<p>
                    :violet[Plotly:] Integrated Plotly, a versatile plotting library, to generate insightful visualizations from the dataset. Plotly's interactive plots, including geospatial plots and other data visualizations, provided users with a comprehensive understanding of the dataset's contents.<p>
                    :violet[Power BI:] Made use of Power BI's impressive dashboarding tools to better visualise all the data in a single view. ''',unsafe_allow_html=True)
        st.subheader(':violet[Contact :]')
        st.markdown('##### Linkedin: www.linkedin.com/in/ajay-k-76a28a227/')
        st.markdown('##### GitHub : https://github.com/AjayKarthekeyan')

if selected == "INSIGHTS":
        opt=['Top 10 Accommodation with Highest price',
            'Top 10 Accommodation with Lowest price ',
            'Number of Hotels Count by Country',
            'Top 10 Hosts with the highest listings',
            'Top 10 Accommodation with Highest Reviews',
            'Room Type Distribution by Country & Street',
            'Top 10 Accomodations with Average Review Scores',
            'Price of Accomodation based on Number of Rooms']
        st.markdown("<h3 style='font-weight:bold;text-align:center;color:#FF5A9F'>Select a Query</h3>", unsafe_allow_html=True)
        query=st.selectbox('',options=opt,index=None)

        if query==opt[0]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Top 10 Accomodations by Highest Price</h2>'''
            st.markdown(head_text, unsafe_allow_html=True)
            mydb.execute('''SELECT property_name, property_type, Country, MAX(price) as 'Price' from airbnb_listings 
                                        GROUP by property_name, Country,property_type ORDER by MAX(price) DESC LIMIT 10;''')
            df = pd.DataFrame(mydb.fetchall(), columns=['Property_Name','Property_Type','Country','Price']) 
            st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] {font-size: 50px;}
                        </style>""", unsafe_allow_html=True)
            st.write('')
            
            c1,c2,c3,c4 = st.columns((1.2,1.5,2,1.5), gap='small')
            with c1:
                st.image('https://avatars.githubusercontent.com/u/698437?s=280&v=4',width=120)
            with c2:
                st.metric(label="Price in $",value="$ "+str(df['Price'][0]),help="The price of highest priced property")
            with c3:
                st.metric(label="Property Type",value=str(df['Property_Type'][0]),help="The highest priced property type")
            with c4:
                st.metric(label="Country of Property",value=str(df['Country'][0]),help="The Country of highest priced property")

            col1,col2=st.columns([2,1.5])

            with col1:
                st.write(' ')
                st.write(' ')
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Top 10 Accommodation with Highest price</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                mydb.execute('''SELECT property_name, property_type, Country, MAX(price) as 'Price' from airbnb_listings 
                                        GROUP by property_name, Country,property_type ORDER by MAX(Price) DESC LIMIT 10;''')
                df = pd.DataFrame(mydb.fetchall(), columns=['Property_Name','Property_Type','Country','Price'])
                
                fig=px.bar(df,y='Price',x='Property_Type',color='Property_Name',
                        hover_data=['Property_Type','Country'],
                        color_discrete_sequence=px.colors.sequential.Blugrn)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.write(' ')
                st.write(' ')
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Top 10 Accommodation with Highest price (%)</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                fig=px.pie(df,names='Property_Name',values='Price',color='Property_Name',
                        color_discrete_sequence=px.colors.sequential.Blugrn,
                        hole = 0.3)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.markdown('<br>', unsafe_allow_html=True)
            
            c1,c2 = st.columns([2,1.5])
            with c1:
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Tabulation of Accomodations</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                st.dataframe(df,hide_index=True)
            with c2:
                i2 = st.button("Insight")
                if i2:
                        st.markdown('''
                                        - Istanbul, Turkey: "Center of Istanbul Sisli" stands out as the most expensive accommodation with a price of 48,842 Turkish Lira,
                                    reflecting its prime location in the heart of Istanbul's vibrant Sisli district.
                                        
                                    - Hong Kong: The city boasts several high-priced accommodations, including "HS1-2人大床房+丰泽､苏宁､百脑汇+女人街+美食中心" and 
                                    "良德街3号温馨住宅" priced at 11,681 Hong Kong Dollars each, suggesting a strong demand for upscale lodging options in this bustling.
                                        
                                    - Brazil: Brazil features luxurious accommodations like "Apartamento de luxo em Copacabana - 4 quartos" and "Deslumbrante apartamento na AV.Atlantica"
                                    with prices exceeding 6,000 Brazilian Reais, catering to travelers seeking premium experiences along the country's picturesque coastlines
                                        ''')
        if query==opt[1]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Top 10 Accomodations by Lowest Price</h2>'''
            st.markdown(head_text, unsafe_allow_html=True)
            mydb.execute('''SELECT property_name, property_type, Country, MIN(price) as 'Price' from airbnb_listings 
                                        GROUP by property_name, Country,property_type ORDER by MIN(Price) LIMIT 10;''')
            df = pd.DataFrame(mydb.fetchall(), columns=['Property_Name','Property_Type','Country','Price']) 
            st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] {font-size: 50px;}
                        </style>""", unsafe_allow_html=True)
            st.write('')
            
            c1,c2,c3,c4 = st.columns((1.2,1.5,2,1.5), gap='small')
            with c1:
                st.image('https://avatars.githubusercontent.com/u/698437?s=280&v=4',width=120)
            with c2:
                st.metric(label="Price in $",value="$ "+str(df['Price'][0]),help="The price of lowest priced property")
            with c3:
                st.metric(label="Property Type",value=str(df['Property_Type'][0]),help="The lowest priced property type")
            with c4:
                st.metric(label="Country of Property",value=str(df['Country'][0]),help="The Country of lowest priced property")

            col1,col2=st.columns([2,1.5])

            with col1:
                st.write(' ')
                st.write(' ')
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Top 10 Accommodation with Lowest price</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                mydb.execute('''SELECT property_name, property_type, Country, MIN(price) as 'Price' from airbnb_listings 
                                        GROUP by property_name, Country,property_type ORDER by MIN(Price)  LIMIT 10;''')
                df = pd.DataFrame(mydb.fetchall(), columns=['Property_Name','Property_Type','Country','Price'])
                
                fig=px.bar(df,y='Price',x='Property_Type',color='Property_Name',
                        hover_data=['Property_Type','Country'],
                        color_discrete_sequence=px.colors.sequential.Blugrn)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.write(' ')
                st.write(' ')
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Top 10 Accommodation with Lowest price (%)</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                fig=px.pie(df,names='Property_Name',values='Price',color='Property_Name',
                        color_discrete_sequence=px.colors.sequential.Blugrn,
                        hole = 0.3)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.markdown('<br>', unsafe_allow_html=True)
            
            c1,c2 = st.columns([2,1.5])
            with c1:
                head_text = '''<h5 style='font-size: 24px;color:#00A699;text-align: center;'>Tabulation of Accomodations</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                st.dataframe(df,hide_index=True)
            with c2:
                i2 = st.button("Insights")
                if i2:
                        st.markdown('''
                                        - Among the top 10 accommodations listed, the most budget-friendly options are found in Portugal,Canada and Spain..
                                        
                                    - Portugal offers the most affordable accommodations, with prices ranging from  9 to 13 dollars. Spain also provides reasonably priced options, with room rates starting at 10 and 12 dollars.
                                        
                                    - Notably, Canada appears in the top 10 list with a "Good room" priced at $13, reflecting a competitive pricing compared to European destinations.
                                        ''')

        if(query == opt[2]):
             head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Numbers Of Hotels Count By Country</h2>'''
             st.markdown(head_text, unsafe_allow_html=True)
             mydb.execute("Select distinct Country as 'Country' from airbnb_listings")
             df_country = pd.DataFrame(mydb.fetchall(), columns=['Country'])
             c1,c2 = st.columns([1,2])
             with c1:
                country_select = st.selectbox("Country", options = df_country['Country'].tolist(), index = None)
             if country_select:
                 c1,c2 = st.columns([1.8,1], gap='large')
                 mydb.execute(f'''SELECT property_type, count(_id) as 'property_count', Country from airbnb_listings 
                                        where Country = '{country_select}' group by property_type ORDER BY count(_id) DESC limit 10;''')
                 df_main = pd.DataFrame(mydb.fetchall(), columns=['Property Type','Count of Stays','Country'])
                 with c1:
                    st.write('')
                    head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Total Listings by Property Types</h5>'''
                    st.markdown(head_text, unsafe_allow_html=True)
                    fig=px.bar(df_main,x='Property Type',y='Count of Stays',
                        hover_data=['Property Type','Count of Stays'],
                        color = 'Property Type',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                 with c2:
                    head_text = '''<h2 style='font-size: 24px;color:#00A699;text-align: left;'>Tabulation: Total Listings by Property Types</h2>'''
                    st.markdown(head_text, unsafe_allow_html=True)
                    st.dataframe(df_main, hide_index=True)
                 i2 = st.button("Insights")
                 if i2:
                         st.markdown('''
                                    - The most common property types across these countries are Apartments, reflecting the popularity of urban living spaces and providing comfortable accommodation options for travelers.

                                    - Other prevalent property types include Houses, Townhouses, and Condominiums, offering diverse choices for different preferences and travel styles.

                                    - Additionally, unique accommodations such as Lofts, Serviced Apartments, and Boutique Hotels cater to travelers seeking distinctive and memorable lodging experiences.
                                        ''')
        if query==opt[3]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Top 10 Hosts with highest listings(with Country filter)</h2>'''
            st.markdown(head_text, unsafe_allow_html=True)
            st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] {font-size: 40px;}
                        </style>""", unsafe_allow_html=True)
            st.write('')
            mydb.execute(f'''SELECT host_id, host_name, Street, COUNT(host_id) as 'Listing_count' FROM airbnb_listings
                             group by host_id, host_name  Order by count(host_id) DESC limit 10;''')
            df_main = pd.DataFrame(mydb.fetchall(), columns=['Host ID','Host Name','Host_location','Listings count'])
            c1,c2,c3,c4 = st.columns((1.2,1,1,2), gap='small')
            with c1:
                st.image('https://avatars.githubusercontent.com/u/698437?s=280&v=4',width=120)
            with c2:
                st.metric(label="Top Host",value= str(df_main['Host Name'][0]))
            with c3:
                st.metric(label="Host Listings",value=str(df_main['Listings count'][0]))
            with c4:
                st.metric(label="Host Location",value=str(df_main['Host_location'][0][0:9]))
            c1,c2 = st.columns([2,1], gap='large')
            with c1:
                st.write('')
                st.write('')
                head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Hosts with Highest listings</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                fig=px.bar(df_main,x='Listings count',y='Host Name',
                hover_data=['Host Name','Listings count','Host_location'],
                color = 'Host Name',
                color_discrete_sequence=px.colors.qualitative.Pastel2)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                        
            with c2:
                st.write('')
                head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: center;'>Tabulation: Top 10 Hosts</h2>'''
                st.markdown(head_text, unsafe_allow_html=True)
                st.write('')
                st.dataframe(df_main, hide_index=True)
                
            i2 = st.button("Insights")
            if i2:
                st.markdown('''
                                - Jov leads the pack with an impressive tally of 18 listings, showcasing a significant presence in the accommodation landscape.

                                - Sonder follows closely with 11 listings, indicating a substantial contribution to the Airbnb platform.
                                
                                - Alejandro and Eva&Jacques each boast 9 listings, further diversifying the options available to Airbnb guests.
                                ''')
        if query==opt[4]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Top 10 Accomodations with Highest Reviews</h2>'''
            st.markdown(head_text, unsafe_allow_html=True)
            st.write('')
            # mydb.execute("Select distinct Country as 'Country' from airbnb_listings")
            # df_country = pd.DataFrame(mydb.fetchall(), columns=['Country'])
            # c1,c2 = st.columns([1,2])
            # with c1:
            #     country_select = st.selectbox("Country", options = df_country['Country'].tolist(), index = None)
            # if country_select:
            c1,c2 = st.columns([1.8,1], gap='large')
            mydb.execute(f'''select property_name,host_name,Country,Ratings,Review_cnt from airbnb_listings 
                                 order by Review_cnt DESC LIMIT 10;''')
            df_main = pd.DataFrame(mydb.fetchall(), columns=['Property Name','Host Name','Country','Ratings','Review_count'])
            c1,c2,c3,c4 = st.columns((1.5,1.7,1,1), gap='small')
            with c1:
                st.image('https://avatars.githubusercontent.com/u/698437?s=280&v=4',width=120)
            with c2:
                st.metric(label="Country of Property",value= str(df_main['Country'][0]))
            with c3:
                st.metric(label="Review count",value=str(df_main['Review_count'][0]))
            with c4:
                st.metric(label="Host Name",value=str(df_main['Host Name'][0]))
            c1,c2 = st.columns([1.7,1], gap='large')
            with c1:
                st.write('')
                st.write('')
                st.write('')
                head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Accomodations with highest reviews</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                fig=px.bar(df_main,x='Review_count',y='Property Name',
                hover_data=['Property Name','Review_count'],
                color = 'Review_count',
                color_continuous_scale=px.colors.sequential.Blugrn)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                        
            with c2:
                st.write('')
                st.write('')
                head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: center;'>Tabulation: Top 10 Most Reviewed Stays</h2>'''
                st.markdown(head_text, unsafe_allow_html=True)
                st.write('')
                st.dataframe(df_main, hide_index=True)

            i2 = st.button("Insights")
            if i2:
                st.markdown('''
                            - #Private Studio - Waikiki Dream, a Condo in the United States hosted by Dana, leads the list with 533 reviews in total proving how
                            often the property has been rented out and loves by people.
                            - The second and third are closeby in the reviews of 469 and 463 respectively belongnig to a guest suite in Australia & an Apartment in Spain.
                            - The maximum in the list are from Portugal and Spain, proving our analysis that the stays in these places are among the affordable ones for guests.
                                ''')
        if query==opt[5]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Room Type Distribution by Country & Street</h2>'''
            st.markdown(head_text, unsafe_allow_html=True)
            c1,c2 = st.columns([1.5,1.5])
            with c1:
                mydb.execute("Select distinct Country as 'Country' from airbnb_listings;")
                df_country = pd.DataFrame(mydb.fetchall(), columns=['Country'])
                country_select = st.selectbox("Country", options = df_country['Country'].tolist(), index = None)
            with c2:
                mydb.execute(f"Select distinct Street as 'Street' from airbnb_listings where Country = '{country_select}';")
                df_street = pd.DataFrame(mydb.fetchall(), columns=['Street'])
                street_select = st.selectbox("Street", options = df_street['Street'].tolist(), index = None)
            if street_select:
                c1,c2 = st.columns([1.5,1.5], gap='large')
                mydb.execute(f"SELECT room_type, COUNT(room_type) as 'Room_Count',Country,Street FROM airbnb_listings WHERE Country = '{country_select}' AND Street = '{street_select}' GROUP BY Room_Type ORDER BY count(room_type) DESC LIMIT 10;")
                df_main = pd.DataFrame(mydb.fetchall(), columns=['Room Type','Count of Stays','Country','Street'])
                with c1:
                    st.write('')
                    head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Total Listings by Room Types</h5>'''
                    st.markdown(head_text, unsafe_allow_html=True)
                    fig=px.bar(df_main,x='Room Type',y='Count of Stays',
                               hover_data=['Room Type','Count of Stays'],
                               color = 'Room Type', color_discrete_sequence=px.colors.qualitative.Pastel1)
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with c2:
                    head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: center;'>Chart Metrics</h2>'''
                    st.markdown(head_text, unsafe_allow_html=True)
                    st.write('')
                    c0,c1 = st.columns([1,0.5])
                    with c0:
                        st.metric(label="Room Type",value= str(df_main['Room Type'][0]))
                    with c1:
                        st.metric(label="Count of Stays",value= str(df_main['Count of Stays'][0]))
                    st.write('')
                    st.write('')
                    head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: left;'>Tabulation: Total Listings by Room Types</h2>'''
                    st.markdown(head_text, unsafe_allow_html=True)
                    st.write('')
                    st.dataframe(df_main, hide_index=True)
        if query==opt[6]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Top 10 Accomodations with High Review Scores</h2>'''
            st.markdown(head_text, unsafe_allow_html=True) 
            st.write('')
            c1,c2 = st.columns([1.5,1.5])
            with c1:
                mydb.execute("Select distinct Country as 'Country' from airbnb_listings;")
                df_country = pd.DataFrame(mydb.fetchall(), columns=['Country'])
                country_select = st.selectbox("Country", options = df_country['Country'].tolist(), index = None)
            with c2:
                mydb.execute(f"Select distinct Street as 'Street' from airbnb_listings where Country = '{country_select}';")
                df_street = pd.DataFrame(mydb.fetchall(), columns=['Street'])
                street_select = st.selectbox("Street", options = df_street['Street'].tolist(), index = None)
            if street_select:
                mydb.execute(f'''SELECT property_name, Review_cnt, Ratings, host_name, Country, Street from airbnb_listings 
                                where Country = '{country_select}' and Street = '{street_select}' and Ratings>=9
                                order by Review_cnt DESC limit 10;''')
                df_main = pd.DataFrame(mydb.fetchall(), columns=['Property Name','Review Count','Review Score','Host Name','Country','Street'])
                st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] {font-size: 50px;}
                        </style>""", unsafe_allow_html=True)
                c1,c2,c3,c4 = st.columns((1.2,1,1,1), gap='small')
                with c1:
                        st.image('https://avatars.githubusercontent.com/u/698437?s=280&v=4',width=100)
                with c2:
                        st.metric(label="No_of_Reviews",value= str(df_main['Review Count'][0]))
                with c3:
                        st.metric(label="Review Score",value=str(df_main['Review Score'][0]))
                with c4:
                        st.metric(label="Host Name",value=str(df_main['Host Name'][0]))
                c1,c2 = st.columns([1.8,1.3], gap='large')
                with c1:
                        st.write('')
                        st.write('')
                        st.write('')
                        head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Top 10 Accomodations with High Review Scores</h5>'''
                        st.markdown(head_text, unsafe_allow_html=True)
                        fig=px.bar(df_main,x='Property Name',y='Review Score',
                        hover_data=['Property Name','Review Score'],
                        color = 'Review Score',
                        color_continuous_scale=px.colors.sequential.Burgyl)
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                                
                with c2:
                        st.write('')
                        st.write('')
                        head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: center;'>Tabulation: Top 10 High Scoring Listings</h2>'''
                        st.markdown(head_text, unsafe_allow_html=True)
                        st.write('')
                        st.dataframe(df_main, hide_index=True)
        if query==opt[7]:
            head_text = '''<h2 style='font-size: 36px;color:#00A699;text-align: center;'>Price of Accomodation by Number of rooms</h2>'''
            st.markdown(head_text, unsafe_allow_html=True, help= "This is to see the Average stay prices by number of rooms for each country") 
            st.write('')
            mydb.execute('''SELECT bedrooms, round(AVG(price),2) as 'Avg Price', Country from airbnb_listings 
                             Group by bedrooms, Country Order by bedrooms desc;''')
            df_main = pd.DataFrame(mydb.fetchall(), columns=['Total_bedrooms','Avg Price','Country'])
            c1,c2 = st.columns([2.5,0.9], gap='small')
            with c1:
                st.write('')
                head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Average Price by Rooms (Country coded)</h5>'''
                st.markdown(head_text, unsafe_allow_html=True)
                fig=px.line(df_main,x='Total_bedrooms',y='Avg Price',
                color = 'Country', color_discrete_sequence=px.colors.qualitative.Pastel_r)
                fig.update_layout(showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                        
            with c2:
                head_text = '''<h2 style='font-size: 28px;color:#00A699;text-align: center;'>Tabulation: Rooms with Average Prices and Country</h2>'''
                st.markdown(head_text, unsafe_allow_html=True)
                st.write('')
                st.dataframe(df_main, hide_index=True)

            i2 = st.button("Insights")
            if i2:
                st.markdown('''
                            - More on a price trend perspective, we see that Brazil (an exotic location) is peaking with high average price seeing a heavy spike for more than 3 rooms. 
                            - We do see an upward trend with Hong Kong that is seeing a spike similar to Brazil. Hong Kong has a thrilling city scape that enthuses guests. 
                            - On the other hand, we see Turkey which sees an upward trend spiking at the 7 rooms mark but only to decline after that. This maybe because the bigger properties for rent
                            are secluded from the rest of the country in an area which is not ideal for tourists.
                            - Brazil has the highest average price. 
                                ''')
if (selected == 'DISCOVER'):
    head_text = '''<h2 style='font-size: 38px;color:#00A699;text-align: left;'>Explore Accommodation</h2>'''
    st.markdown(head_text, unsafe_allow_html=True)
    st.markdown('''Here, we can discover the possible available Airbnbs for accommodation by filtering on the country, the street and type of property of stay.
        Let us look at our options.''')

    c1,c2,c3 = st.columns([1,1,1.5])
    with c1:
        mydb.execute("Select distinct Country as 'Country' from airbnb_listings")
        df_country = pd.DataFrame(mydb.fetchall(), columns=['Country'])
        country_select = st.selectbox("**Country**", options = df_country['Country'].tolist(), index = None)
#     st.write(' ')
    with c2:
        mydb.execute(f"Select distinct Street as 'Street' from airbnb_listings where Country = '{country_select}'")
        df_street = pd.DataFrame(mydb.fetchall(), columns=['Street'])
        street_select = st.selectbox("**Street**", options = df_street['Street'].tolist(), index = None)
    with c3:
        mydb.execute(f"Select distinct property_type as 'Type' from airbnb_listings where Street = '{street_select}'")
        df_prop_name = pd.DataFrame(mydb.fetchall(), columns=['Type'])
        prop_select = st.selectbox("**Type**", options = df_prop_name['Type'].tolist(), index = None)
    if prop_select: 
        head_text = '''<h2 style='font-size: 38px;color:#00A699;text-align: left;'>Details of the Accommodation</h2>'''
        st.markdown(head_text, unsafe_allow_html=True)

        c0,c1 = st.columns([2,2], gap='small')
        with c0:
            mydb.execute(f'''Select property_name,property_type,Price,Ratings,latitude,longitude from airbnb_listings
                where Country='{country_select}' and Street='{street_select}' and property_type = '{prop_select}';''')
            df0 = pd.DataFrame(mydb.fetchall(),columns=['Property_Name','Property_Type', 'Price', 'Review_scores', 'Latitude','Longitude'])
            df0[['Latitude','Longitude']] = df0[['Latitude','Longitude']].astype(float)
            st.write('')
            head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Geo visual of Accomodations</h5>'''
            st.markdown(head_text, unsafe_allow_html=True)
            fig = px.scatter_mapbox(df0, lat="Latitude", lon="Longitude",
                                            hover_name='Property_Name',zoom=10,
                                            hover_data={'Longitude':False,'Latitude':False, 'Price': True,'Property_Type':True},
                                            color_discrete_sequence=px.colors.colorbrewer.Set2)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig,use_container_width=True)
        with c1:
            st.write('')
            head_text = '''<h5 style='font-size: 28px;color:#00A699;text-align: left;'>Tabular view of Accomodations</h5>'''
            st.markdown(head_text, unsafe_allow_html=True)
            #if prop_select:
            mydb.execute(f'''Select property_name, property_type, Ratings from airbnb_listings 
                            where Country = '{country_select}' AND Street = '{street_select}' AND Property_type = '{prop_select}' 
                            ORDER BY Ratings DESC;''')
            df1 = pd.DataFrame(mydb.fetchall(), columns=['Property_Name','Property_type','Review_scores'])
            st.dataframe(df1,hide_index=True)
    st.write(' ')
    st.write(' ')
    head_text = '''<h3 style='font-size: 38px;color:#00A699;text-align: left;'>More details on the Accomodation</h3>'''
    st.markdown(head_text, unsafe_allow_html=True)
    mydb.execute(f'''Select distinct property_name as 'Name' from airbnb_listings where 
                        Country = '{country_select}' AND Street = '{street_select}' AND property_type = '{prop_select}';''')
    prop_name_df = pd.DataFrame(mydb.fetchall(), columns=['Name'])
    propname_select = st.selectbox("**Name**", options = prop_name_df['Name'].tolist(), index = None)
    if propname_select:
        mydb.execute(f'''Select property_name,property_type,description,room_type,bed_type,
            minimum_nights,maximum_nights,accommodates,bedrooms,
            beds,bathrooms,amenities,price,security_deposit,cleaning_fee,guests_included,
            host_name,host_id,Street,listing_url,Ratings,Location_Ratings from airbnb_listings
            where Country = '{country_select}' AND Street = '{street_select}' AND 
            property_type = '{prop_select}' AND property_name = '{propname_select}';''')
        df_main = pd.DataFrame(mydb.fetchall(),columns=['Property_Name', 'Property_Type','Description',
                    'Room_Type','Bed_Type','Min_Nights','Max_Nights','Accommodates','Bedrooms',
                    'Beds','Bathrooms','Amenities','Price','Security_fee','Cleaning_fee','Guests_included',
                    'Host_name','Host_id','Street','Listing_url','Ratings','Location_Ratings'])
        st.write('')
        st.write('')
        extract_detail = df_main.to_dict(orient='records')[0]
        c1,c2,c3=st.columns([2,1.5,1], gap = 'large')
        with c1:
                text = '''<h5 style='font-size: 24px;color:#D98880;text-align: left;'>🏡 Property & Room Details</h5>'''
                st.markdown(text, unsafe_allow_html=True)
                st.write("**:violet[Name :]**", extract_detail['Property_Name'])
                st.write("**:violet[Type :]**",extract_detail['Property_Type'])
                st.write("**:violet[Description :]**",extract_detail['Description'])
                st.write("**:violet[Country :]**",country_select)
                st.write("**:violet[Room :]**",extract_detail['Room_Type'])
                st.write("**:violet[Bedrooms :]**",extract_detail['Bedrooms'])
                st.write("**:violet[Accomodations :]**",extract_detail['Accommodates'])
                st.write("**:violet[Amenities :]**",extract_detail['Amenities'])
                st.write("**:violet[Price in $ :]**",extract_detail['Price'])
                st.write("**:violet[Assurance Deposit in $ :]**",extract_detail['Security_fee'])
                st.write("**:violet[Guest Included :]**",extract_detail['Guests_included'])

        with c2:
            text = '''<h5 style='font-size: 24px;color:#D98880;text-align: left;'>💁‍♀️ Host Details</h5>'''
            st.markdown(text, unsafe_allow_html=True)
            st.write("**:violet[Host Name :]**",extract_detail['Host_name'])
            st.write("**:violet[Host URL :]**",extract_detail['Listing_url'])
            st.write("**:violet[Host id :]**",extract_detail['Host_id'])
        with c3:
            text = '''<h5 style='font-size: 24px;color:#D98880;text-align: left;'>👈👉 Reviews </h5>'''
            st.markdown(text, unsafe_allow_html=True)
            st.write("**:violet[Overall Rating :]**",extract_detail['Ratings'])
            st.write("**:violet[Location Rating :]**",extract_detail['Location_Ratings'])
            st.write("**:violet[Street :]**",extract_detail['Street'])
if selected =="HOME":
        st.title(':violet[AirBnB - The Whats and Hows]')
        st.write('')
        c1,c2=st.columns([1,2],gap="large")
        with c2:
                st.subheader(':violet[What is AirBnB?]')
                st.markdown('''**Airbnb, Inc.**, is an American company operating an online marketplace for short- and long-term homestays and experiences, founded in :red[August 2008 in San Francisco, California, U.S.] by :red[Brian Chesky, Nathan Blecharczyk], and :red[Joe Gebbia].<p>
                            Airbnb is a shortened version of its original name, :red[AirBedandBreakfast.com]. The company acts as a broker and :red[charges a commission] from each booking.''',unsafe_allow_html=True)
                
                st.markdown("##### :violet[Learn more about Airbnb by clicking the button below!]")
                c0,c3 = st.columns([0.5,0.5])
                with c0:
                    st.link_button("Airbnb  - Website", "https://www.airbnb.co.in/")
                    st.link_button("Airbnb - news","https://news.airbnb.com/")
                with c3:
                    st.link_button("Airbnb - Career","https://careers.airbnb.com/")
                    st.link_button("Airbnb - Investors","https://investors.airbnb.com/home/default.aspx")
        with c1:  
                st.write(' ')    
                st.image('https://1000logos.net/wp-content/uploads/2017/08/Color-Airbnb-Logo.jpg', use_column_width=True)          
               
        c1,c2=st.columns([1.5,1.5],gap="large")
        with c1:
                st.subheader(':violet[How does AirBnB work?]')
                st.markdown('''The idea behind Airbnb is simple: matching local people with a :red[spare room] or :red[entire home to rent] to others who are visiting the area. 
                            Hosts using the platform get to :red[advertise their rentals] to millions of people worldwide, with the reassurance that a big company will handle payments 
                            and offer other support. And for guests, Airbnb can provide a homey place to stay, perhaps with a kitchen to save on dining out, often at a lower price than hotels charge.
                            Today, the company operates in over :red[220 countries] and regions, including the US, Europe, Australia, and Asia.''',unsafe_allow_html=True)
        
        with c2:   
                st.subheader(':violet[How Does Airbnb Make Money?]')
                st.markdown('''Airbnb's business model is :red[quite profitable]. The company like Uber, Lyft, and others, has capitalized on the so-called sharing economy, essentially :red[making money renting out property that it doesn't own.] 
                            Every time someone books a stay, Airbnb takes a cut. When customers click on a property, they'll see a breakdown of the fees they'll be charged if they proceed. As mentioned, guest fees typically max out at :red[14.2%], 
                            while hosts generally pay about 3% of the amount they take in.''',unsafe_allow_html=True)
        
        st.title(':violet[Airbnb - Growth over the years]')
        c1,c2=st.columns([1,2], gap = "large")
        
        with c1:
                st.subheader(':violet[Chronological History of Airbnb:]')
                st.markdown('''From their inception to the present, Airbnb has travelled far and done wonders in the tourism and hotel industry.
                            ''')
                st.image('https://rubygarage.s3.amazonaws.com/uploads/article_image/file/2940/Success_timeline_Airbnb_1x.png',width = 320)
                
        with c2:
                st.subheader(':violet[Airbnb Outstanding Aquisitions:]')
                st.markdown('''With its focus on setting a milestone in the lodging and hospitality industry, Airbnb has acquired several companies since its launch.
                            The below chart gives an idea about that.''',unsafe_allow_html=True)
                st.write('')
                st.image('https://techreport.com/wp-content/uploads/2024/01/Airbnb-Outstanding-Acquisitions-e1706379656241.png', use_column_width=True)
                st.write('')
                st.write('')
                st.subheader(':violet[Airbnb Bookings & Gross Booking Value:]')
                st.markdown('''With operations in more than 100,000 cities worldwide and over 220 regions and countries, Airbnb has seen millions of bookings with their valuation reaching about 60 billion dollars in 2023.
                            With the numbers still increasing, the below chart gives a good visualization of the bookings till 2023. ''',unsafe_allow_html=True)
                st.write('')
                st.image('https://techreport.com/wp-content/uploads/2024/01/Booking-Statistics-e1706378120150.jpeg', use_column_width=True)
                
        st.write('')
        st.header(':violet[Learn more about Airbnb]')
        col1,col2,col3,col4=st.columns([1,1,1,1])
        with col1:
                st.video('https://www.youtube.com/watch?v=dA2F0qScxrI&list=PLe_YVMnS1oXZb4zCNsh_fRqXh5kgx21V_')
        with col2:
                st.video('https://www.youtube.com/watch?v=oh3lnb9Wj08')
        with col3:
                st.video('https://youtu.be/D1MzAMdnoRw?si=ec4Yssi6EAK0n5yj')
        with col4:
                st.video('https://youtu.be/Uet-GeWdKK4?si=K-Uln2EKwui2CLWl')
