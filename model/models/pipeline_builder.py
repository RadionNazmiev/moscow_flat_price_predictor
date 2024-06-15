import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from category_encoders import TargetEncoder

def create_pipeline(model, columns_for_MTE, columns_for_OHE, numerical_columns):
    """
    This function creates a machine learning pipeline using Scikit-learn.
    The pipeline includes preprocessing steps for numerical, mean target 
    encoded, and one-hot encoded features.

    Parameters:
    -----------
    model : object
        The machine learning model to be used in the pipeline.
    columns_for_MTE : list
        List of column names for mean target encoding.
    columns_for_OHE : list
        List of column names for one-hot encoding.
    numerical_columns : list
        List of column names for numerical features.

    Returns:
    --------
    pipeline : object
        A Scikit-learn pipeline object that can be used for training and 
        prediction.
    """

    # Define a pipeline for numerical features
    numerical_pipe = Pipeline([
        ('minmaxscaler', MinMaxScaler())
    ])

    # Define a pipeline for mean target encoded features
    mean_target_pipe = Pipeline([
        ('mean_target', TargetEncoder())
    ])

    # Define a pipeline for one-hot encoded features
    one_hot_pipe = Pipeline([
        ('one_hot', OneHotEncoder(drop='first'))
    ])

    # Combine the preprocessing pipelines into a single ColumnTransformer
    col_transformer = ColumnTransformer([
            ('numerical_pipeline', numerical_pipe, numerical_columns),
            ('mean_target_pipeline', mean_target_pipe, columns_for_MTE),
            ('one_hot_pipeline', one_hot_pipe, columns_for_OHE),
        ],
        remainder='drop'
    )

    # Combine the preprocessing steps with the machine learning model into 
    # a single pipeline
    pipeline = Pipeline([
        ('preprocessor', col_transformer),
        ('model', model)
    ])
    return pipeline


def grid_search_cv(
    X, 
    y, 
    model_configs,
    columns_for_MTE, 
    columns_for_OHE,
    numerical_columns
    ):
    """
    Perform grid search cross-validation for multiple machine learning models.

    Parameters:
    -----------
    X : array-like
        The input features for the machine learning models.
    y : array-like
        The target variable for the machine learning models.
    model_configs : dict
        A dictionary containing the machine learning models and their respective 
        hyperparameter grids. The keys are the model names, and the values are 
        dictionaries with 'odel' and 'params' keys.
    columns_for_MTE : list
        List of column names for mean target encoding.
    columns_for_OHE : list
        List of column names for one-hot encoding.
    numerical_columns : list
        List of column names for numerical features.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the model names, best scores, and best 
        parameters for each model.
    """

    results = []
    kfold_split = KFold(n_splits=5, shuffle=True, random_state=0)

    for model_name, config in model_configs.items():
        model_class = config['model']
        params = config['params']

        pipeline = create_pipeline(
            model_class(), 
            columns_for_MTE, 
            columns_for_OHE,
            numerical_columns
        )

        gs = GridSearchCV(
            pipeline,
            params,
            cv=kfold_split,
            scoring='neg_mean_squared_error',
            return_train_score=True,
            error_score='raise'
        )

        try:
            gs.fit(X, y)
            results.append({
                'model': model_name,
                'best_score': -gs.best_score_,
                'best_params': gs.best_params_

            })
        except Exception as e:
            print(f"Error fitting model {model_name}: {e}")

    return results