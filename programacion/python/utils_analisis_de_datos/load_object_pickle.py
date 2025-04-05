import pickle as p
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import xgboost as xgb



def load_object(
    path: str
                ) ->  LabelEncoder | OneHotEncoder| DecisionTreeClassifier | RandomForestClassifier | ExtraTreesClassifier | xgb.XGBClassifier | LogisticRegression | StandardScaler:
    """
    Carga el objeto en formato pickle existente en la ruta.
    Params:
        path: str -> ruta absoluta del objeto en formato pickle.
    Returns:
        object: LabelEncoder | OneHotEncoder| DecisionTreeClassifier 
            | RandomForestClassifier | ExtraTreesClassifier | xgb.XGBClassifier
            | LogisticRegression-> codificador o estimador.
    """
    with open(path, 'rb') as file:
        object = p.load(file)
        
    return object