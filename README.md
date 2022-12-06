<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/HalleypC">
    <img src="https://cdn-icons-png.flaticon.com/512/3043/3043608.png" alt="Logo" width="80" height="80"/> 
  </a>
<h3 align="center">Wildfire Predictor & Analysis</h3>
  <p align="center">
    A Data Science and Machine Learning Project
    <br />
    <a href="https://github.com/HalleypC/Wildfire-Predictor/blob/main/src/scripts/app.py">View Streamlit app code</a>
    ·
    <a href="https://github.com/HalleypC/Wildfire-Predictor/blob/main/src/notebooks/6\)%20Model_2.ipynb"> Model Building</a>
    ·
    <a href="https://github.com/HalleypC/Wildfire-Predictor/blob/main/src/notebooks/1\)%20EDA.ipynb">EDA on dataset</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## The Motivation
* Naturally occuring wildfires are an essential part of our ecosystem to maintain balance. The natural process clears out old, overgrown forests and resets the local ecosystem. Unfortunately, with increased populations and uneducation about safe practices in high risk zones, coupled with climate change, the last decade has seen an increase in the number, ferocity, and size of human caused wildfires. 
* To more effectively develop insights, tools, and make data driven decisions on targeting resources to the prevention and mitigation of wildfire, the cause of the fire is essential. 
* Without knowing the cause of the fire, it becomes difficult to track and develop strategies to prevent them. 

## About The Project
* Using machine learning, I have built a model that takes wildfire and environement features and predicts it's cause.
* I built a prediction app hosted on **StreamLit**,
* primarily used **Sklearn** for pre-processing and model building,
* and SQLite, Pandas, Numpy, Matplotlib and Seaborn for csv reading, data processing, data cleaning, and visualization.

<!-- GETTING STARTED -->
## Getting Started
* I used the United States Forest Service dataset with forest fires from 1992 to 2015. I extracted data from the west coast states as my base data. The dataset contains fire characteristics such as iginition date, containment date, location, size, cause, and more. 
* I supplemented this data with the Open Weather API to gather elevation, temperature, precipitaion, moisture, and more. 

<!-- USAGE EXAMPLES -->
## Steps
* Aquiring dataset from [US Department of Agriculture](https://www.fs.usda.gov/rds/archive/catalog/RDS-2013-0009.4).
* Exploratory Data Analysis (EDA), investigating the data
* Data Cleaning
* Baseline model
* Feature Engineering - adding the weather data and engineering additional features
* Improving the Model
* Building Streamlit App.

### Investigating the Data
* Used SQLite to connect to the dataset and extract a dataframe of the western states. Saved the dataframe as a CSV file
* EDA to gain insight of the data using Pandas and data visualization using Matplotlib & Seaborn
* Developed frequency plots to better understand the distribution of the data and to see how much data would need cleaning
* Developed geo maps, time series, and more plots to understand the data.

<p align="right">(<a href="#top">back to top</a>)</p> 

### Open Weather API
* I chose to supplement the US wildfire data with historic weather data.
* I was limited to 10,000 calls a day so I grouped my 80,000+ dataset by county. This reduced my datapoints by over a third. I ran the API calls in 10,000 sections until it was complete. 
* I used the [Open Weather historical weather](https://open-meteo.com/en/docs/historical-weather-api) API.
* The features I was able to consistently extract for my dataset were:
    * Elevation (m)
    * Maximum Temperature (2 m)
    * Minimum Temperature (2 m)
    * Precipitation Sum
    * Rain Sum
    * Snowfall Sum
    * Temperature (2 m)
    * Wind Gusts (10 m)
    * Soil Temperature (0-7 cm)
    * Soil Temperature (7-28 cm)
    * Soil Moisture (0-7 cm)
    * Soil Moisture (7-28 cm)
* The elevation, soil temperatures, and max temperatures proved to be the most effective in improving the model. 

### Model Building 
* The model is a multiclass classification algorithm to predict the fire `Cause` from the dataset. Initially I was aiming to classify 12 categories, but after further reflection I consolidated these 12 categories into three: `Natural, Accident, Malicious`.
* I chose to consolidate the features because the goal of the project was to label the cause for prevention and mitigation analysis. The strategies for preventing human accidents - regardless of accident - is similar. Whereas the strategies for natural vs. human are quite different. After this reflection I decided the consolidation of causes would allow my model to produce a higher accuracy while still meeting the goals of the project.
* Models used : **Random Forest, SVM Classifier, XGboost**.
* After three iterations, the Random Forest Model proved to be the most reliable and is the one used in the app.

![results](./output/figures/Result_F1.png)

### Streamlit
* I wanted to build a proof of concept that this model could be used by organizations to help them label their wildfire causes. 
* I imported the Streamlit module and created a page that allow for user input and returns a prediction.
* Although my model takes 19 features as input, only 6 are required from the user in the app. The rest of the features are extracted behind the scenes for a more simple user experience. 
* The app calls the Open Weather API to extract the relevent weather features and calculates the remaining engineered features before returning the prediction. 
* Using the Pickle library I saved my model to be easily used within my app. Unfortunately the pickle model was too large for deploment so I used the bz2file library to compresses the file and successfully deploy the model using the Streamlit Cloud Service.
* [Check out my app!](https://halleypc-wildfire-predictor-srcscriptsapp-93qsj3.streamlit.app/)

### Results
* With the cause of fires predicted we can run analytics to identify clustered locations, proximity to points of interest, or a number of other features that could help organizations make decisions. 
* For example in the figure below we can see that the size vs. day of year cluster very differently for the three causes. Natural fires cluster more narrowly whereas human caused fires (Accidental and Malicious) cluster more loosely. This figure shows the time of year in which resources are needed for the different causes. 
* From the figure we can also see that natual fires occur more frequently at higher elevations, denoted by the darker hue. 
![results_map](./output/figures/Result_SizevsDOY2.png)

Feel free to reach out to me on linkedin for more results and discussion on results!

### **Technologies used**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-%23F7931E.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23000.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Pickle](https://img.shields.io/badge/Pickle-%FF2a2a.svg?style=for-the-badge&logoColor=white)
![Streamlit](https://img.shields.io/badge/Seaborn-%23000.svg?style=for-the-badge&logo=seaborn&logoColor=white)


### **Tools used**
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![JupyterLabs](https://img.shields.io/badge/Jupyter--Labs-%23121011.svg?style=for-the-badge&logo=jupyter&logoColor=white)