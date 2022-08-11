from email.utils import collapse_rfc2231_value
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import preprocessor, helper
import plotly.figure_factory as ff

df= pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympic Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an option ',
    ('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)
# Country as well as year analysis
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally= helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_country=="Overall":
        if selected_year =="Overall": 
            st.title("Overall Tally")
        else:
            st.title("Medal Tally in "+str(selected_year)+" Olympics")
    else:
        if selected_year=="Overall":
            st.title(selected_country+" Overall Performance")
        else:
            st.title(selected_country + " Medal Tally in "+ str(selected_year))
    st.table(medal_tally)

#overall analysis

if user_menu == 'Overall Analysis':
    st.title("Overall Statistics")
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3= st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)   

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Atheletes")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations) 

    nat_part= helper.part_nations(df,'region')
    fig = px.line(nat_part, x='Year', y='region')
    st.title("Paticipating Nations over the years")
    st.plotly_chart(fig)

    event_part= helper.part_nations(df,'Event')
    fig = px.line(event_part, x='Year', y='Event')
    st.title("Paticipating Events over the years")
    st.plotly_chart(fig)

    athlete_part= helper.part_nations(df,'Name')
    fig = px.line(athlete_part, x='Year', y='Name')
    st.title("Paticipating Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of events over time (Every Sport)")
    fig, ax= plt.subplots(figsize = (13,13))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax= sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'), annot= True)
    st.pyplot(fig)

    st.title('Most succesful Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport= st.selectbox('Select a sport', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == "Country wise Analysis":
    st.sidebar.title("Country wise analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a country", country_list)
    country_df= helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country +" excels in following sports")
    pt=helper.country_event_heatmap(df, selected_country)
    fig, ax= plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    
if user_menu == "Athlete wise Analysis":
    athlete_df=df.drop_duplicates(['Name','region'])
    x1=athlete_df['Age'].dropna()
    var1=(athlete_df['Medal']=='Gold')
    var2=(athlete_df['Medal']=='Silver')
    var3=(athlete_df['Medal']=='Bronze')
    x2=athlete_df[var1]['Age'].dropna()
    x3=athlete_df[var2]['Age'].dropna()
    x4=athlete_df[var3]['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medallist','Silver Medallist','Bronze Medallist']
    , show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    x=[]
    name=[]
    for sport in famous_sports:
        var1=(athlete_df['Sport']== sport)
        temp_df=athlete_df[var1]
        var2=(temp_df[var1]['Medal']=='Gold')
        temp_lst=temp_df[var2]['Age'].dropna()
        x.append(temp_lst)
        name.append(sport)

    fig= ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age among Gold Medallist")
    st.plotly_chart(fig)

    st.title("Height v/s Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport= st.selectbox('Select a sport', sport_list)
    temp_df= helper.weight_v_height(df, selected_sport)
    fig, ax= plt.subplots()
    ax= sns.scatterplot(temp_df['Weight'],temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=30)
    st.pyplot(fig)

    st.title("Men v/s Women participation over the years")
    final = helper.men_v_women(df)
    fig= px.line(final, x='Year', y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



