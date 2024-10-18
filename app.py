import streamlit as st
import pandas as pd

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
        source = st.text_input('Source', 'Whatsapp')
    with col2:
        source_scale = st.selectbox('Source Scale', ['New media', 'National', 'National-Regional', 'Regional',
       'New media-National', 'Local partner-International',
       'Local partner-Other', 'Subnational-National',
       'National-International', 'Subnational', 'New media-Regional',
       'Other', 'International', 'Other-National', 'Subnational-Regional',
       'Other-Subnational', 'Other-Regional', 'Other-New media',
       'New media-International', 'Regional-International',
       'Subnational-International', 'Other-International',
       'New media-Subnational'])

    with col1:
        location = st.text_input('Location', 'Bolori')
    with col2:
        geo_precision = st.selectbox('Geo Precision', [1, 2, 3])

    with col1:
        actor1 = st.text_input('Actor 1', 'Protesters (Nigeria)')
    with col2:
        actor2 = st.text_input('Actor 2', '')

    with col1:
        interaction = st.selectbox('Interaction', range(0, 100))
    with col2:
        inter1 = st.selectbox('Inter1', range(0, 10))

    with col1:
        inter2 = st.selectbox('Inter2', range(0, 10))

    with col1:
        admin1 = st.text_input('Admin1', 'Borno')
    with col2:
        admin2 = st.text_input('Admin2', 'Bolori')

    with col1:
        event_type = st.selectbox('Event Type', ['Protests', 'Strategic developments', 'Battles', 'Riots',
       'Violence against civilians', 'Explosions/Remote violence'])
    with col2:
        sub_event_type = st.selectbox('Sub Event Type', ['Peaceful protest', 'Disrupted weapons use', 'Armed clash',
       'Mob violence', 'Abduction/forced disappearance', 'Attack',
       'Violent demonstration', 'Air/drone strike',
       'Looting/property destruction', 'Protest with intervention',
       'Agreement', 'Arrests', 'Change to group/activity', 'Other',
       'Remote explosive/landmine/IED',
       'Excessive force against protesters', 'Sexual violence',
       'Suicide bomb', 'Shelling/artillery/missile attack',
       'Non-state actor overtakes territory',
       'Government regains territory', 'Grenade',
       'Headquarters or base established',
       'Non-violent transfer of territory'])

    with col1:
        time_precision = st.selectbox('Time Precision', [1, 2, 3])
    with col2:
        civilian_targeting = st.selectbox('Civilian Targeting', [True, False])

    with col1:
        disorder_type = st.selectbox('Disorder Type', ['Demonstrations', 'Strategic developments', 'Political violence',
       'Political violence; Demonstrations'])
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
