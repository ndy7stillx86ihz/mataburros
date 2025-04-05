import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler



def prediction( dataset: pd.DataFrame, 
               estimator: LabelEncoder | OneHotEncoder| DecisionTreeClassifier 
               | RandomForestClassifier | ExtraTreesClassifier | xgb.XGBClassifier,
               encoder: LabelEncoder) -> str:
    """"
    Realiza la predicción con el estimador, decodifica la clase obtenida y extrae
        del np array el valor.
    Params: 
        dataset: pd.DataFrame -> DataFrame con las transformaciones necesarias
            para que un estimador realice la predicción.
        estimator: LabelEncoder | OneHotEncoder| DecisionTreeClassifier 
               | RandomForestClassifier | ExtraTreesClassifier |
               xgb.XGBClassifier -> estimador con el que se realizará
               la predicción.
        encoder: LabelEncoder -> codificador entrenado para transformar 
            a la clase objetivo.
    Returns:
        class_predict: str -> clase de la variable objetivo predicha.           
    """
    estimator_predict = estimator.predict(dataset)
    encoded_prediction = encoder.inverse_transform(estimator_predict)
    class_predict = encoded_prediction[0]
    
    return class_predict