'''
Matthew Khoo, Chalsea Chen, Chenyu Hu
CSE 163 Proj
This python file contains all the methods to extract data we want from the
Youtube API to answer our research questions. It does all of the data
processing and transforms the final dataframes into csv files to be used
in the plot_visualizations.py file to create various plots.
'''
import requests
import pandas as pd
import isodate


# python 163.py
def build_df():
    '''
    This function requests data from the Youtube API and turns it into a
    data frame. It extracts 50 videos from each of the 17 countries considered
    to consume the most media. These videos should all be from the most
    popular chart. Returned dataset will consists of information about 850
    trending videos in total.
    '''
    # countries of interest
    countries = ['GB', 'US', 'FR', 'ID', 'KE', 'NG', 'DE', 'KR', 'AU', 'JP',
                 'ES', 'CZ', 'PH', 'CA', 'RU', 'MX', 'IT']
    # countries = ['GB']
    video_df = {'id': [], 'country': [], 'title': [], 'title_length': [],
                'category': [], 'tag_num': [], 'duration': [],
                'duration_secs': [], 'views': [], 'likes': [],
                'dislikes': [], 'comment_count': []}
    # get video Id from API, 50 most popular videos
    for country in countries:
        parameters = {
            'part': 'statistics,snippet,contentDetails',
            'chart': 'mostPopular',
            'maxResults': 50,  # ranges from 1-50
            'regionCode': country
        }
        videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key=your_api_key",
                              params=parameters)
        videos = videos.json()
        items = videos['items']
        # Print statement takes a look in items' format
        # countries = ['GB'] and 'maxResults': 1 shows you 1 item only
        # print(items)
        # add video information to dictionary
        for video in items:
            video_df['id'].append(video['id'])
            video_df['country'].append(country)
            video_df['title'].append(video['snippet']['title'])
            # count characters in title
            video_df['title_length'].append(len(video['snippet']['title']))
            video_df['category'].append(video['snippet']['categoryId'])
            # count number of tags
            # can test by looking at the numbers of a video['snippet']['tags']
            if 'tags' not in video['snippet']:
                video_df['tag_num'].append(0)
            else:
                video_df['tag_num'].append(len(video['snippet']['tags']))
            video_df['duration'].append(video['contentDetails']['duration'])
            # Test duration secs with the duration column
            video_df['duration_secs'].append(
                isodate.parse_duration(
                    video['contentDetails']['duration']).total_seconds())
            video_df['views'].append(int(video['statistics']['viewCount']))
            if 'likeCount' not in video['statistics']:
                video_df['likes'].append(0)
            else:
                video_df['likes'].append(int(video['statistics']['likeCount']))
            if 'dislikeCount' not in video['statistics']:
                video_df['dislikes'].append(0)
            else:
                video_df['dislikes'].append(int(
                    video['statistics']['dislikeCount']))
            if 'commentCount' not in video['statistics']:
                video_df['comment_count'].append(0)
            else:
                video_df['comment_count'].append(int(
                    video['statistics']['commentCount']))
    video_df = pd.DataFrame(video_df)
    return video_df


def build_categories_df():
    """
    Retrieves category information from the YouTube API and turns it into a
    data frame. Every region has the same category information so the region
    does not matter.
    """
    categories_df = {'id': [], 'category_name': []}
    parameters = {
        'part': 'snippet',
        'regionCode': 'US'
    }
    cat = requests.get('https://www.googleapis.com/youtube/v3/videoCategories?key=your_api_key',
                       params=parameters)
    cat = cat.json()
    items = cat['items']
    for category in items:
        categories_df['id'].append(category['id'])
        categories_df['category_name'].append(category['snippet']['title'])
    categories_df = pd.DataFrame(categories_df)
    return categories_df


def build_merge(category_df):
    '''
    Creates a data frame from information from the YouTube API, calculates
    the like dislike ratio to graph the like dislike ratio per country graph.
    '''
    countries = ['GB', 'US', 'FR', 'ID', 'KE', 'NG', 'DE', 'KR', 'AU', 'JP',
                 'ES', 'CZ', 'PH', 'CA', 'RU', 'MX', 'IT']
    video_df = {'country': [], 'category': [], 'likes/dislikes': []}
    for country in countries:
        parameters = {
            'part': 'statistics,snippet',
            'chart': 'mostPopular',
            'maxResults': 50,  # ranges from 1-50
            'regionCode': country
        }
        videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key=your_api_key",
                              params=parameters)
        videos = videos.json()
        items = videos['items']
        # add video information to dictionary
        for video in items:
            video_df['country'].append(country)
            video_df['category'].append(video['snippet']['categoryId'])
            if 'likeCount' not in video['statistics']:
                video_df['likes/dislikes'].append(0)
            elif 'dislikeCount' not in video['statistics']:
                video_df['likes/dislikes'].append(0)
            else:
                likes = int(video['statistics']['likeCount'])
                dislikes = int(video['statistics']['dislikeCount'])
                ratio = round(likes / dislikes, 2)
                video_df['likes/dislikes'].append(ratio)
    video_df = pd.DataFrame(video_df)
    max_ratio = video_df.groupby('country')['likes/dislikes'].max()
    merged = max_ratio.to_frame().merge(
        video_df, on=['country', 'likes/dislikes'], how='left')
    merge_category = merged.merge(
        category_df, left_on='category', right_on='id', how='left')
    return merge_category


def main():
    '''
    Runs the method
    '''
    video_df = build_df()
    video_df.to_csv('videos.csv')
    categories_df = build_categories_df()
    categories_df.to_csv('categories.csv')
    merge_df = build_merge(categories_df)
    merge_df.to_csv('merge_category.csv')


if __name__ == '__main__':
    main()