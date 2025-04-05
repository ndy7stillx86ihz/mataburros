import csv


def csv_with_predict(path: str, logs: list[str|float]) -> csv:
    """
    Crea un csv en la ruta agregando al final la lista.
    Params:
        path: str -> ruta para el archivo en formato csv.
        logs: list[str|float -> lista de los valores de
            las características con las que se entrenaron los 
            estimadores y en la que se incluye la predicción 
            realizada por un modelo.
    Returns:
        writer: csv -> csv con la lista como fila.
    """
    with open(path, 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(logs)
    return writer