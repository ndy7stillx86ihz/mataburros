import pandas as pd
from sklearn.preprocessing import StandardScaler



def fit_scaler(scaler: StandardScaler, dataset_numeric : pd.DataFrame) -> pd.DataFrame:
    """"
    Ajusta un escalador del tipo StandardScaler, de acuerdo a los valores de las características 
    del tipo nuéricas del DataFrame para entrenamiento.
    Params:
        scaler: StandardScaler -> escalador StandardScaler.
        dataset_numeric: pd.DataFrame -> DataFrame de características numéricas para entrenamiento.
    Returns:
        dataset_scaled_numerical: pd.DataFrame -> DataFrame con los valores escalados.  
    """
    scaled_numerical = scaler.fit_transform(dataset_numeric)
    dataset_scaled_numerical = pd.DataFrame(data= scaled_numerical, columns= dataset_numeric.columns)
    return dataset_scaled_numerical