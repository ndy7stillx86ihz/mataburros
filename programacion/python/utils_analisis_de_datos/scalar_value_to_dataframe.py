import pandas as pd

def scalar_to_dataframe(scalar: float, name_column: str) -> pd.DataFrame:
    """
    Transforma una instancia escalar en un DataFrame.
    Params:
        scalar: float -> instancia de una característica.
        name_column: str -> característica a la que pertenece 
            la instancia.
    Returns:
        dataframe: pd.DataFrame -> dataframe 2D con la instancia y la
            característica.
    """
    scalar_to_Series = pd.Series(data= scalar)
    dataframe = pd.DataFrame(data= scalar_to_Series, columns= [name_column])
    
    return dataframe