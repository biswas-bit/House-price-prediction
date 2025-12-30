from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dashboard.ai_model import HousePriceModel
import json
from django.http import JsonResponse
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

@csrf_exempt  
def model_prediction(request):
    # Log request start
    logger.info("=" * 60)
    logger.info("model_prediction API called")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Content-Type: {request.content_type}")
    logger.info(f"Path: {request.path}")
    
    if request.method == 'POST':
        try:
            logger.info("Processing POST request...")
            
            # Check if file is uploaded
            if 'file' in request.FILES:
                csv_file = request.FILES['file']
                logger.info(f"CSV file received: {csv_file.name}")
                logger.info(f"File size: {csv_file.size} bytes")
                logger.info(f"Content type: {csv_file.content_type}")
                
                try:
                    import pandas as pd
                    logger.info("Reading CSV file with pandas...")
                    df = pd.read_csv(csv_file)
                    
                    logger.info(f"CSV loaded successfully. Shape: {df.shape}")
                    logger.info(f"Columns: {list(df.columns)}")
                    logger.info(f"First few rows:\n{df.head(3)}")
                    
                    data = df.to_dict('records')
                    logger.info(f"Converted to {len(data)} records")
                    
                    logger.info("Initializing HousePriceModel...")
                    model = HousePriceModel()
                    logger.info("Model initialized successfully")
                    
                    logger.info("Starting predictions...")
                    predictions = model.predict(data)
                    logger.info(f"Predictions generated: {len(predictions)}")
                    logger.info(f"Sample prediction: {predictions[0] if predictions else 'No predictions'}")
                    
                    # Process results
                    logger.info("Processing results...")
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
                    
                    logger.info(f"Processed {len(results)} results")
                    logger.info(f"Sample result: {results[0] if results else 'No results'}")
                    
                    # Log summary statistics
                    if results:
                        prices = [r['predicted_price'] for r in results]
                        logger.info(f"Price stats - Min: ${min(prices):,.2f}, Max: ${max(prices):,.2f}, Avg: ${sum(prices)/len(prices):,.2f}")
                    
                    response_data = {
                        'success': True,
                        'predictions': results,
                        'count': len(results)
                    }
                    
                    logger.info(f"Returning successful response with {len(results)} predictions")
                    logger.info("-" * 40)
                    
                    return JsonResponse(response_data)
                    
                except Exception as file_error:
                    logger.error(f"Error processing CSV file: {str(file_error)}")
                    logger.error(f"File processing error details:", exc_info=True)
                    raise file_error
            
            # No file uploaded - return test prediction
            logger.info("No file uploaded, returning test prediction...")
            
            model = HousePriceModel()
            logger.info("Model initialized for test prediction")
            
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
            
            logger.info("Generating test prediction...")
            logger.info(f"Test data keys: {list(test_data.keys())}")
            
            prediction = model.predict(test_data)
            logger.info(f"Test prediction generated: {prediction[0] if prediction else 'No prediction'}")
            
            response_data = {
                'success': True,
                'prediction': prediction[0] if prediction else 0,
                'test_mode': True
            }
            
            logger.info(f"Returning test response: {response_data}")
            logger.info("-" * 40)
            
            return JsonResponse(response_data)
            
        except Exception as e:
            logger.error("=" * 60)
            logger.error("EXCEPTION in model_prediction:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            logger.error("Full traceback:", exc_info=True)
            logger.error("=" * 60)
            
            import traceback
            error_response = {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'traceback': traceback.format_exc()
            }
            
            return JsonResponse(error_response, status=500)
    
    # Handle non-POST requests
    logger.warning(f"Invalid request method: {request.method}")
    logger.warning("Only POST requests are allowed")
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are allowed',
        'received_method': request.method
    }, status=405)