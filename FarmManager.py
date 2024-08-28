import pandas as pd
import streamlit as st

# Sample data
farm_data = {
    'Farm Name': ['Farm A', 'Farm B', 'Farm C'],
    'Location': ['Location A', 'Location B', 'Location C'],
    'Crop': ['Wheat', 'Corn', 'Soybean'],
    'Livestock': ['Cattle', 'Pigs', 'Chickens'],
    'Area (acres)': [100, 200, 150],
    'Livestock Count': [50, 200, 150],
    'Feeding Schedule': ['Twice a day', 'Three times a day', 'Once a day'],
    'Health Status': ['Good', 'Excellent', 'Fair']
}

# Initialize the session state if it doesn't already exist
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(farm_data)

# Streamlit app layout
st.title('Farm Management App')
st.write(" ")

# Sidebar with options
st.sidebar.title('Menu')
page = st.sidebar.radio('Select a page', ['Home', 'Crop Management', 'Livestock Tracking', 'Tasks', 'Change Info'])
df = st.session_state.df

if page == 'Home':
    st.subheader('Farm Overview')
    st.write(" ")
    st.write(df)  # Display farm data

elif page == 'Crop Management':
    st.subheader('Crop Management')
    st.write(" ")
    st.write('Select a crop to manage:')
    selected_crop = st.selectbox('Select Crop', df['Crop'].unique())
    crop_info = df[df['Crop'] == selected_crop].iloc[0]
    st.write(f"*Crop Name:* {crop_info['Crop']}")
    st.write(f"*Farm Name:* {crop_info['Farm Name']}")
    st.write(f"*Location:* {crop_info['Location']}")
    st.write(f"*Area (acres):* {crop_info['Area (acres)']}")

elif page == 'Livestock Tracking':
    st.subheader('Livestock Tracking')
    st.write(" ")
    st.write('Select a livestock to track:')
    selected_livestock = st.selectbox('Select Livestock', df['Livestock'].unique())
    livestock_info = df[df['Livestock'] == selected_livestock].iloc[0]
    st.write(f"*Livestock Type:* {livestock_info['Livestock']}")
    st.write(f"*Farm Name:* {livestock_info['Farm Name']}")
    st.write(f"*Location:* {livestock_info['Location']}")
    st.write(f"*Area (acres):* {livestock_info['Area (acres)']}")
    st.write(f"*Livestock Count:* {livestock_info['Livestock Count']}")
    st.write(f"*Feeding Schedule:* {livestock_info['Feeding Schedule']}")
    st.write(f"*Health Status:* {livestock_info['Health Status']}")

    new_health_status = st.selectbox(
        'Change Health Status',
        ['Good', 'Fair', 'Poor', 'Excellent'],
        index=['Good', 'Fair', 'Poor', 'Excellent'].index(livestock_info['Health Status'])
    )

    if st.button('Update Health Status'):
        df.loc[df['Livestock'] == selected_livestock, 'Health Status'] = new_health_status
        st.session_state.df = df  # Update session state
        st.write(f"Health status of {selected_livestock} updated to {new_health_status}")
        livestock_info = df[df['Livestock'] == selected_livestock].iloc[0]
        st.write(f"*Health Status:* {livestock_info['Health Status']}")

elif page == 'Tasks':
    st.subheader('Task Management')
    st.write(" ")
    
    st.write('Manage your farm tasks here.')
    
    # Add New Task
    task = st.text_area('Enter a new task')
    if st.button('Add Task'):
        st.write(f'New task added: {task}')
    

elif page == 'Change Info':
       
    st.write('Add a new farm:')
    with st.form(key='add_farm'):
        farm_name = st.text_input('Farm Name')
        location = st.text_input('Location')
        area_acres = st.number_input('Area (acres)', min_value=0)
        submit_farm = st.form_submit_button('Add Farm')
        if submit_farm and farm_name:
            new_farm = {
                'Farm Name': [farm_name],
                'Location': [location],
                'Crop': [None],  
                'Livestock': [None],  
                'Area (acres)': [area_acres],
                'Livestock Count': [0],  
                'Feeding Schedule': [None],  
                'Health Status': [None]  
            }
            new_farm_df = pd.DataFrame(new_farm)
            df = pd.concat([df, new_farm_df], ignore_index=True)
            st.session_state.df = df  
            st.write(f'Farm "{farm_name}" added.')

    st.write('Add a new crop:')
    with st.form(key='add_crop'):
        crop_name = st.text_input('Crop Name')
        farm_name_crop = st.selectbox('Farm Name', df['Farm Name'].unique())
        submit_crop = st.form_submit_button('Add Crop')
        if submit_crop and crop_name:
            df.loc[df['Farm Name'] == farm_name_crop, 'Crop'] = crop_name
            st.session_state.df = df  
            st.write(f'Crop "{crop_name}" added to farm "{farm_name_crop}".')

    
    st.write('Add new livestock:')
    with st.form(key='add_livestock'):
        livestock_type = st.text_input('Livestock Type')
        farm_name_livestock = st.selectbox('Farm Name', df['Farm Name'].unique())
        count = st.number_input('Count', min_value=0)
        feeding_schedule = st.selectbox('Feeding Schedule', ['Twice a day', 'Three times a day', 'Once a day'])
        health_status = st.selectbox('Health Status', ['Good', 'Fair', 'Poor', 'Excellent'])
        submit_livestock = st.form_submit_button('Add Livestock')
        if submit_livestock and livestock_type:
            new_livestock = {
                'Farm Name': [farm_name_livestock],
                'Location': [df[df['Farm Name'] == farm_name_livestock]['Location'].values[0]],
                'Crop': [None],  
                'Livestock': [livestock_type],
                'Area (acres)': [df[df['Farm Name'] == farm_name_livestock]['Area (acres)'].values[0]],
                'Livestock Count': [count],
                'Feeding Schedule': [feeding_schedule],
                'Health Status': [health_status]
            }
            new_livestock_df = pd.DataFrame(new_livestock)
            df = pd.concat([df, new_livestock_df], ignore_index=True)
            st.session_state.df = df 
            st.write(f'Livestock "{livestock_type}" added to farm "{farm_name_livestock}".')
