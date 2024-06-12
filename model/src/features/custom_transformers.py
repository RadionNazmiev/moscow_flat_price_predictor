import itertools

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin



class CustomTransformer(BaseEstimator, TransformerMixin):
    """
    Custom transformer for preprocessing categorical and numerical features.
    
    Parameters:
    -----------
    cat_columns : list, default=[]
        List of categorical columns to be transformed.
    target_name : str, default='Price'
        Name of the target variable for mean target encoding.
    """
    
    def __init__(self, cat_columns=[], target_name='Price'):
        self.cat_columns = cat_columns  
        self.target_name = target_name  

    def fit(self, X, y):
        """
        Fit the transformer on the data.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix.
        y : Series
            Target variable.
        
        Returns:
        --------
        self : object
            Fitted transformer.
        """
        self.num_columns = [
            col 
            for col in X.columns
            if col not in self.cat_columns
        ]

        df_fit = pd.concat((X, y), axis=1)

        # Separate columns for one-hot encoding (OHE) 
        # and mean target encoding (MTE)
        self.col_names_for_ohe = [
            col 
            for col in self.cat_columns 
            if df_fit[col].nunique() <= 5
        ]
        self.col_names_for_mte = [
            col 
            for col in self.cat_columns 
            if df_fit[col].nunique() > 5
        ]

        # Generate binary column names for OHE
        self.dict_of_bin_col_names = {
            col: [f"{col}_{value}" for value in sorted(df_fit[col].unique())]
            for col in self.col_names_for_ohe
        }

        # Calculate mean target values for MTE
        self.dict_of_means = {
            col: df_fit.groupby(col)[self.target_name].mean()
            for col in self.col_names_for_mte
        }

        return self

    def transform(self, X, y=None):
        """
        Transform the data using the fitted transformer.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix.
        y : Series, optional
            Target variable (not used in transform).
        
        Returns:
        --------
        X_transformed : DataFrame
            Transformed feature matrix.
        """
        # Apply mean target encoding
        for col in self.col_names_for_mte:
            mean_value = self.dict_of_means[col].mean()
            X[col] = X[col].map(self.dict_of_means[col]).fillna(mean_value)

        # Apply one-hot encoding
        bin_feats_df = pd.get_dummies(
            X[self.col_names_for_ohe], 
            prefix=self.col_names_for_ohe
        )
        X = X.drop(self.col_names_for_ohe, axis=1)

        # Ensure all OHE columns are present
        all_bin_col_names = ( 
            list(itertools.chain(*self.dict_of_bin_col_names.values()))
        )
        
        missing_columns = [
            col 
            for col in all_bin_col_names 
            if col not in bin_feats_df.columns
        ]

        if missing_columns:
            missing_df = pd.DataFrame(0, index=X.index, columns=missing_columns)
            bin_feats_df = pd.concat([bin_feats_df, missing_df], axis=1)

        # Drop extra columns that weren't in the fitting stage
        extra_columns = [
            col 
            for col in bin_feats_df.columns 
            if col not in all_bin_col_names
        ]
        
        bin_feats_df = bin_feats_df.drop(extra_columns, axis=1)

        # Drop the first binary column for each categorical feature 
        # (to avoid multicollinearity)
        first_bin_col_to_drop = [
            cols[0] 
            for cols in self.dict_of_bin_col_names.values()
        ]
        bin_feats_df = bin_feats_df.drop(first_bin_col_to_drop, axis=1)

        # Concatenate the numerical features with 
        # the encoded categorical features
        X_transformed = pd.concat([X, bin_feats_df], axis=1)
        
        return X_transformed
