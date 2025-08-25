import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title = 'Tattva Portal',
    page_icon='image.png',

)
st.title(':rainbow[Tattva Portal]')
st.subheader(':grey[Explore and visualize your data with ease!]',divider='red')

file = st.file_uploader('Upload your csv or excel file',type=['csv','xlsx'])
if file !=None:
    if file.name.endswith('csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    st.dataframe(df)
    st.info('Your file has been successfully uploaded!')
    st.subheader('Basic Information about your data',divider ='red')
    # tabs
    tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top and Bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {df.shape[0]} rows in dataset and {df.shape[1]} columns in dataset')
        st.subheader(':grey[Statistical Summary of Numerical Columns]')
        st.write(df.describe())
        st.subheader(':grey[Statistical Summary of Categorical Columns]')
        st.write(df.describe(include='object'))
        st.subheader(':grey[Missing Values in Each Column]')
        st.write(df.isnull().sum())
        st.subheader(':grey[Duplicate Rows in Dataset]')
        st.write(df.duplicated().sum())
    with tab2:
        st.subheader(':grey[Top Rows]')
        # user input in streamlit default 5
        n = st.number_input("Enter number of rows:", min_value=1, max_value=len(df), value=5)
        # toprows = st.slider('Number of rows you want',1,df.shape[0],key='topslider')
        st.write(df.head(n))
        st.subheader(':grey[Bottom Rows]')
        st.write(df.tail(n))
    with tab3:
        st.subheader(':grey[Data Types of Each Column]')
        st.dataframe(df.dtypes)
    with tab4:
        st.subheader(':grey[Column Names in Dataset]')
        st.write(list(df.columns))
    
    st.subheader('Column Values To Count',divider='red')
    with st.expander('Value count'):
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Names',options = list(df.columns))
        with col2:
            toprows = st.number_input('Choose number of Top Rows',min_value=1,step=1,max_value=len(df))

        count = st.button('Count')
        if count == True:
            result = df[column].value_counts().reset_index().head(toprows)
            result.columns = [column, 'count']   # rename columns properly
            st.dataframe(result)
            st.subheader('Visualization of Column Values',divider='red')

            fig = px.bar(data_frame=result,x = column,y ='count',text = 'count')
            st.plotly_chart(fig)

            fig = px.line(data_frame = result,x = column,y = 'count',text = 'count')
            st.plotly_chart(fig)

            fig  = px.pie(data_frame = result,names = column,values = 'count')
            st.plotly_chart(fig)
    
    st.subheader('Groupby : Simplify your Data Analysis',divider ='red')
    st.write('The groupby lets you summarized your data based on a specific column and perform various aggregations on other columns like sum,mean,count etc. This is useful for understanding patterns and trends within different groups in your dataset.')
    with st.expander('Groupby your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your columns to groupby',options = list(df.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options = list(df.columns))
        with col3:
            operation = st.selectbox('choose operation to perform',options = ['sum','mean','count','max','min','median','std','var','all'])
        if groupby_cols:
            result = df.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()
            st.dataframe(result)

            st.subheader('Data Visualization',divider='red')
            graphs = st.selectbox('Choose your Graph',options = ['line','bar','pie','scatter','sunburst'])
            if graphs =='line':
                x_axis = st.selectbox('Choose X axis',options = list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options = list(result.columns))
                color = st.selectbox('Choose color',options=[None]+list(result.columns))
                fig = px.line(data_frame=result,x = x_axis,y = y_axis,color = color,markers='o')
                st.plotly_chart(fig)
            elif graphs == 'bar':
                x_axis = st.selectbox('Choose X axis',options = list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options = list(result.columns))
                color = st.selectbox('Choose color',options=[None]+list(result.columns))
                facet_col = st.selectbox('Column Information',options=[None]+list(result.columns))
                fig = px.bar(data_frame = result,x = x_axis,y = y_axis,color = color,facet_col = facet_col,barmode = 'group')
                st.plotly_chart(fig)
            elif graphs == 'scatter':
                x_axis = st.selectbox('Choose X axis',options = list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options = list(result.columns))
                color = st.selectbox('Choose color',options=[None]+list(result.columns))
                size = st.selectbox('Size Column',options = [None] + list(result.columns))
                fig = px.scatter(data_frame=result,x = x_axis,y = y_axis,color = color,size = size)
                st.plotly_chart(fig)
            elif graphs == 'pie':
                values = st.selectbox('Choose Numerical Values',options = list(result.columns))
                names = st.selectbox('Choose labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values = values,names = names)
                st.plotly_chart(fig)
            elif graphs == 'sunburst':
                path = st.multiselect('Choose path',options = list(result.columns))
                fig = px.sunburst(data_frame=result,path = path,values = 'newcol')
                st.plotly_chart(fig)


            

    
        

