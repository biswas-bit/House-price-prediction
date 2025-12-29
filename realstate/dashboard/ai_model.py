import numpy as np
import pandas as pd
import os
import joblib
from django.conf import settings


class HousePriceModel:
    def __init__(self):
        model_path = os.path.join(settings.BASE_DIR,'dashboard','xgb_pipeline_with_features.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.model = joblib.load(model_path)
        artifact = joblib.load(model_path)
        self.model = artifact['model']
        self.features = artifact['features']

    def predict(self, data: dict | list[dict]):
        df = pd.DataFrame(data if isinstance(data, list) else [data])
        predictions = self.model.predict(df)
        return [float(p) for p in predictions]
    
    



