import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
#********* Data Cleaning **************************
filename = 'IBM ICE- Consolidated Student Count.xlsx'
main_data = pd.read_excel(filename)
main_data['University'].ffill(inplace=True)
null_idx = main_data[main_data['Batch'].isnull()].index
main_data.drop(index=null_idx,inplace=True)
main_data.drop(columns='Total',inplace=True)
main_data.Batch = main_data.Batch.astype(dtype="category")
main_data.University = main_data.University.astype(dtype='category')
main_data.iloc[:,2:] = main_data.iloc[:,2:].fillna(value=0)
main_data.iloc[:,2:] = main_data.iloc[:,2:].astype(dtype='int')
#*************** Plotting Functions **********************
def students_per_course(data):
    courses = data.iloc[:,2:].sum(axis=0).index
    students = data.iloc[:,2:].sum(axis=0).values
    count_df = pd.DataFrame({'course':courses,'no of students':students})
    fig = px.pie(count_df,values='no of students',names='course',title='Course Wise Strength')
    fig.update_traces(textposition = 'inside', textinfo='percent+label')
    return fig

def students_per_batch(data):
    hist = data.groupby(['Batch','University']).sum().sum(1).unstack('University').sum(1)
    if any(hist.values):
        hist = hist + .1
    else:
        pass

    fig = px.histogram(x=hist.index,y=hist,height=450,width=610,
    title="Batch Wise Strength",
    color_discrete_sequence=['yellow'])
    fig.update_layout(
    xaxis_title="",
    yaxis_title="") 
    return fig

def course_trend(data,course_list):
    g_df = data.groupby(['Batch']).sum()
    g_df['Batch'] = g_df.index
    result = pd.melt(g_df,id_vars='Batch',value_name='count')
    result.columns = ['Batch','Course','Strength']
    check_course = lambda x:any([x == e for e in course_list])
    result = result[result.Course.map(check_course)]
    fig = px.line(result,x='Batch',y='Strength',color='Course',text='Course') # ,title='Course Trends'
    fig.update_yaxes(showgrid=False)
#     fig.update_xaxes(showgrid=False)
    return fig

def batch_hist(data,year=None):
    g_df = data.groupby(['Batch']).sum()
    g_df['Batch'] = g_df.index
    result = pd.melt(g_df,id_vars='Batch',value_name='count')
    result.columns = ['Batch','Course','Strength']
    if year:
        result = result[result.Batch==year]
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=result.Strength,
        y=result.Course,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),),
        name='current running courses',
        orientation='h',
    ))
#     fig.update_layout(title='Course Trends')
    return fig
#******************* Main **********************


st.title('IBM ICE (Innovation Centre for Education)')

Universities = list(main_data.University.unique())
Universities.insert(0,'All')
selected_uni = st.selectbox(label = "SELECT THE UNIVERSITY" ,options = Universities)

if selected_uni != 'All':
    st.subheader('Analysing {} University'.format(selected_uni))
    data = main_data[main_data.University==selected_uni]
    total_students = data.iloc[:,2:].values.sum()
    st.write('Total Strength : ',total_students)
    st.write(students_per_course(data))
    st.write(students_per_batch(data))
    st.subheader('Course Trend')
    st.write('tick the courses')
    selections = []
    courses = np.array(main_data.columns[2:])
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        for course in courses[:4]:
            selections.append(st.checkbox(course))
    with c2:
        for course in courses[4:8]:
            selections.append(st.checkbox(course))
    with c3:
        for course in courses[8:12]:
            selections.append(st.checkbox(course))
    with c4:
        for course in courses[12:16]:
            selections.append(st.checkbox(course))
    selections = np.array(selections)
    st.write(course_trend(data,courses[selections]))
    #**************
    batches = np.array(['All']+list(data.Batch.unique()))
    st.subheader('Course Strength')
    year = st.selectbox(label='select a batch',options=batches)
    if year!='All':
        figure = batch_hist(data,year)
        st.write(figure)
    else:
        figure = batch_hist(data)
        st.write(figure)
