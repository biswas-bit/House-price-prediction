from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dashboard.ai_model import HousePriceModel
import json
from django.http import JsonResponse
import logging
from realstate.forms import HouseForm
import pandas as pd
from datetime import datetime
from django.db.models import Avg, Count, Q
from django.core.cache import cache

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
                "Id":1,
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
    
    
def Data_input_form(request):
    print("=" * 50)
    print("Data_input_form view called")
    
    if request.method == 'POST':
        print("POST request received")
        print(f"POST data keys: {list(request.POST.keys())}")
        
        form = HouseForm(request.POST)
        print(f"Form instantiated with POST data")
        print(f"Form is bound: {form.is_bound}")
        
        if form.is_valid():
            print("✓ Form is valid")
            cleaned_data = form.cleaned_data
            print(f"✓ Cleaned data keys: {list(cleaned_data.keys())}")
            print(f"✓ TotalBsmtSF: {cleaned_data.get('TotalBsmtSF')}")
            print(f"✓ GrLivArea: {cleaned_data.get('GrLivArea')}")
            
            # Save to session or process further
            request.session['form_data'] = cleaned_data
            
            # Redirect to success page or process prediction
            return render(request, 'home/form.html', {
                'form': form, 
                'cleaned_data': cleaned_data,
                'success': True
            })
        else:
            print("✗ Form is INVALID")
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")
            
            # Debug specific fields
            for field_name, errors in form.errors.items():
                print(f"Field '{field_name}': {errors}")
            
            return render(request, 'home/form.html', {
                'form': form,
                'errors': form.errors
            })
    
    else:
        print("GET request received")
        form = HouseForm()
        print("GET request - rendering empty form")
    
    return render(request, 'home/form.html', {'form': form})

# apis
def get_market_insights(requets):
    """ Api end points for market insights data"""
    try:
        model = HousePriceModel()
        insights = {
            'avg_price_trend':'+5.2%',
            'days_on_market':42,
            'top_neighborhood':[
                {'name':'NoRidge','avg_price':750000},
                {'name':'StoneBr','avg_price':680000},
                {'name':'Nridght','avg_price':68000}
            ],
            'feature_impace':[
                {'feature':"OverallQual",'impact':0.85},
                {'feature':"GrlivArea",'impace':0.76},
                {'feature':"GarageCars",'impace':0.68}
                ],
            'model_metrics':{
                'accuracy':91.5,
                'error_margin':3.2,
                'r2_score':0.89
            },
            'seasonal_trends': [
                {'month': 'Jan', 'avg_price': 280000},
                {'month': 'Feb', 'avg_price': 285000},
                {'month': 'Mar', 'avg_price': 295000},
                {'month': 'Apr', 'avg_price': 305000},
                {'month': 'May', 'avg_price': 315000},
                {'month': 'Jun', 'avg_price': 325000},
                {'month': 'Jul', 'avg_price': 320000},
                {'month': 'Aug', 'avg_price': 310000},
                {'month': 'Sep', 'avg_price': 300000},
                {'month': 'Oct', 'avg_price': 290000},
                {'month': 'Nov', 'avg_price': 285000},
                {'month': 'Dec', 'avg_price': 280000}
            ],
             'property_distribution': [
                {'type': 'Single Family', 'percentage': 45},
                {'type': 'Townhouse', 'percentage': 25},
                {'type': 'Condo', 'percentage': 15},
                {'type': 'Multi-Family', 'percentage': 10},
                {'type': 'Luxury', 'percentage': 5}
            ]
        }
        
        return JsonResponse({
            'success': True,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
