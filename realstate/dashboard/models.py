
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json
from .ai_model import HousePriceModel

class PropertySubmission(models.Model):
    # Basic Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    
    # Property Details
    property_type = models.CharField(
        max_length=50,
        choices=[
            ('single_family', 'Single Family Home'),
            ('townhouse', 'Townhouse'),
            ('condo', 'Condo/Apartment'),
            ('multi_family', 'Multi-Family'),
            ('luxury', 'Luxury Home'),
            ('commercial', 'Commercial'),
            ('land', 'Land')
        ]
    )
    
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    
    # Property Specifications
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()  # Allows 1.5, 2.5 bathrooms
    living_area = models.IntegerField(help_text="Square feet")  # GrLivArea
    lot_area = models.IntegerField(help_text="Square feet")
    year_built = models.IntegerField()
    year_remodeled = models.IntegerField(null=True, blank=True)
    
    # Quality & Condition (1-10 scale)
    overall_quality = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    overall_condition = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    
    # Garage Information
    garage_cars = models.IntegerField(default=0)
    garage_area = models.IntegerField(default=0)
    
    # Basement
    basement_area = models.IntegerField(default=0)
    basement_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('none', 'No Basement')
        ],
        default='none'
    )
    
    # Exterior Features
    exterior_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('fair', 'Fair'),
            ('poor', 'Poor')
        ]
    )
    
    # Kitchen
    kitchen_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('fair', 'Fair'),
            ('poor', 'Poor')
        ]
    )
    
    # Additional Features
    has_pool = models.BooleanField(default=False)
    pool_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('none', 'No Pool')
        ],
        default='none'
    )
    
    has_fireplace = models.BooleanField(default=False)
    fireplace_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('none', 'No Fireplace')
        ],
        default='none'
    )
    
    # Sale Information (optional for predictions)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sale_date = models.DateField(null=True, blank=True)
    days_on_market = models.IntegerField(null=True, blank=True)
    
    # AI Prediction
    predicted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prediction_confidence = models.FloatField(null=True, blank=True)
    prediction_timestamp = models.DateTimeField(null=True, blank=True)
    
    # Additional Notes
    description = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True)  # List of additional features
    
    # Contact Information (for non-registered users)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Images
    image1 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    
    class Meta:
        ordering = ['-submission_date']
        verbose_name = 'Property Submission'
        verbose_name_plural = 'Property Submissions'
    
    def __str__(self):
        return f"{self.address}, {self.city} - ${self.predicted_price or 'No Prediction'}"
    
    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
    
    def get_property_features(self):
        """Extract features for AI model prediction"""
        features = {
            'BedroomAbvGr': self.bedrooms,
            'FullBath': int(self.bathrooms),
            'HalfBath': int((self.bathrooms - int(self.bathrooms)) * 2),
            'GrLivArea': self.living_area,
            'LotArea': self.lot_area,
            'OverallQual': self.overall_quality,
            'OverallCond': self.overall_condition,
            'YearBuilt': self.year_built,
            'YearRemodAdd': self.year_remodeled or self.year_built,
            'GarageCars': self.garage_cars,
            'GarageArea': self.garage_area,
            'TotalBsmtSF': self.basement_area,
            'Neighborhood': self.neighborhood,
            'MSSubClass': self.get_ms_subclass(),
            'MSZoning': self.get_ms_zoning(),
            'LotFrontage': self.estimate_lot_frontage(),
            'Street': 'Pave',  # Default assumption
            'Alley': 'NA',
            'LotShape': 'Reg',
            'LandContour': 'Lvl',
            'Utilities': 'AllPub',
            'LotConfig': 'Inside',
            'LandSlope': 'Gtl',
            'Condition1': 'Norm',
            'Condition2': 'Norm',
            'BldgType': self.get_bldg_type(),
            'HouseStyle': self.get_house_style(),
            'RoofStyle': 'Gable',
            'RoofMatl': 'CompShg',
            'Exterior1st': 'VinylSd',
            'Exterior2nd': 'VinylSd',
            'MasVnrType': 'None',
            'MasVnrArea': 0,
            'ExterQual': self.get_exter_qual_code(),
            'ExterCond': 'TA',
            'Foundation': 'PConc',
            'BsmtQual': self.get_bsmt_qual_code(),
            'BsmtCond': 'TA',
            'BsmtExposure': 'No',
            'BsmtFinType1': 'GLQ',
            'BsmtFinSF1': self.basement_area * 0.6 if self.basement_area > 0 else 0,
            'BsmtFinType2': 'Unf',
            'BsmtFinSF2': 0,
            'BsmtUnfSF': self.basement_area * 0.4 if self.basement_area > 0 else 0,
            'Heating': 'GasA',
            'HeatingQC': 'Ex',
            'CentralAir': 'Y',
            'Electrical': 'SBrkr',
            '1stFlrSF': self.living_area * 0.5,
            '2ndFlrSF': self.living_area * 0.5 if self.bedrooms > 3 else 0,
            'LowQualFinSF': 0,
            'BsmtFullBath': 0,
            'BsmtHalfBath': 0,
            'KitchenAbvGr': 1,
            'KitchenQual': self.get_kitchen_qual_code(),
            'TotRmsAbvGrd': self.bedrooms + 2,
            'Functional': 'Typ',
            'Fireplaces': 1 if self.has_fireplace else 0,
            'FireplaceQu': self.get_fireplace_qual_code(),
            'GarageType': 'Attchd',
            'GarageYrBlt': self.year_built,
            'GarageFinish': 'Fin',
            'GarageQual': 'TA',
            'GarageCond': 'TA',
            'PavedDrive': 'Y',
            'WoodDeckSF': 0,
            'OpenPorchSF': 100,
            'EnclosedPorch': 0,
            '3SsnPorch': 0,
            'ScreenPorch': 0,
            'PoolArea': 200 if self.has_pool else 0,
            'PoolQC': self.get_pool_qual_code(),
            'Fence': 'NA',
            'MiscFeature': 'NA',
            'MiscVal': 0,
            'MoSold': timezone.now().month,
            'YrSold': timezone.now().year,
            'SaleType': 'WD',
            'SaleCondition': 'Normal'
        }
        return features
    
    def get_ms_subclass(self):
        """Map property type to MSSubClass codes"""
        mapping = {
            'single_family': 20,
            'townhouse': 30,
            'condo': 50,
            'multi_family': 70,
            'luxury': 80,
            'commercial': 90,
            'land': 180
        }
        return mapping.get(self.property_type, 20)
    
    def get_ms_zoning(self):
        """Estimate zoning based on property type"""
        mapping = {
            'single_family': 'RL',
            'townhouse': 'RM',
            'condo': 'RM',
            'multi_family': 'RM',
            'luxury': 'RL',
            'commercial': 'C',
            'land': 'RL'
        }
        return mapping.get(self.property_type, 'RL')
    
    def get_bldg_type(self):
        """Map property type to BldgType codes"""
        mapping = {
            'single_family': '1Fam',
            'townhouse': 'TwnhsE',
            'condo': 'Twnhs',
            'multi_family': '2fmCon',
            'luxury': '1Fam',
            'commercial': '1Fam',
            'land': '1Fam'
        }
        return mapping.get(self.property_type, '1Fam')
    
    def get_house_style(self):
        """Estimate house style based on bedrooms"""
        if self.bedrooms <= 3:
            return '1Story'
        elif self.bedrooms <= 5:
            return '2Story'
        else:
            return 'SLvl'
    
    def get_exter_qual_code(self):
        """Convert quality to codes"""
        mapping = {
            'excellent': 'Ex',
            'good': 'Gd',
            'average': 'TA',
            'fair': 'Fa',
            'poor': 'Po'
        }
        return mapping.get(self.exterior_quality, 'TA')
    
    def get_bsmt_qual_code(self):
        """Convert basement quality to codes"""
        mapping = {
            'excellent': 'Ex',
            'good': 'Gd',
            'average': 'TA',
            'fair': 'Fa',
            'poor': 'Po',
            'none': 'NA'
        }
        return mapping.get(self.basement_quality, 'NA')
    
    def get_kitchen_qual_code(self):
        """Convert kitchen quality to codes"""
        mapping = {
            'excellent': 'Ex',
            'good': 'Gd',
            'average': 'TA',
            'fair': 'Fa',
            'poor': 'Po'
        }
        return mapping.get(self.kitchen_quality, 'TA')
    
    def get_fireplace_qual_code(self):
        """Convert fireplace quality to codes"""
        if not self.has_fireplace:
            return 'NA'
        mapping = {
            'excellent': 'Ex',
            'good': 'Gd',
            'average': 'TA',
            'fair': 'Fa',
            'poor': 'Po',
            'none': 'NA'
        }
        return mapping.get(self.fireplace_quality, 'TA')
    
    def get_pool_qual_code(self):
        """Convert pool quality to codes"""
        if not self.has_pool:
            return 'NA'
        mapping = {
            'excellent': 'Ex',
            'good': 'Gd',
            'average': 'TA',
            'fair': 'Fa',
            'poor': 'Po',
            'none': 'NA'
        }
        return mapping.get(self.pool_quality, 'TA')
    
    def estimate_lot_frontage(self):
        """Estimate lot frontage based on lot area"""
        # Simple estimation: assume square lot
        import math
        if self.lot_area > 0:
            return int(math.sqrt(self.lot_area))
        return 80  # Default
    
    def predict_price(self):
        """Generate price prediction using AI model"""
        try:
            model = HousePriceModel()
            features = self.get_property_features()
            prediction = model.predict(features)
            
            if prediction and len(prediction) > 0:
                self.predicted_price = prediction[0]
                self.prediction_confidence = 90.0  # This would come from model confidence
                self.prediction_timestamp = timezone.now()
                self.save()
                return self.predicted_price
        except Exception as e:
            print(f"Prediction error: {e}")
            return None


class MarketInsight(models.Model):
    """Store calculated market insights"""
    date = models.DateField(auto_now_add=True)
    insights = models.JSONField()
    
    # Summary metrics
    avg_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_price = models.DecimalField(max_digits=12, decimal_places=2)
    max_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_properties = models.IntegerField()
    avg_days_on_market = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Market Insights - {self.date}"


class UserSubmissionAnalytics(models.Model):
    """Track analytics about user submissions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
    # Submission counts
    total_submissions = models.IntegerField(default=0)
    verified_submissions = models.IntegerField(default=0)
    pending_submissions = models.IntegerField(default=0)
    
    # Prediction accuracy (if actual prices are provided)
    avg_prediction_error = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics - {self.user or 'Anonymous'} - {self.date}"