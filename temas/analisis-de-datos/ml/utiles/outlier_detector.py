import numpy as np
import pandas as pd


def outlier_detector(feature: pd.Series) -> list[int | float] | str:
    """
    Calcula para una característica numérica el percentil 25 y el percentil 75,determina el rango intercuartílico, establece los límites para considerar un valor atípico
      y busca los valores atípicos presentes en la característica.
    Params:
      feature : pd.Series -> característica numérica.
    Returns:
      outlier : list[int | float] -> lista con los valores atípicos.
    """
    none = 'No existen valores atípicos en la característica'
    q1 = np.percentile(feature, 25)
    q3 = np.percentile(feature, 75)
    iqr = q3 - q1
    limit_inferior = q1 - 1.5 * iqr
    limit_superior = q3 + 1.5 * iqr
    outlier: list[int | float] = []
    for value in feature:
        if value < limit_inferior or value > limit_superior:
            outlier.append(value)
    if outlier == []:
      return none
    else:
      return outlier
