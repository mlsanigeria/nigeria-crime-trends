# Nigeria Crime Trends Prediction App

The application provides predictions on the number of fatalities in Nigeria based on various features derived from historical data on crime and violent events. The app utilizes a machine learning model to analyze input features and predict the number of fatalities recorded for specific event types.

## Selected Features
The application uses the following features for predictions:
- **Year**: The year in which the event took place.
- **Month**: The month in which the event took place.
- **Time Precision**: A numeric code between 1 and 3 indicating the level of precision of the date recorded for the event. The higher the number, the lower the precision.
- **Disorder Type**: The disorder category an event belongs to (e.g., Political violence, Demonstrations, etc).
- **Event Type**: The type of event; further specifies the nature of the event.
- **Sub Event Type**: A subcategory of the event type (e.g., Armed clash).
- **Actor 1**: One of two main actors involved in the event (does not necessarily indicate the aggressor).
- **Inter1**: A text value indicating the type of 'Actor 1'.
- **Actor 2**: One of two main actors involved in the event (does not necessarily indicate the target or victim).
- **Inter2**: A text value indicating the type of 'Actor 2'.
- **Interaction**: A text value based on a combination of 'Inter 1' and 'Inter 2' indicating the two actor types interacting in the event.
- **Civilian Targeting**: This column indicates whether the event involved civilian targeting. 
- **Admin 1**: The largest sub-national administrative region in which the event took place.
- **Admin 2**: The second largest sub-national administrative region in which the event took place.
- **Location**: The name of the location at which the event took place.
- **Geo Precision**: A numeric code between 1 and 3 indicating the level of certainty of the location recorded for the event. The higher the number, the lower the precision.
- **Source**: The source of information for the event.
- **Source Scale**: An indication of the geographic closeness of the used sources to the event.


For more information about the features, please consult the [ACLED Codebook](https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2024/10/ACLED-Codebook-2024-7-Oct.-2024.pdf).


## Application Overview

### Data Preprocessing
The application uses the following steps to clean and preprocess the data:
1. **Data Wrangling**: 
    - Load the dataset and convert `event_date` to a proper datetime format.
    - Extract `month` and `day` from the `event_date` column for further use.
    - Replace missing or infrequent values with appropriate substitutes (e.g., replace missing values in `actor2` with 'Not available').
    - Drop any rows that contain significant missing values, such as administrative locations (`admin1` and `admin2`).
    - Consolidate values in certain features (e.g., replacing values in `source`, `actor1`, and `actor2` with 'Other' if they occur less than 100 times).
    - Remove duplicates.

2. **Label Encoding**:
    - Categorical variables are label-encoded to convert them into numeric values required for the model. Mappings for each categorical feature are saved to allow decoding back to their original values for use on the application interface.

## Machine Learning Model Selection

Seven machine learning models were evaluated on the cleaned dataset using a 70:30 train-test split to determine the most effective model for predicting fatalities, utilizing default parameters. The models include:

- **Linear Regression**
- **Lasso Regression**
- **Ridge Regression**
- **Random Forest Regressor**
- **Decision Tree Regressor**
- **Gradient Boosting Regressor**
- **XGBoost Regressor**

The models were evaluated based on the following performance metrics:
- **Mean Absolute Error (MAE)**
- **Root Mean Squared Error (RMSE)**
- **Mean Squared Error (MSE)**
- **R² Score (R2)**

Among these, the **Gradient Boosting Regressor** was selected because it had the best overall performance across all the metrics. For detailed results and performance comparisons, please refer to the notebook included in the repository.

### App Features
- **User Input**: The sidebar provides detailed information about the features used in the app, and users can select various options from dropdown menus on the main page.
- **Prediction**: The application generates predictions for the number of fatalities after the user selects the relevant input features.

### Data
The data used for this application is sourced from historical records of violent events in Nigeria from 1997 to 2024 by ACLED.

## Installation

To run this application locally, follow the steps below:

1. Clone the repository:
    ```bash
    git clone https://github.com/yusufokunlola/nigeria-crime-trends.git
    ```
- Navigate to the `cd experimentation_yusufokunlola` folder
  
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Launch the app:
    ```bash
    streamlit run app.py
    ```

## Usage
Once the app is launched, follow these steps:

1. Select the features you want to use for the prediction from the dropdown menus on the main page.
2. Click the "Predict Fatalities" button to get the prediction.
3. The app will display the predicted number of fatalities based on the selected inputs.