import pandas as pd
import scipy.stats as scp


def classifier_type_distribution(dataset: pd.DataFrame) -> dict[str: str]:
    """
    Calcula la curtosis de pearson para todas las características numéricas de un DataFrame y de acuerdo a su valor las clasifica.
    Params:
      dataset: pd.DataFrame -> DataFrame.
    Returns:
      type_distribution: dict[str: str] -> diccionario con cada característica númerica y su tipo de distribución.
    """
    dataset_numeric = dataset.select_dtypes(exclude=object)
    type_distribution: dict[str: str] = {}
    
    for column in dataset_numeric:
        kurtosis_pearson: float = scp.kurtosis(
            a=dataset_numeric[column], fisher=False)
        if kurtosis_pearson == 3:
            type_distribution[column] = "mesocúrtica"
        elif kurtosis_pearson > 3:
            type_distribution[column] = "leptocúrtica"
        elif kurtosis_pearson < 3:
            type_distribution[column] = "platicúrtica"
            
    return type_distribution
