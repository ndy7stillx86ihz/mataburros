import pandas as pd


def class_labels( dataset : pd.DataFrame) -> dict[str: [list[int| float| str]]]:
    """
    Determina para cada característica de un DataFrame las clases únicas que la conforman.
    Params:
    dataset: pd.DataFrame -> DataFrame.
    Returns:
    dict_unique_classes : dict [str : list [str | int | float] ] -> diccionario con cada característica del DataFrame y las listas con sus clases únicas.
    """

    unique_classes : list[str | int | float] = []
    dict_unique_classes : dict [str : list [str | int | float] ]= {}
    for columns in dataset:
        unique_classes= dataset[columns].unique()
        dict_unique_classes[columns] = unique_classes
    return dict_unique_classes
