import pandas as pd


def count_classes_feature(feature: pd.Series) -> pd.DataFrame:
    """
      Calcula la cantidad de valores para cada clase de una característica.
      Params:
        feature : pd.Series -> característica del DataFrame.
      Returns:
        classes: pd.DataFrame -> DataFrame de la forma clases x cantidad.
    """

    classes: pd.DataFrame = feature.value_counts()
    return classes