else:
    st.subheader('Overall Analysis')
    data = main_data
    total_students = data.iloc[:,2:].values.sum()
    st.write('Total Strength : ',total_students)
    st.write(students_per_course(data))
    st.write(students_per_batch(data))
    st.subheader('Course Trend')
    st.write('tick the courses')
    selections = []
    courses = np.array(data.columns[2:])
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        for course in courses[:4]:
            selections.append(st.checkbox(course))
    with c2:
        for course in courses[4:8]:
            selections.append(st.checkbox(course))
    with c3:
        for course in courses[8:12]:
            selections.append(st.checkbox(course))
    with c4:
        for course in courses[12:16]:
            selections.append(st.checkbox(course))
    selections = np.array(selections)
    st.write(course_trend(data,courses[selections]))
    #****************
    batches = np.array(['All']+list(data.Batch.unique()))
    st.subheader('Course Strength')
    year = st.selectbox(label='select a batch',options=batches)
    if year!='All':
        figure = batch_hist(data,year)
        st.write(figure)
    else:
        figure = batch_hist(data)
        st.write(figure)


# Universities = list(main_data.University.unique())
# Universities.insert(0,'All')
# selected_uni = st.selectbox(label = "SELECT THE UNIVERSITY" ,options = Universities)

# if selected_uni != 'All':
#     st.header('Analysing {} University'.format(selected_uni))
#     data = main_data[main_data.University==selected_uni]
#     total_students = data.iloc[:,2:].values.sum()
#     st.write('Total Strength : ',total_students)
#     st.write(students_per_course(data))
#     st.write(students_per_batch(data))

#     st.write('tick the courses')
#     selections = []
#     courses = np.array(main_data.columns[2:])
#     c1,c2,c3,c4 = st.columns(4)
    
#     with c1:
#         for course in courses[:4]:
#             selections.append(st.checkbox(course))
#     with c2:
#         for course in courses[4:8]:
#             selections.append(st.checkbox(course))
#     with c3:
#         for course in courses[8:12]:
#             selections.append(st.checkbox(course))
#     with c4:
#         for course in courses[12:16]:
#             selections.append(st.checkbox(course))
#     selections = np.array(selections)    
#     st.write(course_trend(data,courses[selections]))
#     #**************
#     batches = np.array(['All']+list(data.Batch.unique()))
#     year = st.selectbox(label='select a batch',options=batches)
#     if year!='All':
#         figure = batch_hist(data,year)
#         st.write(figure)
#     else:
#         figure = batch_hist(data)
#         st.write(figure)
# else:
#     st.header('Overall Analysis')
#     data = main_data
#     total_students = data.iloc[:,2:].values.sum()
#     st.write('Total Strength : ',total_students)
#     st.write(students_per_course(data))
#     st.write(students_per_batch(data))

#     st.write('tick the courses')
#     selections = []
#     courses = np.array(data.columns[2:])
#     c1,c2,c3,c4 = st.columns(4)
    
#     with c1:
#         for course in courses[:4]:
#             selections.append(st.checkbox(course))
#     with c2:
#         for course in courses[4:8]:
#             selections.append(st.checkbox(course))
#     with c3:
#         for course in courses[8:12]:
#             selections.append(st.checkbox(course))
#     with c4:
#         for course in courses[12:16]:
#             selections.append(st.checkbox(course))
#     selections = np.array(selections)    
#     st.write(course_trend(data,courses[selections]))
#     #****************
#     batches = np.array(['All']+list(data.Batch.unique()))
#     year = st.selectbox(label='select a batch',options=batches)
#     if year!='All':
#         figure = batch_hist(data,year)
#         st.write(figure)
#     else:
#         figure = batch_hist(data)
#         st.write(figure)
