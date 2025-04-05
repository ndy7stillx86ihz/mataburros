import pandas as pd


def metrics_to_dataframe(accuracy: float, precision: float, recall: float,
                         f1_score: float, estimator: str) -> pd.DataFrame:
    """
    Crea un DataFrame con las métricas empleadas en los conjuntos de pruebas de un estimador.
    Params:
            accuracy: float -> accuracy del estimador.
            precision: float -> precision del estimador.
            recall: float -> recall del estimador.
            f1_score: float -> f1_score del estimador.
            estimator: str -> nombre del estimador utilizado para crear el modelo.
    Returns:metrics: pd.Dataframe -> DataFrame con las métricas, sus valores y el nombre del estimador empleado.
    """
    metrics_list = [[accuracy,precision, recall, f1_score, estimator]]

    metrics = pd.DataFrame(data=metrics_list, columns= ['accuracy', 'precision',
                                                      'recall', 'f1_s',
                                                      'estimator'])
    return metrics

