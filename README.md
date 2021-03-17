# Investigation Into Trending Videos On YouTube
Authors: **Matthew Khoo**, **Chalsea Chen**, and **Chenyu Hu**

## Installing the _requests_ library
Our project involves querying the YouTube API and to do this we will be using the _requests_ library, which does not come installed in python. To do this, we need to use pip to install _requests_. Type the call _**$ python -m pip install requests**_ into the terminal to install _requests_. To convert the video duration into seconds, we also need to install and use the _isodate_ library, which can be installed in the same way.

## Running the code
To query the YouTube API require an _API key_, since this key is personalized to each user the key will not be provided in the code since it is not advisable to have your displayed on public websites like github where our code is available. Instead we will provide the key seperately in the submission. To run the code just replace _**your_api_key**_ with the _API key_ we provide. For example on line 20, videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key= _**your_api_key**_ ", params=parameters) and all other lines that have the requests.get call.

## Additional Information
Since the YouTube API is constantly being updated, when you run the code and generate the plots they might look different and/or have different results everytime we extract data from the api. We turned this temporary data into a csv for later use in our visualizations. The csv files we have cannot be reproduced due to the updated API, but running our get_data.py file should produce files in similar format. All visualizations should be reproduced by the plot_visualizations.py file using the existing csv files we have saved in the directory. The csvs in the plot_visualizations.py uses an absolute path '/home/csv_name.csv', so if paths are different please update the constants.