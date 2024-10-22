import streamlit as st
import pandas as pd

df = pd.read_csv("data\\Nigeria_1997-2024_Sep20.csv")

#To dynamically store the unique sources
ls = df["source"].unique()
unique_sources = set()
for val in ls:
  if(val.find(';')==-1):
    unique_sources.add(val)
  else:
      temp = val.split(';')
      for i in range(len(temp)):
        unique_sources.add(temp[i].strip())

#Loading the data dynamically
list_of_locations = df["location"].unique()
list_of_source_scale = df["source_scale"].unique()
list_of_event_type = df["event_type"].unique()
list_of_sub_event_type = df["sub_event_type"].unique()
list_of_disorder_type = df["disorder_type"].unique()
list_of_admin_1 = df["admin1"].unique()
list_of_admin_2 = df["admin2"].unique()
list_of_actor1 = df["actor1"].unique()
list_of_actor2 = df["actor2"].dropna().unique()


#edit this for actual predictions
def predict_fatalities(input_features):
    #placeholder
    pass

st.title('Nigeria Crime Fatalities Prediction')
st.write('This app predicts the number of crime fatalities in Nigeria based on specific input features from the user.')

with st.form("user_inputs"):
    st.header("Input Event Details")

    col1, col2 = st.columns(2)

    with col1:
        year = st.selectbox('Year', range(1997, 2025))
    with col2:
        month = st.selectbox('Month', range(1, 13))

    with col1:
        source = st.multiselect('Source', unique_sources)
    with col2:
        source_scale = st.selectbox('Source Scale', list_of_source_scale)

    with col1:
        location = st.selectbox('Location', list_of_locations)
    with col2:
        geo_precision = st.selectbox('Geo Precision', [1, 2, 3])

    with col1:
        actor1 = st.selectbox('Actor 1', list_of_actor1)
    with col2:
        actor2 = st.selectbox('Actor 2', list_of_actor2, index=None)

    with col1:
        interaction = st.selectbox('Interaction', range(0, 100))
    with col2:
        inter1 = st.selectbox('Inter1', range(0, 10))

    with col1:
        inter2 = st.selectbox('Inter2', range(0, 10))

    with col1:
        admin1 = st.selectbox('Admin1', list_of_admin_1)
    with col2:
        admin2 = st.selectbox('Admin2',list_of_admin_2)

    with col1:
        event_type = st.selectbox('Event Type', list_of_event_type)
    with col2:
        sub_event_type = st.selectbox('Sub Event Type', list_of_sub_event_type)

    with col1:
        time_precision = st.selectbox('Time Precision', [1, 2, 3])
    with col2:
        civilian_targeting = st.selectbox('Civilian Targeting', [True, False])

    with col1:
        disorder_type = st.selectbox('Disorder Type', list_of_disorder_type)
    with col2:
        notes = st.text_area('Notes', 'Provide any specific notes here.')

    submit_button = st.form_submit_button("Predict Fatalities")

if submit_button:
    input_features = {
        'year': year,
        'source': source,
        'source_scale': source_scale,
        'location': location,
        'interaction': interaction,
        'actor1': actor1,
        'month': month,
        'admin2': admin2,
        'admin1': admin1,
        'event_type': event_type,
        'time_precision': time_precision,
        'sub_event_type': sub_event_type,
        'actor2': actor2,
        'inter1': inter1,
        'inter2': inter2,
        'geo_precision': geo_precision,
        'civilian_targeting': civilian_targeting,
        'disorder_type': disorder_type,
        'notes': notes
    }

    predicted_fatalities = predict_fatalities(input_features)

    st.subheader('Prediction Result')
    st.write(f'Predicted Fatalities: {predicted_fatalities}')

    st.subheader('Input Features')
    st.write(pd.DataFrame([input_features]))
