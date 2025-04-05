import numpy as np
import pandas as pd


def parse_one_hot_encoded_feature(encoder: np.float64, feature: pd.Series) -> pd.DataFrame:
    """
    Codifica la característica categórica con One Hot Encoder, transforma la salida del array numpy a DataFrame y asigna a cada categoría creada
      como nombre a su columna en el DataFrame.
    Params:
      encoder: np.float64 -> codificador creado con One Hot Encoder.
      features: pd.Series -> característica categórica del conjunto para entrenamiento a codificar.    
    Returns:
      dataframe_encoded: pd.DataFrame -> DataFrame con las clases codificadas.
    """

    encoded_feature = encoder.fit_transform(feature)
    dataframe_encoded = pd.DataFrame(encoded_feature)
    categories = encoder.categories_[0]
    replace: dict[int: str] = {}
    for columns, category in zip(dataframe_encoded.columns, categories):
        replace[columns] = category
    dataframe_encoded.rename(
        columns=replace,
        inplace=True
    )
    return dataframe_encoded
