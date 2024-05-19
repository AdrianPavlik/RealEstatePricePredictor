import datetime
import json
import random
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import learning_curve


def impute_price(df):
    median_price = df['price'].median()
    high_price = median_price * 1.25
    low_price = median_price * 0.75

    # Define conditions
    conditions = [
        (df['land_area'] < 60) & (df['number_of_rooms'] <= 3),
        (df['land_area'] >= 60) & (df['land_area'] <= 140) & (df['number_of_rooms'] > 2) & (
                    df['number_of_rooms'] <= 4),
        (df['land_area'] > 140) & (df['number_of_rooms'] > 4)
    ]
    choices = [
        low_price,
        median_price,
        high_price
    ]
    price_values = np.select(conditions, choices, default=median_price)
    df.loc[df['price'].isna(), 'price'] = price_values[df['price'].isna()]
    return df


def clean_columns(df, float_columns, int_columns, object_columns, float_impute='mean', int_impute=0):
    """
    Cleans and converts specified columns to either float, int, or maintains object type, with options for imputation.

    Args:
    - df (pd.DataFrame): The DataFrame containing the columns to clean.
    - float_columns (list of str): The columns to convert to float.
    - int_columns (list of str): The columns to convert to int.
    - object_columns (list of str): The columns to manage as objects (strings).
    - float_impute (str or float): The imputation method for float columns ('mean', 'median', 'mode') or a specific value.
    - int_impute (int or float): The imputation value for integer columns or a specific value.

    Returns:
    - pd.DataFrame: The DataFrame with cleaned and converted columns.
    """

    for col in float_columns:
        df[col] = df[col].replace('', pd.NA)
        df[col] = df[col].astype(str).apply(lambda x: x.replace('.', '').replace(',', '.') if (
                    ',' in x and x.count(',') == 1 and len(x.split(',')[-1]) <= 2) else x.replace(',', ''))
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if col == 'price':
            continue
        if isinstance(float_impute, str):
            if float_impute == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif float_impute == 'median':
                df[col] = df[col].fillna(df[col].median())
            elif float_impute == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(float_impute)

    for col in int_columns:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        df[col] = df[col].replace('', pd.NA)
        most_frequent = df[col].mode().iloc[0] if not df[col].mode().empty else int_impute
        df[col] = df[col].astype(str).apply(lambda x: x.replace('.', '').replace(',', '.') if (',' in x and x.count(',') == 1 and len(x.split(',')[-1]) <= 2) else x.replace(',', ''))
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(most_frequent).astype(int)
        if col == 'year_of_construction' and 'new_building' in df.columns:
            current_year = datetime.datetime.now().year
            condition = (df['new_building'] == 1) & df[col].isna()
            df.loc[condition, col] = df.loc[condition, col].apply(
                lambda x: random.randint(current_year - 5, current_year)
            )

    for col in object_columns:
        df[col] = df[col].replace('', pd.NA)
        most_frequent = df[col].mode().iloc[0] if not df[col].mode().empty else 'missing'
        df[col] = df[col].fillna(most_frequent)

    #df = impute_price(df)
    return df


def remove_outliers(df, int_columns=None, float_columns=None):
    """
    Remove outliers from a DataFrame based on 3 standard deviations from the mean.

    Parameters:
    df (DataFrame): The input DataFrame from which to remove outliers.
    int_columns (list): List of column names with integer data to check for outliers.
    float_columns (list): List of column names with float data to check for outliers.

    Returns:
    DataFrame: A new DataFrame with outliers removed.
    """

    df_out = df.copy()
    numeric_columns = []

    if int_columns is not None:
        numeric_columns += [col for col in int_columns if col in df_out.columns]

    if float_columns is not None:
        numeric_columns += [col for col in float_columns if col in df_out.columns]

    for column in numeric_columns:
        if df_out[column].dtype == 'int64' or df_out[column].dtype == 'float64':
            mean = df_out[column].mean()
            std = df_out[column].std()
            upper_limit = mean + 3 * std
            lower_limit = mean - 3 * std
            df_out = df_out[(df_out[column] >= lower_limit) & (df_out[column] <= upper_limit)]

    return df_out


def plot_grid_search_validation_curve(file_name, grid, param_to_plot, title='Validation Curve', xlabel='Parameter', ylabel='Score'):
    param_name = 'param_' + param_to_plot
    test_scores = grid.cv_results_['mean_test_score']
    param_values = list(grid.cv_results_[param_name])

    plt.figure(figsize=(8, 5))
    plt.plot(param_values, test_scores, label="Test score")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_name}.png", bbox_inches='tight')


def plot_learning_curve(file_name, train_sizes, train_scores, test_scores, title):
    train_scores_mean = -np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.title(title)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.legend(loc="best")
    plt.grid(True)
    plt.savefig(f"{file_name}.png", bbox_inches='tight')


