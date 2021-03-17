'''
Matthew Khoo, Chalsea Chen, Chenyu Hu
CSE 163 Proj
This python file contains all the methods to create visualizations
corresponding to the research questions we have. It uses the csv files
produced from the get_data.py file.
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


VIDEOS = '/home/videos.csv'
CATEGORIES = '/home/categories.csv'
MERGE_CATEGORY = '/home/merge_category.csv'


def world_like_dislike_raio(videos_df, categories_df):
    '''
    This function takes in the trending videos data set and
    the categories data set. It plots the total likes divides
    by the total dislikes per category in a bar chart.
    '''
    likes_df = videos_df.groupby('category')['likes'].sum()
    dislikes_df = videos_df.groupby('category')['dislikes'].sum()
    merged = likes_df.to_frame().merge(
        dislikes_df.to_frame(), on='category', how='left')
    merged['ratio'] = round(merged['likes'] / merged['dislikes'], 2)
    add_category_name = merged.merge(
        categories_df, left_on='category', right_on='id', how='left')
    sns.catplot(x='category_name', y='ratio', kind='bar',
                data=add_category_name, height=5, aspect=1.5)
    plt.xticks(rotation=-45)
    plt.title('Category by Like:Dislike Ratio')
    plt.xlabel('Category')
    plt.ylabel('Ratio of Like:Dislike')
    plt.savefig('world_like_dislike_ratio.png', bbox_inches='tight')


def world_views_plot(videos_df, categories_df):
    '''
    This function takes in the trending videos data set and
    the categories data set. It plots the total views per category
    in a bar chart.
    '''
    views_df = videos_df.groupby('category')['views'].sum()
    merged = views_df.to_frame().merge(categories_df, left_on='category',
                                       right_on='id', how='left')
    sns.catplot(x='category_name', y='views', kind='bar', data=merged,
                height=5, aspect=2)
    plt.xticks(rotation=-45)
    plt.title('Category by Total Views')
    plt.xlabel('Category')
    plt.ylabel('Views')
    plt.savefig('world_views.png', bbox_inches='tight')


def plot_likes_dislikes_ratio(merge_category):
    '''
    This plot takes in a data frame on trending videos
    and plots the categories with highest total likes
    divides by total dislikes per country.
    '''
    sns.catplot(x='country', y='likes/dislikes', hue='category_name',
                kind='bar', data=merge_category)
    plt.xticks(rotation=-45)
    plt.title('Category with Highest Like to Dislike Ratio in each Country')
    plt.xlabel('Country')
    plt.ylabel('Ratio of Like:Dislike')
    plt.savefig('likes_dislikes_ratio.png', bbox_inches='tight')


def plot_title_length(videos):
    '''
    This function takes in the trending videos dataset and plots a histogram
    of the number of videos distributed based on title length.
    '''
    fig, ax = plt.subplots(1, figsize=(15, 10))
    sns.histplot(ax=ax, x=videos['title_length'], bins=30)
    ax.set_xlabel('Title Length (Characters)')
    ax.set_ylabel('Count (Number of Videos)')
    ax.set_title('Title Length Distribution for Trending Videos')
    plt.savefig('title_plot.png', bbox_inches='tight')


def plot_duration(videos):
    '''
    This function takes in the trending videos dataset and plots 2 histograms,
    one with all the number of videos distributed based on duration in hour and
    another based on the duration in minutes for videos less than 1 hour.
    '''
    fig, [ax1, ax2] = plt.subplots(ncols=2, figsize=(25, 10))
    duration_minutes = videos['duration_secs'] / 60
    duration_hours = duration_minutes / 60
    sns.histplot(ax=ax1, x=duration_hours)
    duration_1_hr = duration_minutes[duration_minutes < 60]
    sns.histplot(ax=ax2, x=duration_1_hr)
    ax1.set_xlabel('Duration (Hours)')
    ax1.set_ylabel('Count (Number of Videos)')
    ax2.set_xlabel('Duration (Minutes)')
    ax2.set_ylabel('Count (Number of Videos)')
    ax1.set_title('Duration Distribution for Trending Videos')
    ax2.set_title(
        'Duration Distribution for Trending Videos (Less than 1 Hour)')
    plt.savefig('duration_plot.png', bbox_inches='tight')
    # Checking the outlier
    # print(videos['duration_secs'].max())
    # print(videos[videos['duration_secs'] == videos['duration_secs'].max()])


def plot_tag_num(videos):
    '''
    This function takes in the trending videos dataset and plots a histogram
    of the number of videos distributed based on the number of tags associated.
    '''
    fig, ax = plt.subplots(1, figsize=(15, 10))
    sns.histplot(ax=ax, x=videos['tag_num'], bins=30)
    ax.set_xlabel('Number of Tags)')
    ax.set_ylabel('Count (Number of Videos)')
    ax.set_title('Number of Tags for Trending Videos')
    plt.savefig('tag_num_plot.png', bbox_inches='tight')
    # Check outlier
    # print(videos['tag_num'].max())
    # print(videos[videos['tag_num'] == videos['tag_num'].max()])


def individual_statistics(videos):
    '''
    This function takes in the trending videos dataset and plots 2 boxplots for
    each of the statistics: views, likes, dislikes, and comment counts. One
    boxplot shows outliers, other one doesn't.
    '''
    fig, [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8] = plt.subplots(
        nrows=1, ncols=8, figsize=(45, 20))
    stats = videos[['views', 'likes', 'dislikes', 'comment_count']]
    sns.boxplot(ax=ax1, data=stats['views'])
    sns.boxplot(ax=ax2, data=stats['views'], showfliers=False)
    sns.boxplot(ax=ax3, data=stats['likes'], color='orange')
    sns.boxplot(ax=ax4, data=stats['likes'], showfliers=False, color='orange')
    sns.boxplot(ax=ax5, data=stats['dislikes'], color='green')
    sns.boxplot(ax=ax6, data=stats['dislikes'], showfliers=False,
                color='green')
    sns.boxplot(ax=ax7, data=stats['comment_count'], color='red')
    sns.boxplot(ax=ax8, data=stats['comment_count'], showfliers=False,
                color='red')
    ax1.set_title('Views for Trending Videos (With Outliers)')
    ax2.set_title('Views for Trending Videos')
    ax3.set_title('Likes for Trending Videos (With Outliers)')
    ax4.set_title('Likes for Trending Videos')
    ax5.set_title('Dislikes for Trending Videos (With Outliers)')
    ax6.set_title('Dislikes for Trending Videos')
    ax7.set_title('Comment Counts for Trending Videos (With Outliers)')
    ax8.set_title('Comment Counts for Trending Videos')
    plt.savefig('individual_statistics.png', bbox_inches='tight')
    # Test plots with quantile
    # print(stats.quantile([.01,.25,.5,.75,.99]))
    # Check maximums
    # print(videos[videos['views']==videos['views'].max()])
    # print(videos[videos['likes']==videos['likes'].max()])
    # print(videos[videos['dislikes']==videos['dislikes'].max()])
    # print(videos[videos['comment_count']==videos['comment_count'].max()])


def plot_correlations(videos):
    '''
    This function takes in the trending videos dataset and plots a heatmap
    for the correlations of the numerical values in the dataset.
    '''
    corr = videos.drop(videos.columns[[0, 5]], axis=1).corr()
    fig, ax = plt.subplots(1, figsize=(10, 5))
    sns.heatmap(corr, ax=ax, annot=True)
    ax.set_title('Correlatons')
    plt.savefig('correlation_plot.png', bbox_inches='tight')


def views_ml(videos):
    '''
    This function takes in the trending videos dataset and creates a machine
    learning model taking category, country, tag number, title length, and
    duration seconds as features and predicts the view.
    '''
    quantile25 = videos['views'].quantile(.25)
    quantile75 = videos['views'].quantile(.75)
    # Filter out outliers
    videos = videos[(videos['views'] > quantile25) &
                    (videos['views'] < quantile75)]
    print(videos)
    country = pd.get_dummies(videos['country'])
    categories = pd.get_dummies(videos['category'])
    features = videos[['title_length', 'tag_num', 'duration_secs']].join(
        [country, categories])
    # print(features)
    labels = videos['views']
    # print(labels)
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)
    model = DecisionTreeRegressor(max_depth=0.5)
    model.fit(features_train, labels_train)
    # Compute train mean squared error
    train_predictions = model.predict(features_train)
    print('Train Error:', mean_squared_error(labels_train, train_predictions))
    # Compute train mean squared error
    test_predictions = model.predict(features_test)
    print('Test Error:', mean_squared_error(labels_test, test_predictions))


def plot_title_length_country(videos):
    '''
    This function takes in the trending videos dataset and plots a bar chart
    of the average title lengths of each country.
    '''
    sns.catplot(x='country', y='title_length', kind='bar', data=videos)
    plt.xlabel('Countries')
    plt.ylabel('Title Length (Characters)')
    plt.title('Average Title Lengths for Different Countries')
    plt.savefig('title_country_plot.png', bbox_inches='tight')


def plot_views_country(videos):
    '''
    This function takes in the trending videos dataset and plots a bar chart
    of the average number of views of each countriey.
    '''
    sns.catplot(x='country', y='views', kind='bar', data=videos)
    plt.xlabel('Countries')
    plt.ylabel('Views')
    plt.title('Average Views for Different Countries')
    plt.savefig('view_coutry_plot.png', bbox_inches='tight')


def plot_duration_country(videos):
    '''
    This function takes in the trending videos dataset and plots a bar chart
    of the average duration seconds of each country.
    '''
    sns.catplot(x='country', y='duration_secs', kind='bar', data=videos)
    plt.xlabel('Countries')
    plt.ylabel('Duration (Seconds)')
    plt.title('Average Video Duration for Different Countries')
    plt.savefig('duration_coutry_plot.png', bbox_inches='tight')


def main():
    '''
    Creates the various visualizations and runs the machine learning model.
    '''
    # python proj.py
    videos = pd.read_csv(VIDEOS)
    categories = pd.read_csv(CATEGORIES)
    merge = pd.read_csv(MERGE_CATEGORY)
    plot_likes_dislikes_ratio(merge)
    world_views_plot(videos, categories)
    world_like_dislike_raio(videos, categories)
    individual_statistics(videos)
    plot_title_length(videos)
    plot_duration(videos)
    plot_tag_num(videos)
    plot_correlations(videos)
    views_ml(videos)
    plot_title_length_country(videos)
    plot_views_country(videos)
    plot_duration_country(videos)


if __name__ == '__main__':
    main()