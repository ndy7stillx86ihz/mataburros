from sklearn.preprocessing import LabelEncoder
import pandas as pd


def parse_label_encoded(encoder: LabelEncoder, target_train: pd.Series) -> pd.DataFrame:
    """
    Entrena el codificador Label Encoder con las clases de la variable objetivo y transforma
        a DataFrame.
    Params:
        encoder: LabelEncoder -> codificador para la variable objetivo.
        target_train: pd.Series -> variable objetivo en el conjunto de entrenamiento.
    Returns:
        target : pd.DataFrame -> DataFrame con la variable objetivo codificada.
    """
    column_name= target_train.name
    encoded_target_train = encoder.fit_transform(target_train)
    target = pd.DataFrame(data=encoded_target_train, columns=[column_name])
    return target