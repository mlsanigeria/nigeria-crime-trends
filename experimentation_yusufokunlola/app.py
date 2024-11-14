# import libraries
import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder

# Set up page configuration
st.set_page_config(page_title="Nigeria-Crime-Trends", page_icon="📝")

# Title and description
st.title("Nigeria Crime Trends Prediction App")

# Data cleaning function
def wrangle_data(filepath):
    # Load the dataset
    data = pd.read_csv(filepath)

    # Convert 'event_date' to datetime format
    data['event_date'] = pd.to_datetime(data['event_date'])

    # Extract month and day into new columns and convert them to int64
    data['month'] = data['event_date'].dt.month.astype('int64')
    data['day'] = data['event_date'].dt.day.astype('int64')

    # List of columns to extract for the app interface
    # Note: The feature 'notes' isn't included as it contained a brief summary of the event
    columns_to_extract = ['year', 'month', 'time_precision', 'disorder_type',  'event_type', 
                          'sub_event_type', 'actor1', 'inter1', 'actor2', 'inter2', 'interaction', 
                          'civilian_targeting', 'admin1', 'admin2', 'location', 'geo_precision', 
                          'source', 'source_scale',  'fatalities'
                    ]

    # Create a copy of the dataset with the specified columns
    df = data[columns_to_extract].copy()

    # Replace NaN values in 'actor2' with 'Not available' as it was recorded that it can be blank
    df['actor2'] = df['actor2'].fillna('Not available')
    
    # Replace NaN values in 'civilian_targeting' with 'Not Civilian targeting' as it was recorded that it can be blank
    df['civilian_targeting'] = df['civilian_targeting'].fillna('Not Civilian targeting')

    # Rename values in 'civilian_targeting' with 'Yes' or 'No'
    df['civilian_targeting'] = df['civilian_targeting'].replace({'Not Civilian targeting': 'No', 'Civilian targeting': 'Yes'})

    # The row 'admin2' or 'admin1' had 1 missing value and had to be dropped because the location was the Gulf of Guinea; international waters
    df = df.dropna(subset=['admin2', 'admin1'])
    
    # Replace source values with counts less than 100 with 'Other'  
    df['source'] = df['source'].replace(df['source'].value_counts()[df['source'].value_counts() < 100].index, 'Other')

    # Replace actor1 values with counts less than 100 with 'Other'
    df['actor1'] = df['actor1'].replace(df['actor1'].value_counts()[df['actor1'].value_counts() < 100].index, 'Other')
    
    # Replace actor2 values with counts less than 100 with 'Other'
    df['actor2'] = df['actor2'].replace(df['actor2'].value_counts()[df['actor2'].value_counts() < 100].index, 'Other')
    
    # Drop duplicates
    df = df.drop_duplicates()

    return df


# label encoding and categorical mapping function
def preprocess_data(df):
    # Encoding categorical variables
    label_encoders = {}
    category_mappings = {}
    
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        
        # mapping of the original category to the encoded value
        category_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    
    return df, label_encoders, category_mappings


# specify the data path and implement the wrangle function to clean the data
data_path = "https://raw.githubusercontent.com/mlsanigeria/nigeria-crime-trends/main/data/Nigeria_1997-2024_Sep20.csv"
df = wrangle_data(data_path)

# preprocess data
df_processed, label_encoders, category_mappings = preprocess_data(df)

# copy the processed dataframe
df = df_processed.copy()

# Specify the model filename and path
model_filename = os.path.join('experimentation_yusufokunlola/pickled_model', 'finalized_model.sav')

# Load the pickled Gradient Boosting Regressor model
model = pickle.load(open(model_filename,'rb'))
    
# Sidebar for app information
st.sidebar.title('App Information')
st.sidebar.write("""
    This application predicts the number of fatalities based on the following features:
    - Time
    - Disorder Type
    - Event Type
    - Involved Parties
    - Location
    - Event Reporter
""")
st.sidebar.write("Please enter the features on the main page to get the number of fatalities recorded.")

st.text('')
st.text('')
st.sidebar.write("To learn more about the features, consult the [ACLED Codebook](https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2024/10/ACLED-Codebook-2024-7-Oct.-2024.pdf)")

st.text('')
st.text('')
st.sidebar.markdown('`Code:` [GitHub](https://github.com/mlsanigeria/nigeria-crime-trends/)')

# Time Precision mapping
time_mapping = {
    1: 'Exact Date',
    2: 'Estimated Week',
    3: 'Estimated Month'
}

# Geo-Precision mapping
geo_mapping = {
    1: 'Exact Location',
    2: 'Near the Town',
    3: 'Regional Area'
}

# Month mapping
month_mapping = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

#  Inter1 mapping
inter1_mapping = {
    1: 'State Forces',
    2: 'Rebel Groups',
    3: 'Political Militias',
    4: 'Identity Militias',
    5: 'Rioters',
    6: 'Protesters',
    7: 'Civilians',
    8: 'External/Other Forces'    
}

#  Inter2 mapping
inter2_mapping = {
    0: 'Nil',
    1: 'State Forces',
    2: 'Rebel Groups',
    3: 'Political Militias',
    4: 'Identity Militias',
    5: 'Rioters',
    6: 'Protesters',
    7: 'Civilians',
    8: 'External/Other Forces'    
}

