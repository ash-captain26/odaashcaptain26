import numpy as np
import seaborn as sns

#creating a input output function
def fetch_medal_tally(df, year, country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag =0
    if year=='Overall' and country=='Overall':
        
        temp_df=medal_df
    if year=='Overall' and country!='Overall':
        flag=1
        var=(medal_df['region']==country)
        temp_df= medal_df[var]
    if year!='Overall' and country=='Overall':
        var=(medal_df['Year']==int(year))
        temp_df= medal_df[var]
    if year!='Overall' and country!='Overall':
        var=(medal_df['Year']==int(year))& (medal_df['region']==country)
        temp_df= medal_df[var]
    if flag ==1:    
        var = temp_df.groupby('Year').agg({'Gold':'sum','Silver':'sum','Bronze':'sum'})
        x = var.sort_values('Year',ascending=False)
    else:
        var = temp_df.groupby('region').agg({'Gold':'sum','Silver':'sum','Bronze':'sum'})
        x = var.sort_values('Gold',ascending=False)
    x['Gold']=x['Gold'].astype('int')
    x['Silver']=x['Silver'].astype('int')
    x['Bronze']=x['Bronze'].astype('int') 
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    x['Total']=x['Total'].astype('int')  
    return x




def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    df_new=medal_tally.groupby('NOC').agg({'Gold':'sum','Silver':'sum','Bronze':'sum'})
    medal_tally= df_new.sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['Total']=medal_tally['Total'].astype('int')
    return medal_tally

#overall analysis
def country_year_list(df):
    year= sorted(df['Year'].unique().tolist())
    year.insert(0,'Overall')

    country = sorted(np.unique(df['region'].dropna().values).tolist())
    country.insert(0,"Overall")

    return year, country

def part_nations(df, col):
    nat_part = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index()
    nat_part.columns=['Year',col]
    nat_part= nat_part.sort_values('Year', ascending= False)
    return nat_part

def most_successful(df, sport):
    #require only those athele who have won medals
    temp_df= df.dropna(subset=["Medal"])
    if sport != "Overall":
        var= (temp_df['Sport']==sport)
        temp_df= temp_df[var]
        result=  temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index',right_on='Name',how='left')
       
        x=result[['index','Name_x','Sport','region']].drop_duplicates('index')
        x.columns=['Name','Medals','Sport','region']
        return x
    else:
        result= temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index',right_on='Name',how='left')
        x=result[['index','Name_x','Sport','region']].drop_duplicates('index')
        x.columns=['Name','Medals','Sport','region']
        return x
    

def year_wise_medal_tally(df,country):
    temp_df=df.dropna(subset="Medal")
    #when a team wins in grp tournament its members all are given medals so inorder to remove that we need to drop the 
    #duplicates values
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'], inplace= True)
    var=(temp_df['region']== country)
    temp_df=temp_df[var]
    new_df=temp_df.groupby('Year').agg({'Medal':'count'}).reset_index()
    return new_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset="Medal")
    #when a team wins in grp tournament its members all are given medals so inorder to remove that we need to drop the 
    #duplicates values
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'], inplace= True)
    var=(temp_df['region']== country)
    new_df=temp_df[var]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(['Name','region'])
    athlete_df['Medal'].fillna("No Medal", inplace=True)
    if sport !='Overall':
        var= (athlete_df['Sport']== sport)
        temp_df=athlete_df[var]
        return temp_df
    else:
        return athlete_df

def men_v_women(df):
    athlete_df=df.drop_duplicates(['Name','region'])
    var=(athlete_df['Sex']=='M')
    male_df=athlete_df[var].groupby('Year').agg({'Sex':'count'}).reset_index()
    temp=(athlete_df['Sex']=='F')
    female_df=athlete_df[temp].groupby('Year').agg({'Sex':'count'}).reset_index()
    athlete_sex=male_df.merge(female_df, on="Year", how="left")
    athlete_sex.columns=['Year','Male','Female']
    athlete_sex.fillna(0,inplace=True)
    return athlete_sex
