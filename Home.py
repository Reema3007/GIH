import streamlit as st
from matplotlib import pyplot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
from sqlalchemy import text
import pandas as pd
import altair as alt

def level_chart(state,level):
    state_param = "'"+"','".join(state)+"'"
    level_param = "'"+"','".join(level)+"'"
    query = f'select level, sum(Male) Male,sum(Female) Female, sum(Male)+sum(Female) total from Snowflake_GIH.GIH.DataReport_RegionalCourse where level in ({level_param}) and statename in ({state_param}) group by level'
    print(query)
    pd_level_chart = pd.read_sql(query,con=engine)
    # pd_level_chart
    df =  pd.DataFrame(
    {
        'Level': pd_level_chart['level'],
        'Male': pd_level_chart['male'],
        'Female': pd_level_chart['female']
    },
    columns=['Level', 'Male', 'Female']
    )
    title = alt.TitleParams('Level(Education) Wise Insights', anchor='middle')
    df = df.melt('Level', var_name='name', value_vars=['Male','Female'])
    c = alt.Chart(df,title=title).mark_bar().encode(
       x=alt.X('value', axis=alt.Axis(labels=False,title=""),stack='zero'), 
       y=alt.Y('Level',axis=alt.Axis(title="")).sort('-x'), 
       color=alt.Color("name:N",legend=alt.Legend(title="")),
       tooltip=[alt.Tooltip('name', title="  "),alt.Tooltip('value:N', title=" ")])
    
    text = alt.Chart(df).mark_text(dy=-15, color='white').encode(
    x=alt.X('value', axis=alt.Axis(labels=False,title=""))) 
    st.altair_chart(c+text, use_container_width=True, theme="streamlit")

def state_level_chart(state,level):
    state_param = "'"+"','".join(state)+"'"
    level_param = "'"+"','".join(level)+"'"
    query = f'select statename,level,male+female as total from Snowflake_GIH.GIH.STATE_LEVEL_VIEW where level in ({level_param}) and statename in ({state_param})'
    pd_level_chart = pd.read_sql(query,con=engine)
    # pd_level_chart
    df =  pd.DataFrame(
    {
        'State': pd_level_chart['statename'],
        'Level': pd_level_chart['level'],
        'Total': pd_level_chart['total']
    },
    columns=['State', 'Level', 'Total']
    )
    # df
    # df = df.melt('Level', var_name='name', value_vars=['Male','Female'])
    title = alt.TitleParams('State Wise Insights', anchor='middle')
    c = alt.Chart(df, title=title).mark_bar().encode(
       x=alt.X('Total',axis=alt.Axis(labels=False,title=""),stack='zero'), 
       y=alt.Y('State',axis=alt.Axis(title="")).sort('-x'), 
       color=alt.Color("Level:N",legend=alt.Legend(title=""))
       # tooltip=[alt.Tooltip('name', title="  "),alt.Tooltip('value:N', title=" ")]
       )
    
    text = alt.Chart(df).mark_text(dy=-15, color='white').encode(
    x=alt.X('Level', axis=alt.Axis(labels=False,title="")))  
    st.altair_chart(c+text, use_container_width=True, theme="streamlit")
    
def district_level_chart(state,level):
    state_param = "'"+"','".join(state)+"'"
    level_param = "'"+"','".join(level)+"'"
    query = f'select statename,districtregionalcenter as district,level,male+female as total from Snowflake_GIH.GIH.DISTRICT_LEVEL_VIEW where level in ({level_param}) and statename in ({state_param})'
    pd_level_chart = pd.read_sql(query,con=engine)
    # pd_level_chart
    df =  pd.DataFrame(
    {
        'District': pd_level_chart['district'],
        'Level': pd_level_chart['level'],
        'Total': pd_level_chart['total']
    },
    columns=['District', 'Level', 'Total']
    )
    # df
    # df = df.melt('Level', var_name='name', value_vars=['Male','Female'])
    title = alt.TitleParams('Region Wise Insights', anchor='middle')
    c = alt.Chart(df,title=title).mark_bar().encode(
       x=alt.X('Total',axis=alt.Axis(labels=False,title=""),stack='zero'), 
       y=alt.Y('District',axis=alt.Axis(title="")).sort('-x'), 
       color=alt.Color("Level:N",legend=alt.Legend(title=""))
       # tooltip=[alt.Tooltip('name', title="  "),alt.Tooltip('value:N', title=" ")]
       )
    
    text = alt.Chart(df).mark_text(dy=-15, color='white').encode(
    x=alt.X('Level', axis=alt.Axis(labels=False,title="")))  
    st.altair_chart(c+text, use_container_width=True, theme="streamlit")

def chart_function(state,level):
    state_param = "'"+"','".join(state)+"'"
    level_param = "'"+"','".join(level)+"'"    
    query = f'select Sum(FEMALE)+Sum(male) as Total, sum(Male) as Male, sum(Female) as Female from Snowflake_GIH.GIH.STATE_LEVEL_VIEW where STATENAME in ({state_param}) and LEVEL in ({level_param})'
    pd_total_summary = pd.read_sql(query,con=engine)
    # pd_total_summary
    # pd_total_summary["total"]
    col1, col2, col3 = st.columns(3)    
    with col1:
        tile = col1.container(height=105)
        tile.metric(label="Total Enrollments", value=f'{int(pd_total_summary["total"]):,d}',help="Total number of student enrolled for Regional Courses")
    with col2:
        tile = col2.container(height=105)
        tile.metric(label="Male", value=f'{int(pd_total_summary["male"]):,d}',help="Total number of Male students enrolled for Regional Courses")
    with col3:
        tile = col3.container(height=105)
        tile.metric(label="Female", value=f'{int(pd_total_summary["female"]):,d}',help="Total number of Female students enrolled for Regional Courses")
    
    col1,col2 = st.columns(2)
    with col1:
        with st.container(height=200):
            level_chart(state,level)
    with col2:
        with st.container(height=200):
            state_level_chart(state,level)
    with st.container(height=300):
        district_level_chart(state,level)
        
    # Display the chart in Streamlit


engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user='REEMA3007',
        password='Reema3007',
        account_identifier='znioaaf-qhb92981',
    )
)
connection = engine.connect()
try:
    print('Start')
    
    with st.form(key="my_form"):
        col1, col2, col3 = st.columns([0.5,0.5,0.25],gap="medium",vertical_alignment="center")
        state_sql = pd.read_sql("Select distinct statename as state from Snowflake_GIH.GIH.state_level_view",con=engine)
        level_sql = pd.read_sql("select distinct Level as level from Snowflake_GIH.GIH.LEVEL_WISE;",con=engine)
        with col1:
            container = st.container()
            options_state =  container.multiselect("State",state_sql["state"],placeholder="All States are selected")
            if len(options_state) == 0:
                state_value = state_sql["state"]
            else:
                state_value = options_state
        with col2:
            container = st.container()
            options_level = container.multiselect(
                    "Level of Education",
                    level_sql['level'],
                    placeholder="All Levels are selected"
                )
            if len(options_level)==0:
                level_value = level_sql["level"]
            else:
                level_value=options_level
        with col3:
            st.write('\n\n\n\n')
            filtered = st.form_submit_button("\nFilter", type="primary",use_container_width=True)
    if(filtered):
        chart_function(state_value,level_value)
    else:
        chart_function(state_value,level_value)
    
finally:
    connection.close()
    engine.dispose()
    