# Create two columns for the input features
col1, col2 = st.columns(2)

# Input features in two columns
with col1:
    year = st.selectbox('Year', options=df['year'].unique().tolist())
    month = st.selectbox('Month', options=list(month_mapping.values()))
    time = st.selectbox('Recorded Date Accuracy', options=list(time_mapping.values()))
    disorder_type = st.selectbox('Disorder Type', options=list(category_mappings['disorder_type'].keys()))
    event_type = st.selectbox('Event Type', options=list(category_mappings['event_type'].keys()))
    sub_event_type = st.selectbox('Event Subcategory', options=list(category_mappings['sub_event_type'].keys()))
    actor1 = st.selectbox('Primary Involved Party', options=list(category_mappings['actor1'].keys()))
    inter1 = st.selectbox('Primary Group Affiliation', options=list(inter1_mapping.values()))
    actor2 = st.selectbox('Secondary Involved Party', options=list(category_mappings['actor2'].keys()))  
    
    
with col2:
    inter2 = st.selectbox('Secondary Group Affiliation', options=list(inter2_mapping.values()))
    civilian_targeting = st.selectbox('Civilian Targeting', options=list(category_mappings['civilian_targeting'].keys()))
    
    # Dynamic selection of admin1, admin2 and location
    admin1_options = list(category_mappings['admin1'].keys())
    selected_admin1 = st.selectbox("State", options=admin1_options)

    # Filter admin2 based on selected admin1 and map it with category mappings
    filtered_admin2_codes = df[df['admin1'] == category_mappings['admin1'][selected_admin1]]['admin2'].unique()
    filtered_admin2 = [key for key, value in category_mappings['admin2'].items() if value in filtered_admin2_codes]
    selected_admin2 = st.selectbox("Local Government Area", options=filtered_admin2)

    # Filter location based on selected admin2 and map it with category mappings
    filtered_location_codes = df[
        (df['admin1'] == category_mappings['admin1'][selected_admin1]) & 
        (df['admin2'] == category_mappings['admin2'][selected_admin2])]['location'].unique()
    filtered_location = [key for key, value in category_mappings['location'].items() if value in filtered_location_codes]
    selected_location = st.selectbox("Town", options=filtered_location)
    
    geo = st.selectbox('Location Precision', options=list(geo_mapping.values()))
    source = st.selectbox('Event Reporter', options=list(category_mappings['source'].keys()))
    source_scale = st.selectbox('Source Coverage', options=list(category_mappings['source_scale'].keys()))

# Convert mapped columns back to its corresponding numerical value
time_precision = [key for key, value in time_mapping.items() if value == time][0]
month_encoded = [key for key, value in month_mapping.items() if value == month][0]
inter1_encoded = [key for key, value in inter1_mapping.items() if value == inter1][0]
inter2_encoded = [key for key, value in inter2_mapping.items() if value == inter2][0]
geo_precision = [key for key, value in geo_mapping.items() if value == geo][0]

# Encoding categorical features
disorder_type_encoded = category_mappings['disorder_type'][disorder_type]
event_type_encoded = category_mappings['event_type'][event_type]
sub_event_type_encoded = category_mappings['sub_event_type'][sub_event_type]
actor1_encoded = category_mappings['actor1'][actor1]
actor2_encoded = category_mappings['actor2'][actor2]
civilian_targeting_encoded = category_mappings['civilian_targeting'][civilian_targeting]
admin1_encoded = category_mappings['admin1'][selected_admin1]
admin2_encoded = category_mappings['admin2'][selected_admin2]
location_encoded = category_mappings['location'][selected_location]
source_encoded = category_mappings['source'][source]
source_scale_encoded = category_mappings['source_scale'][source_scale]

# calculate the interaction and format as integer (e.g., if inter1=6 and inter2=0, interaction will be 60)
# this is hidden from the user interface 
interaction = int(f"{inter1_encoded}{inter2_encoded}")

# Create the input DataFrame for prediction in the specified order
input_data = pd.DataFrame({
    'year': [year],
    'month': [month_encoded],
    'time_precision': [time_precision],
    'disorder_type': [disorder_type_encoded],
    'event_type': [event_type_encoded],
    'sub_event_type': [sub_event_type_encoded],
    'actor1': [actor1_encoded],
    'inter1': [inter1_encoded], 
    'actor2': [actor2_encoded],
    'inter2': [inter2_encoded],
    'interaction': [interaction],
    'civilian_targeting': [civilian_targeting_encoded],
    'admin1': [admin1_encoded],
    'admin2': [admin2_encoded],
    'location': [location_encoded],
    'geo_precision': [geo_precision],
    'source': [source_encoded],
    'source_scale': [source_scale_encoded]
})


# Prediction button
if st.button('Predict Fatalities'):
    prediction = model.predict(input_data)
    st.markdown(f"<h2 style='text-align: left; color: orange;'><strong>Predicted Fatalities: {int(prediction[0])}</strong></h2>", unsafe_allow_html=True)
