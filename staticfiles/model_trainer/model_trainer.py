import getpass
import os
import platform
import time

import joblib
import matplotlib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from skopt import BayesSearchCV

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from unicodedata import normalize
from xgboost import XGBRegressor

matplotlib.use('TkAgg')

from helper import *


def get_db_file_path():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'database.db')
    elif system == 'Linux':
        return os.path.join(f'/home/scraping-control', 'RealEstateWebScraper', 'database.db')
    else:
        raise NotImplementedError('Unsupported operating system')


def get_model_file_path(offer_type):
    system = platform.system()
    if system == 'Windows':
        if offer_type == 'Predaj':
            return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'predaj_model.pkl')
        elif offer_type == 'Prenájom':
            return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'prenajom_model.pkl')
    elif system == 'Linux':
        if offer_type == 'Predaj':
            return os.path.join(f'/home/scraping-control', 'RealEstateWebScraper', 'predaj_roddom_model.pkl')
        elif offer_type == 'Prenájom':
            return os.path.join(f'/home/scraping-control', 'RealEstateWebScraper', 'prenajom_roddom_model.pkl')
    else:
        raise NotImplementedError('Unsupported operating system')


def normalize_string(s):
    return normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii').lower()


connection = sqlite3.connect(get_db_file_path())
query = "SELECT * FROM properties"
df = pd.read_sql_query(query, connection)

df = df.replace("Nepoznané", np.nan)
df = df.replace("Nezadaná", np.nan)
df = df.replace("NULL", np.nan)
df = df.replace("Cena", np.nan)
df = df.replace("Info", np.nan)
df = df.replace(u"\\xa0", u'')

offer_types = ['Predaj']

cols_to_drop = [
    'id',
    'website',
    'title',
    'district',
    'street',
    'city',
    'offer_type',
    'type',
    'ownership',
    'date_posted',
    'short_description',
    'property_condition',
    'long_description',
    'timestamp',
    'url',
]

float_columns = [
    'land_area',
    'latitude',
    'longitude'
]

int_columns = [
    'year_of_construction',
    'number_of_rooms',
]

truefalse_columns = [
    'parking_space',
    'basement',
    'gazebo',
    'terrace',
    'pool',
    'air_conditioning',
    'sauna',
    'balcony',
    'garage',
    'loggia',
    'garden',
    'fireplace',
    'bathroom',
    'lift',
    'new_building'
]

numeric_columns = float_columns + int_columns

models_param_grid = [
    {
        'model': GradientBoostingRegressor(random_state=42),
        'params': {
            'n_estimators': [100, 300, 500, 700],
            'learning_rate': [0.01, 0.05, 0.1, 0.5],
            'max_depth': [None, 5, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 3, 5, 10],
            'max_features': ['sqrt', 'log2']
        }
    },
    {
        'model': RandomForestRegressor(random_state=42),
        'params': {
            'n_estimators': [100, 300, 500, 700],
            'max_depth': [None, 5, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 3, 5, 10],
            'max_features': ['sqrt', 'log2']
        }
    },
    {
        'model': XGBRegressor(random_state=42),
        'params': {
            'n_estimators': [100, 300, 500, 700],
            'learning_rate': [0.01, 0.05, 0.1, 0.5],
            'max_depth': [3, 5, 7, 10],
            'min_child_weight': [1, 3, 5],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
        }
    },
    {
        'model': KNeighborsRegressor(),
        'params': {
            'n_neighbors': [3, 5, 7, 10, 15],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        }
    },
    {
        'model': DecisionTreeRegressor(random_state=42),
        'params': {
            'max_depth': [None, 5, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 3, 5, 10]
        }
    },
    {
        'model': Ridge(random_state=42),
        'params': {
            'alpha': [0.1, 0.5, 1.0, 2.0]
        }
    },
    {
        'model': Lasso(random_state=42),
        'params': {
            'alpha': [0.1, 0.5, 1.0, 2.0]
        }
    },
]

scoring = {
    'MSE': make_scorer(mean_squared_error, greater_is_better=False),
    'MAE': make_scorer(mean_absolute_error, greater_is_better=False)
}

i = 0

for offer_type in offer_types:
    df_copy = df.copy(deep=True)

    df_copy = df_copy[df_copy['offer_type'].isin([offer_type])]
    df_copy = df_copy[df_copy['type'].apply(normalize_string).str.contains(normalize_string('izbovy byt'))]
    df_copy = df_copy[df_copy['city'].apply(normalize_string).str.contains(normalize_string('kosice'))]


    # filter price
    if offer_type == 'Prenájom':
        lower_price_bound = 100
        upper_price_bound = 5000
    else:
        lower_price_bound = 50000
        upper_price_bound = 180000
    df_copy['price'] = pd.to_numeric(df_copy['price'], errors='coerce')
    df_copy = df_copy[(df_copy['price'] >= lower_price_bound) & (df_copy['price'] <= upper_price_bound)]

    # filter area
    lower_land_area_bound = 30
    upper_land_area_bound = 85
    df_copy['land_area'] = pd.to_numeric(df_copy['land_area'], errors='coerce')
    df_copy = df_copy[(df_copy['land_area'] >= lower_land_area_bound) & (df_copy['land_area'] <= upper_land_area_bound)]

    # filter years
    lower_year_bound = 1500
    upper_year_bound = 2024
    #df_copy['year_of_construction'] = pd.to_numeric(df_copy['year_of_construction'], errors='coerce')
    #df_copy = df_copy[(df_copy['year_of_construction'] >= lower_year_bound) & (df_copy['year_of_construction'] <= upper_year_bound)]

    df_copy = remove_outliers(df_copy, int_columns, float_columns)

    # Split the data
    X = preprocess_data(df_copy.drop(cols_to_drop + ['price'], axis=1), offer_type, numeric_columns, float_columns, int_columns, truefalse_columns)
    y = preprocess_price(df_copy['price'], offer_type)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Initialization
    model_results = []

    output_file_name = normalize("NFKD", f'{get_model_file_path(offer_type)}').encode('ascii', 'ignore').decode('utf-8').lower()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    for model in models_param_grid:
        start_time = time.time()
        bayes_search = BayesSearchCV(
            estimator=model['model'],
            search_spaces=model['params'],
            cv=kf,
            n_iter=50,
            scoring='neg_mean_squared_error',
            n_jobs=-1,
            return_train_score=True,
            random_state=42,
            verbose=3
        )
        bayes_search.fit(X_train, y_train)

        end_time = time.time()
        elapsed_time = end_time - start_time

        val_score = bayes_search.score(X_test, y_test)
        y_pred = bayes_search.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results = {
            'Model': model['model'].__class__.__name__,
            'Val Score': val_score,
            'Best Parameters': bayes_search.best_params_,
            'Best Score (MSE)': -bayes_search.best_score_,
            'Test MSE': mse,
            'Test RMSE': rmse,
            'Test MAE': mae,
            'Test R2': r2,
            'Testing took (seconds)': elapsed_time,
            'Prediction': y_pred[:1]
        }
        temp = [results]

        # results
        model_results.append(results)
        print(model_results)

    results_test_df = pd.DataFrame(model_results)
    results_test_df = results_test_df.sort_values(by='Test MSE', ascending=True)
    results_test_df.to_excel(f'{i}.xlsx')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print(results_test_df)

    best_model_index = results_test_df['Test MSE'].idxmin()
    best_model_info = model_results[best_model_index]
    best_model = models_param_grid[best_model_index]['model'].set_params(**best_model_info['Best Parameters'])
    best_model.fit(X_train, y_train)
    joblib.dump(best_model, output_file_name)
    i+=1

exit(0)
