import numpy as np
import pandas as pd


def transform_one_hot_feature(encoder: np.float64, feature: pd.Series) -> pd.DataFrame:
    """
    Transforma la característica mediante las clases aprendidas en el codificador One Hot Encoder, transforma la salida de array numpy a DataFrame y asigna
      cada categoría como nombre de su columna en el DataFrame.
    Params:
      encoder: np.float64 -> codificador One Hot Encoder entrenado con las clases de la característica.
      feature: pd.Series -> característica categórica del conjunto para entrenamiento.
    Returns:
      dataframe_transform: pd.DataFrame -> DataFrame con las clases codificadas.
    """

    transform_feature = encoder.transform(feature)
    dataframe_transform = pd.DataFrame(transform_feature)
    categories = encoder.categories_[0]
    replace: dict[int: str] = {}
    for columns, category in zip(dataframe_transform.columns, categories):
        replace[columns] = category
    dataframe_transform.rename(
        columns=replace,
        inplace=True
    )
    return dataframe_transform
