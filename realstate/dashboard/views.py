from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dashboard.ai_model import HousePriceModel
import json
from django.http import JsonResponse
import logging

logs = logging.getLogger(__name__)

@csrf_exempt  
def model_prediction(request):
    if request.method == 'POST':
        try:
            
            if 'file' in request.FILES:
                csv_file = request.FILES['file']
              
                import pandas as pd
                df = pd.read_csv(csv_file)
                data = df.to_dict('records')
                
          
                model = HousePriceModel()
                predictions = model.predict(data)
                
                
                results = []
                for i, (record, pred) in enumerate(zip(data, predictions)):
                    results.append({
                        'id': i + 1,
                        'bedrooms': record.get('BedroomAbvGr', 0),
                        'bathrooms': record.get('FullBath', 0),
                        'sqft_living': record.get('GrLivArea', 0),
                        'neighborhood': record.get('Neighborhood', 'Unknown'),
                        'year_built': record.get('YearBuilt', 0),
                        'predicted_price': pred
                    })
                
                return JsonResponse({
                    'success': True,
                    'predictions': results,
                    'count': len(results)
                })
            
            
            model = HousePriceModel()
            test_data = {
                "Id": 1461,
                "MSSubClass": 20,
                "MSZoning": "RH",
                "LotFrontage": 80,
                "LotArea": 11622,
                "Street": "Pave",
                "Alley": "NA",
                "LotShape": "Reg",
                "LandContour": "Lvl",
                "Utilities": "AllPub",
                "LotConfig": "Inside",
                "LandSlope": "Gtl",
                "Neighborhood": "NAmes",
                "Condition1": "Feedr",
                "Condition2": "Norm",
                "BldgType": "1Fam",
                "HouseStyle": "1Story",
                "OverallQual": 5,
                "OverallCond": 6,
                "YearBuilt": 1961,
                "YearRemodAdd": 1961,
                "RoofStyle": "Gable",
                "RoofMatl": "CompShg",
                "Exterior1st": "VinylSd",
                "Exterior2nd": "VinylSd",
                "MasVnrType": "None",
                "MasVnrArea": 0,
                "ExterQual": "TA",
                "ExterCond": "TA",
                "Foundation": "CBlock",
                "BsmtQual": "TA",
                "BsmtCond": "TA",
                "BsmtExposure": "No",
                "BsmtFinType1": "Rec",
                "BsmtFinSF1": 468,
                "BsmtFinType2": "LwQ",
                "BsmtFinSF2": 144,
                "BsmtUnfSF": 270,
                "TotalBsmtSF": 882,
                "Heating": "GasA",
                "HeatingQC": "TA",
                "CentralAir": "Y",
                "Electrical": "SBrkr",
                "1stFlrSF": 896,
                "2ndFlrSF": 0,
                "LowQualFinSF": 0,
                "GrLivArea": 896,
                "BsmtFullBath": 0,
                "BsmtHalfBath": 0,
                "FullBath": 1,
                "HalfBath": 0,
                "BedroomAbvGr": 2,
                "KitchenAbvGr": 1,
                "KitchenQual": "TA",
                "TotRmsAbvGrd": 5,
                "Functional": "Typ",
                "Fireplaces": 0,
                "FireplaceQu": "NA",
                "GarageType": "Attchd",
                "GarageYrBlt": 1961,
                "GarageFinish": "Unf",
                "GarageCars": 1,
                "GarageArea": 730,
                "GarageQual": "TA",
                "GarageCond": "TA",
                "PavedDrive": "Y",
                "WoodDeckSF": 140,
                "OpenPorchSF": 0,
                "EnclosedPorch": 0,
                "3SsnPorch": 0,
                "ScreenPorch": 120,
                "PoolArea": 0,
                "PoolQC": "NA",
                "Fence": "MnPrv",
                "MiscFeature": "NA",
                "MiscVal": 0,
                "MoSold": 6,
                "YrSold": 2010,
                "SaleType": "WD",
                "SaleCondition": "Normal"
            }
    
            prediction = model.predict(test_data)
            return JsonResponse({
                'success': True,
                'prediction': prediction[0],
                'test_mode': True
            })
            
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

