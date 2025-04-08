import pandas as pd
from sklearn.preprocessing import StandardScaler

def transform_scaler(scaler: StandardScaler, dataset_numeric: pd.DataFrame) -> pd.DataFrame:
    """"
    Transforma los valores de las características del DataFrame a partir del
    escalador ajustado.
    Params:
        scaler: StandardScaler -> escalador ajustado.
        dataset_numeric: pd.DataFrame -> DataFrame de características numéricas
            del DataFrame para pruebas.
    Returns:
        dataset_scaled_numerical_test: pd.DataFrame -> DataFrame con los valores escalados.
    """
    np_array = scaler.transform(dataset_numeric)
    dataset_scaled_numerical_test = pd.DataFrame(data=np_array, columns=dataset_numeric.columns)
    return dataset_scaled_numerical_test