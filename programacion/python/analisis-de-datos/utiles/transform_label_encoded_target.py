import pandas as pd
from sklearn.preprocessing import LabelEncoder

def transform_label_encoded(encoder: LabelEncoder, target_test: pd.Series) -> pd.DataFrame:
  """
  Transforma la variable objetivo mediante el codificador entrenado y convierte el array np
    en un DataFrame.
  Params:
    encoder: LabelEncoder -> codificador Labelencoder entrenado.
    target_test: pd.series -> variable objetivo en el conjunto de prueba.
  Returns:
    target: pd.dataFrame -> DataFrame con las clases de la variable objetivo
      codificadas.
  """
  column_name= target_test.name
  enc_target_test = encoder.transform(target_test)
  target = pd.DataFrame(data= enc_target_test, columns=[column_name])
  return target