def load_json(file_path):
    with open(file_path, 'r', encoding='utf8') as json_file:
        return json.load(json_file)


def get_cities():
    # Load all necessary data
    regions_data = load_json('regions.json')
    districts_data = load_json('districts.json')
    cities_data = load_json('cities.json')

    # Prepare the mapping structures
    region_districts_cities_mapping = {}

    # First, map districts to their regions
    for district in districts_data:
        region_id = district['region_id']
        region_name = next((region['name'] for region in regions_data if region['id'] == region_id), 'Unknown Region')
        if region_name not in region_districts_cities_mapping:
            region_districts_cities_mapping[region_name] = {}

        region_districts_cities_mapping[region_name][district['name']] = []

    # Now map cities to the appropriate district in the appropriate region
    for city_name, city_details in cities_data.items():
        district_name = city_details['district']
        # Iterate through all regions and their districts to find the right one
        for region in region_districts_cities_mapping:
            if district_name in region_districts_cities_mapping[region]:
                region_districts_cities_mapping[region][district_name].append(city_name)

    # Optionally sort cities under each district
    for region in region_districts_cities_mapping:
        for district in region_districts_cities_mapping[region]:
            region_districts_cities_mapping[region][district] = sorted(region_districts_cities_mapping[region][district])

    return dict(sorted(region_districts_cities_mapping.items(), key=lambda x: x[0]))


def check_city_in_regions(city, regions):
    for region, cities_dict in regions.items():
        for city_group, city_list in cities_dict.items():
            if city in city_list:
                return True
    return False


def drop_cities_not_in_regions(db_path, regions):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Fetch all cities from the database
        cursor.execute("SELECT DISTINCT city FROM properties")
        cities = cursor.fetchall()

        for (city) in cities:
            # Check each city if it's in the provided regions dictionary
            if not check_city_in_regions(city, regions):
                # If city not in regions, delete it from database
                cursor.execute("DELETE FROM properties WHERE city = ?", (city,))
                print(f"Dropped city: {city}")

        # Commit the changes to the database
        conn.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the database connection
        conn.close()


def plot_learning_curves(output_file_name, model, X, y, cv):
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=cv, train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='neg_mean_squared_error', n_jobs=-1)

    train_scores_mean = -np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure()
    plt.title(f"Learning Curves {model.__class__.__name__}")
    plt.xlabel("Training examples")
    plt.ylabel("Mean Squared Error")
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    plt.grid(True)
    plt.savefig(f'{output_file_name}.png')


def preprocess_data(df, offer_type, numeric_columns, float_columns, int_columns, truefalse_columns):
    #top_cities = df['city'].value_counts().nlargest(6).index
    #df = df[df['city'].isin(top_cities)]

    non_numeric_columns = [col for col in df.columns if col not in numeric_columns + truefalse_columns]
    clean_columns(df, float_columns, int_columns, non_numeric_columns)

    # add features
    df['age_of_property'] = datetime.datetime.now().year - df['year_of_construction']
    df['area_per_room'] = df['land_area'] / df['number_of_rooms']
    df['luxury_index'] = df[truefalse_columns].sum(axis=1)
    df['rooms_x_age'] = df['number_of_rooms'] * df['age_of_property']
    df['has_outdoor_space'] = df[['garden', 'gazebo', 'terrace']].any(axis=1).astype(int)
    df['has_wellness_space'] = df[['pool', 'sauna']].any(axis=1).astype(int)
    df['has_parking'] = df[['parking_space', 'garage']].any(axis=1).astype(int)
    #df['price_per_sqm'] = df['price'] / df['land_area']
    #df['is_renovated'] = ((datetime.datetime.now().year - df['year_of_construction']) > 30) & (df['price_per_sqm'] > df['price_per_sqm'].median()).astype(int)
    type_scores = {'Rodinný dom': 2, 'izbový byt': 3, 'garsónka': 1, 'kancelárie': 2, 'pozemok': 3}
    #df['type_score'] = df['type'].map(type_scores)

    # df = df.apply(lambda x: np.log1p(x) if np.issubdtype(x.dtype, np.number) else x)

    clean_columns(df, float_columns,
                  int_columns + ['age_of_property', 'area_per_room', 'luxury_index', 'rooms_x_age'],
                  non_numeric_columns)

    # encode
    df = pd.get_dummies(df, columns=non_numeric_columns, drop_first=False)
    return df


def preprocess_price(y, offer_type):
    y = y.astype(str).apply(lambda x: x.replace('.', '').replace(',', '.') if (
            ',' in x and x.count(',') == 1 and len(x.split(',')[-1]) <= 2) else x.replace(',', ''))
    y = pd.to_numeric(y, errors='coerce')
    y = y.replace([np.inf, -np.inf], np.nan)



    return y