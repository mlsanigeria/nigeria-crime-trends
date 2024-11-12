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
data_path = "../data/Nigeria_1997-2024_Sep20.csv"
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
    - Year
    - Month
    - Time Precision
    - Disorder Type
    - Event Type
    - Sub Event Type
    - Actor 1 and Actor 2
    - Inter 1 and Inter 2 
    - Interaction
    - Civilian Targeting
    - Admin 1 and Admin 2
    - Location
    - Geo Precision
    - Source and Source Scale
""")
st.sidebar.write("Please enter the features on the main page to get the number of fatalities recorded.")

st.text('')
st.text('')
st.sidebar.write("To learn more about the features, consult the [ACLED Codebook](https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2024/10/ACLED-Codebook-2024-7-Oct.-2024.pdf)")

st.text('')
st.text('')
st.sidebar.markdown('`Code:` [GitHub](https://github.com/mlsanigeria/nigeria-crime-trends/)')


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

# Unique values for various features
years = df['year'].unique().tolist()
interactions = df['interaction'].unique().tolist()
time_precisions = df['time_precision'].unique().tolist()
inter1s = df['inter1'].unique().tolist()
inter2s = df['inter2'].unique().tolist()
geo_precisions = df['geo_precision'].unique().tolist()


# Create two columns for the input features
col1, col2 = st.columns(2)

# Input features in two columns
with col1:
    year = st.selectbox('Year', options=years)
    month = st.selectbox('Month', options=list(month_mapping.values()))
    time_precision = st.selectbox('Time Precision', options=time_precisions)
    disorder_type = st.selectbox('Disorder Type', options=list(category_mappings['disorder_type'].keys()))
    event_type = st.selectbox('Event Type', options=list(category_mappings['event_type'].keys()))
    sub_event_type = st.selectbox('Sub Event Type', options=list(category_mappings['sub_event_type'].keys()))
    actor1 = st.selectbox('Actor 1', options=list(category_mappings['actor1'].keys()))
    inter1 = st.selectbox('Inter 1', options=inter1s)
    actor2 = st.selectbox('Actor 2', options=list(category_mappings['actor2'].keys()))  
    
    
with col2:
    inter2 = st.selectbox('Inter 2', options=inter2s) 
    interaction = st.selectbox('Interaction', options=interactions)
    civilian_targeting = st.selectbox('Civilian Targeting', options=list(category_mappings['civilian_targeting'].keys()))
    admin1 = st.selectbox('Admin 1', options=list(category_mappings['admin1'].keys()))    
    admin2 = st.selectbox('Admin 2', options=list(category_mappings['admin2'].keys()))
    location = st.selectbox('Location', options=list(category_mappings['location'].keys()))
    geo_precision = st.selectbox('Geo Precision', options=geo_precisions)
    source = st.selectbox('Source', options=list(category_mappings['source'].keys()))
    source_scale = st.selectbox('Source Scale', options=list(category_mappings['source_scale'].keys()))


# Convert selected month back to its corresponding numerical value
month_encoded = [key for key, value in month_mapping.items() if value == month][0]

# Encoding categorical features
disorder_type_encoded = category_mappings['disorder_type'][disorder_type]
event_type_encoded = category_mappings['event_type'][event_type]
sub_event_type_encoded = category_mappings['sub_event_type'][sub_event_type]
actor1_encoded = category_mappings['actor1'][actor1]
actor2_encoded = category_mappings['actor2'][actor2]
civilian_targeting_encoded = category_mappings['civilian_targeting'][civilian_targeting]
admin1_encoded = category_mappings['admin1'][admin1]
admin2_encoded = category_mappings['admin2'][admin2]
location_encoded = category_mappings['location'][location]
source_encoded = category_mappings['source'][source]
source_scale_encoded = category_mappings['source_scale'][source_scale]


# Create the input DataFrame for prediction in the specified order
input_data = pd.DataFrame({
    'year': [year],
    'month': [month_encoded],
    'time_precision': [time_precision],
    'disorder_type': [disorder_type_encoded],
    'event_type': [event_type_encoded],
    'sub_event_type': [sub_event_type_encoded],
    'actor1': [actor1_encoded],
    'inter1': [inter1], 
    'actor2': [actor2_encoded],
    'inter2': [inter2],
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
