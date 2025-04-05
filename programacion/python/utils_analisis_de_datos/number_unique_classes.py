import pandas as pd


def number_unique_classes(dataset: pd.DataFrame) -> dict[str: int]:
    """
    Calcula la cantidad de valores únicos presentes en cada característica de un DataFrame.
    Params:
      dataset : pd.DataFrame -> DataFrame.
    Returns:
      unique_values : dict [str: int] -> diccionario concada característica y su cantidad de valores únicos.
    """

    unique_values: dict[str: int] = {}
    for column in dataset.columns:
        unique_values[column] = dataset[column].nunique()

    return unique_values
