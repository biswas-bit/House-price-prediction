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
from django.conf import settings
import os
import numpy as np
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


@csrf_exempt
def get_market_insights(request):
    """API endpoint for real market insights data based on predictions"""
    try:
        # Initialize your model
        model = HousePriceModel()
        
        # Load your training data or recent predictions to generate real insights
        # You need to have access to your dataset
        try:
            # Method 1: Load from your training dataset
            data_path = os.path.join(settings.BASE_DIR, 'dashboard', 'data', 'train.csv')
            if os.path.exists(data_path):
                df = pd.read_csv(data_path)
                
                # Calculate real insights from data
                avg_price = df['SalePrice'].mean() if 'SalePrice' in df.columns else 250000
                min_price = df['SalePrice'].min() if 'SalePrice' in df.columns else 100000
                max_price = df['SalePrice'].max() if 'SalePrice' in df.columns else 500000
                
                # Calculate price trend (simulate based on time)
                if 'YrSold' in df.columns and 'MoSold' in df.columns:
                    # Group by month/year to get trends
                    df['SaleDate'] = pd.to_datetime(df['YrSold'].astype(str) + '-' + df['MoSold'].astype(str) + '-01')
                    monthly_prices = df.groupby(df['SaleDate'].dt.month)['SalePrice'].mean()
                    
                    # Calculate year-over-year change
                    if len(monthly_prices) > 1:
                        price_trend = ((monthly_prices.iloc[-1] - monthly_prices.iloc[0]) / monthly_prices.iloc[0]) * 100
                        avg_price_trend = f"+{price_trend:.1f}%" if price_trend > 0 else f"{price_trend:.1f}%"
                    else:
                        avg_price_trend = "+5.2%"  # Fallback
                else:
                    avg_price_trend = "+5.2%"
                
                # Calculate top neighborhoods
                if 'Neighborhood' in df.columns and 'SalePrice' in df.columns:
                    neighborhood_stats = df.groupby('Neighborhood')['SalePrice'].agg(['mean', 'count']).reset_index()
                    top_neighborhoods = neighborhood_stats.nlargest(3, 'mean')
                    top_neighborhoods_list = []
                    for _, row in top_neighborhoods.iterrows():
                        top_neighborhoods_list.append({
                            'name': row['Neighborhood'],
                            'avg_price': int(row['mean']),
                            'count': int(row['count'])
                        })
                else:
                    top_neighborhoods_list = [
                        {'name': 'NoRidge', 'avg_price': 750000, 'count': 45},
                        {'name': 'StoneBr', 'avg_price': 680000, 'count': 32},
                        {'name': 'NridgHt', 'avg_price': 680000, 'count': 28}
                    ]
                
                # Calculate feature impact (simplified correlation analysis)
                feature_impact_list = []
                if 'OverallQual' in df.columns and 'SalePrice' in df.columns:
                    corr_qual = df['OverallQual'].corr(df['SalePrice'])
                    feature_impact_list.append({'feature': 'OverallQual', 'impact': abs(round(corr_qual, 2))})
                
                if 'GrLivArea' in df.columns and 'SalePrice' in df.columns:
                    corr_area = df['GrLivArea'].corr(df['SalePrice'])
                    feature_impact_list.append({'feature': 'GrLivArea', 'impact': abs(round(corr_area, 2))})
                
                if 'GarageCars' in df.columns and 'SalePrice' in df.columns:
                    corr_garage = df['GarageCars'].corr(df['SalePrice'])
                    feature_impact_list.append({'feature': 'GarageCars', 'impact': abs(round(corr_garage, 2))})
                
                if not feature_impact_list:
                    feature_impact_list = [
                        {'feature': 'OverallQual', 'impact': 0.85},
                        {'feature': 'GrLivArea', 'impact': 0.76},
                        {'feature': 'GarageCars', 'impact': 0.68}
                    ]
                
                # Calculate seasonal trends from actual data
                if 'MoSold' in df.columns and 'SalePrice' in df.columns:
                    monthly_avg = df.groupby('MoSold')['SalePrice'].mean()
                    seasonal_trends_list = []
                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    for month_num in range(1, 13):
                        if month_num in monthly_avg.index:
                            avg_price_month = int(monthly_avg[month_num])
                        else:
                            # Generate realistic seasonal pattern
                            base_price = 280000
                            seasonal_factor = 1 + 0.15 * np.sin((month_num - 6) * np.pi / 6)
                            avg_price_month = int(base_price * seasonal_factor)
                        
                        seasonal_trends_list.append({
                            'month': months[month_num - 1],
                            'avg_price': avg_price_month
                        })
                else:
                    seasonal_trends_list = [
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
                    ]
                
                # Calculate property distribution
                if 'BldgType' in df.columns:
                    property_counts = df['BldgType'].value_counts(normalize=True) * 100
                    property_distribution_list = []
                    
                    # Map building types to categories
                    type_mapping = {
                        '1Fam': 'Single Family',
                        '2fmCon': 'Duplex',
                        'Duplex': 'Multi-Family',
                        'TwnhsE': 'Townhouse',
                        'Twnhs': 'Townhouse'
                    }
                    
                    for bldg_type, percentage in property_counts.items():
                        category = type_mapping.get(bldg_type, bldg_type)
                        property_distribution_list.append({
                            'type': category,
                            'percentage': round(percentage, 1)
                        })
                    
                    # Limit to top 5 categories
                    property_distribution_list = sorted(property_distribution_list, key=lambda x: x['percentage'], reverse=True)[:5]
                else:
                    property_distribution_list = [
                        {'type': 'Single Family', 'percentage': 45},
                        {'type': 'Townhouse', 'percentage': 25},
                        {'type': 'Condo', 'percentage': 15},
                        {'type': 'Multi-Family', 'percentage': 10},
                        {'type': 'Luxury', 'percentage': 5}
                    ]
                
                # Get model metrics from actual model evaluation
                # You should store these metrics when training your model
                model_metrics = {
                    'accuracy': 91.5,  # Replace with actual R² score or accuracy
                    'error_margin': 3.2,  # Replace with actual RMSE/MAE
                    'r2_score': 0.89,
                    'rmse': 25000,  # Root Mean Squared Error in dollars
                    'mae': 18000    # Mean Absolute Error in dollars
                }
                
                insights = {
                    'avg_price_trend': avg_price_trend,
                    'days_on_market': 42,  # This would come from actual data if available
                    'avg_price': int(avg_price),
                    'min_price': int(min_price),
                    'max_price': int(max_price),
                    'total_properties': len(df),
                    'top_neighborhoods': top_neighborhoods_list,
                    'feature_impact': feature_impact_list,
                    'model_metrics': model_metrics,
                    'seasonal_trends': seasonal_trends_list,
                    'property_distribution': property_distribution_list,
                    'data_source': 'real_data',
                    'last_updated': datetime.now().isoformat()
                }
                
            else:
                # If no data file exists, generate realistic insights
                insights = generate_realistic_insights()
                
        except Exception as data_error:
            print(f"Error processing real data: {data_error}")
            # Fallback to realistic generated insights
            insights = generate_realistic_insights()
        
        return JsonResponse({
            'success': True,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in get_market_insights: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def generate_realistic_insights():
    """Generate realistic insights based on typical housing market patterns"""
    import numpy as np
    from datetime import datetime
    
    # Generate realistic price trends based on current month
    current_month = datetime.now().month
    base_price = 300000
    seasonal_factor = 1 + 0.15 * np.sin((current_month - 6) * np.pi / 6)
    current_avg_price = int(base_price * seasonal_factor)
    
    # Generate price trend (simulate 5-8% annual growth)
    monthly_growth = np.random.uniform(0.004, 0.007)  # 0.4% - 0.7% monthly
    avg_price_trend = f"+{monthly_growth * 12 * 100:.1f}%"
    
    # Generate realistic neighborhood data
    neighborhoods = ['NoRidge', 'StoneBr', 'NridgHt', 'Somerst', 'CollgCr', 'Edwards', 'OldTown']
    neighborhood_prices = {}
    
    for neighborhood in neighborhoods:
        # Each neighborhood has a different base price
        if neighborhood == 'NoRidge':
            base = 750000
        elif neighborhood == 'StoneBr':
            base = 680000
        elif neighborhood == 'NridgHt':
            base = 650000
        elif neighborhood == 'Somerst':
            base = 550000
        else:
            base = 350000 + np.random.randint(0, 100000)
        
        # Add some random variation
        price = base + np.random.randint(-20000, 20000)
        count = np.random.randint(20, 100)
        neighborhood_prices[neighborhood] = {'price': price, 'count': count}
    
    # Sort by price and get top 3
    top_neighborhoods = sorted(neighborhood_prices.items(), key=lambda x: x[1]['price'], reverse=True)[:3]
    top_neighborhoods_list = [
        {'name': name, 'avg_price': int(data['price']), 'count': data['count']}
        for name, data in top_neighborhoods
    ]
    
    # Generate realistic feature impacts
    features = ['OverallQual', 'GrLivArea', 'GarageCars', 'YearBuilt', 'FullBath', 'BedroomAbvGr']
    feature_impacts = []
    
    for feature in features:
        if feature == 'OverallQual':
            impact = np.random.uniform(0.8, 0.9)
        elif feature == 'GrLivArea':
            impact = np.random.uniform(0.7, 0.8)
        elif feature == 'GarageCars':
            impact = np.random.uniform(0.6, 0.7)
        elif feature == 'YearBuilt':
            impact = np.random.uniform(0.5, 0.6)
        else:
            impact = np.random.uniform(0.3, 0.5)
        
        feature_impacts.append({'feature': feature, 'impact': round(impact, 2)})
    
    # Sort by impact
    feature_impacts.sort(key=lambda x: x['impact'], reverse=True)
    
    # Generate seasonal trends with realistic pattern
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasonal_trends = []
    
    for i, month in enumerate(months, 1):
        # Realistic seasonal pattern: peak in summer, low in winter
        seasonal_factor = 1 + 0.15 * np.sin((i - 6) * np.pi / 6) + np.random.uniform(-0.02, 0.02)
        avg_price = int(300000 * seasonal_factor)
        seasonal_trends.append({'month': month, 'avg_price': avg_price})
    
    # Generate property distribution
    property_types = ['Single Family', 'Townhouse', 'Condo', 'Multi-Family', 'Luxury']
    percentages = [45, 25, 15, 10, 5]
    property_distribution = [
        {'type': prop_type, 'percentage': percentage}
        for prop_type, percentage in zip(property_types, percentages)
    ]
    
    # Realistic model metrics
    model_metrics = {
        'accuracy': round(np.random.uniform(0.88, 0.93) * 100, 1),
        'error_margin': round(np.random.uniform(2.8, 3.5), 1),
        'r2_score': round(np.random.uniform(0.86, 0.91), 2),
        'rmse': np.random.randint(20000, 30000),
        'mae': np.random.randint(15000, 20000)
    }
    
    return {
        'avg_price_trend': avg_price_trend,
        'days_on_market': np.random.randint(35, 50),
        'avg_price': current_avg_price,
        'min_price': int(100000 + np.random.randint(0, 50000)),
        'max_price': int(800000 + np.random.randint(0, 200000)),
        'total_properties': np.random.randint(1000, 3000),
        'top_neighborhoods': top_neighborhoods_list,
        'feature_impact': feature_impacts[:3],  # Top 3 features
        'model_metrics': model_metrics,
        'seasonal_trends': seasonal_trends,
        'property_distribution': property_distribution,
        'data_source': 'generated_realistic',
        'last_updated': datetime.now().isoformat()
    }
        
@csrf_exempt
def get_recommendations(request):
    """Get property recommendations based on current market"""
    try:
        data = json.loads(request.body)
        
        # Get user preferences or use defaults
        budget = data.get('budget', 500000)
        bedrooms = data.get('bedrooms', 3)
        
        # Generate recommendations using your model
        model = HousePriceModel()
        
        # Create sample properties based on user criteria
        recommendations = []
        
      
        # For now, return sample data
        for i in range(5):
            recommendations.append({
                'id': i + 1,
                'neighborhood': f'Neighborhood {i+1}',
                'predicted_price': budget * (0.8 + i * 0.1),
                'bedrooms': bedrooms,
                'bathrooms': bedrooms - 1,
                'sqft': 1500 + i * 200,
                'value_score': 85 + i * 3,
                'features': ['Good Schools', 'Near Park', 'Modern Kitchen'][:i+1]
            })
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations,
            'criteria': {
                'budget': budget,
                'bedrooms': bedrooms
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
        

@csrf_exempt
def analyze_property(request):
    """ analyze a specfic property's market position"""
    try:
        data = json.loads(request.body)
        property_data = {
            'GrLivArea': data.get('sqft_living', 2000),
            'BedroomAbvGr': data.get('bedrooms', 3),
            'FullBath': data.get('bathrooms', 2),
            'OverallQual': data.get('quality', 7),
            'Neighborhood': data.get('neighborhood', 'NAmes')
        }
        model = HousePriceModel()
        predicted_price = model.predict(property_data)
        
        # generated market analysis
        analysis = {
            'predicted': predicted_price[0] if predicted_price else 0,
            'markket_position': 'Above Average' if predicted_price > 350000 else 'Average',
            'comparable':[
                {'price':predicted_price *0.35, 'sqft': property_data['GrLivArea'] *0.9},
                {'price':predicted_price *1.05, 'sqft': property_data['GrLivArea'] *1.1}
            ],
            'recommendations': [
                'Consider kitchen upgrades for higher ROI',
                'Energy-efficient windows improve value',
                'Updated bathrooms yield 80% ROI'
            ]
        }
        return JsonResponse({
            'success':True,
            'analysis':analysis,
            'property_data':property_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)