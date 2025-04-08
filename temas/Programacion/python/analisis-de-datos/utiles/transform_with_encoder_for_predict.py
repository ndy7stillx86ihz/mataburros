import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def transform_with_encoder(value: str, encoder: OneHotEncoder) -> pd.DataFrame:
    """" 
    Transforma el valor de una característica numérica en np.array y le cambia
        las dimensiones para poder codificarlo como array 2D mediante el codificador
        One Hot Encoder. Transforma el np.array resultante de la codificación
        a DataFrame.
    Params: 
        logs: list -> lista con todos los valores de las características recolectadas.
    Returns:
        proto_dataframe: pd.DataFrame -> DataFrame con la instancia de 'proto' codificada.
    """
    np_array = np.array(value).reshape(-1, 1)
    encoded = encoder.transform(np_array)
    categories = encoder.categories_[0]
    dataframe = pd.DataFrame(data= encoded, columns= categories)
    
    return dataframe 