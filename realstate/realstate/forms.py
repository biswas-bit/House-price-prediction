from django import forms

class HouseForm(forms.Form):
    # MSSubClass: Identifies the type of dwelling involved in the sale
    MSSubClass = forms.IntegerField(
        label='MS SubClass',
        min_value=20,
        max_value=190,
        help_text='Identifies the type of dwelling involved in the sale. Example: 20 = 1-STORY 1946 & NEWER ALL STYLES'
    )
    
    # MSZoning: Identifies the general zoning classification of the sale
    MSZONING_CHOICES = [
        ('A', 'Agriculture'),
        ('C', 'Commercial'),
        ('FV', 'Floating Village Residential'),
        ('I', 'Industrial'),
        ('RH', 'Residential High Density'),
        ('RL', 'Residential Low Density'),
        ('RP', 'Residential Low Density Park'),
        ('RM', 'Residential Medium Density'),
    ]
    MSZoning = forms.ChoiceField(
        label='MS Zoning',
        choices=MSZONING_CHOICES,
        help_text='General zoning classification'
    )
    
    LotFrontage = forms.IntegerField(
        label='Lot Frontage (feet)',
        min_value=0,
        max_value=500,
        help_text='Linear feet of street connected to property'
    )
    
    LotArea = forms.IntegerField(
        label='Lot Area (sqft)',
        min_value=1000,
        max_value=50000,
        help_text='Lot size in square feet'
    )
    
    STREET_CHOICES = [
        ('Grvl', 'Gravel'),
        ('Pave', 'Paved'),
    ]
    Street = forms.ChoiceField(
        label='Street Type',
        choices=STREET_CHOICES
    )
    
    ALLEY_CHOICES = [
        ('Grvl', 'Gravel'),
        ('Pave', 'Paved'),
        ('NA', 'No alley access'),
    ]
    Alley = forms.ChoiceField(
        label='Alley Access',
        choices=ALLEY_CHOICES,
        required=False,
        help_text='Type of alley access to property'
    )
    
    LOTSHAPE_CHOICES = [
        ('Reg', 'Regular'),
        ('IR1', 'Slightly irregular'),
        ('IR2', 'Moderately irregular'),
        ('IR3', 'Irregular'),
    ]
    LotShape = forms.ChoiceField(
        label='Lot Shape',
        choices=LOTSHAPE_CHOICES
    )
    
    LANDCONTOUR_CHOICES = [
        ('Lvl', 'Near Flat/Level'),
        ('Bnk', 'Banked - Quick and significant rise from street grade to building'),
        ('HLS', 'Hillside - Significant slope from side to side'),
        ('Low', 'Depression'),
    ]
    LandContour = forms.ChoiceField(
        label='Land Contour',
        choices=LANDCONTOUR_CHOICES
    )
    
    UTILITIES_CHOICES = [
        ('AllPub', 'All public Utilities (E,G,W,& S)'),
        ('NoSewr', 'Electricity, Gas, and Water (Septic Tank)'),
        ('NoSeWa', 'Electricity and Gas Only'),
        ('ELO', 'Electricity only'),
    ]
    Utilities = forms.ChoiceField(
        label='Utilities',
        choices=UTILITIES_CHOICES
    )
    
    LOTCONFIG_CHOICES = [
        ('Inside', 'Inside lot'),
        ('Corner', 'Corner lot'),
        ('CulDSac', 'Cul-de-sac'),
        ('FR2', 'Frontage on 2 sides of property'),
        ('FR3', 'Frontage on 3 sides of property'),
    ]
    LotConfig = forms.ChoiceField(
        label='Lot Configuration',
        choices=LOTCONFIG_CHOICES
    )
    
    LandSlope = forms.ChoiceField(
        label='Land Slope',
        choices=[
            ('Gtl', 'Gentle slope'),
            ('Mod', 'Moderate slope'),
            ('Sev', 'Severe slope'),
        ]
    )
    
    NEIGHBORHOOD_CHOICES = [
        ('Blmngtn', 'Bloomington Heights'),
        ('Blueste', 'Bluestem'),
        ('BrDale', 'Briardale'),
        ('BrkSide', 'Brookside'),
        ('ClearCr', 'Clear Creek'),
        ('CollgCr', 'College Creek'),
        ('Crawfor', 'Crawford'),
        ('Edwards', 'Edwards'),
        ('Gilbert', 'Gilbert'),
        ('IDOTRR', 'Iowa DOT and Rail Road'),
        ('MeadowV', 'Meadow Village'),
        ('Mitchel', 'Mitchell'),
        ('NAmes', 'North Ames'),
        ('NoRidge', 'Northridge'),
        ('NPkVill', 'Northpark Villa'),
        ('NridgHt', 'Northridge Heights'),
        ('NWAmes', 'Northwest Ames'),
        ('OldTown', 'Old Town'),
        ('SWISU', 'South & West of Iowa State University'),
        ('Sawyer', 'Sawyer'),
        ('SawyerW', 'Sawyer West'),
        ('Somerst', 'Somerset'),
        ('StoneBr', 'Stone Brook'),
        ('Timber', 'Timberland'),
        ('Veenker', 'Veenker'),
    ]
    Neighborhood = forms.ChoiceField(
        label='Neighborhood',
        choices=NEIGHBORHOOD_CHOICES
    )
    
    CONDITION_CHOICES = [
        ('Artery', 'Adjacent to arterial street'),
        ('Feedr', 'Adjacent to feeder street'),
        ('Norm', 'Normal'),
        ('RRNn', 'Within 200\' of North-South Railroad'),
        ('RRAn', 'Adjacent to North-South Railroad'),
        ('PosN', 'Near positive off-site feature--park, greenbelt, etc.'),
        ('PosA', 'Adjacent to postive off-site feature'),
        ('RRNe', 'Within 200\' of East-West Railroad'),
        ('RRAe', 'Adjacent to East-West Railroad'),
    ]
    Condition1 = forms.ChoiceField(
        label='Condition 1',
        choices=CONDITION_CHOICES
    )
    
    Condition2 = forms.ChoiceField(
        label='Condition 2',
        choices=CONDITION_CHOICES,
        required=False,
        help_text='Second condition if present'
    )
    
    BLDGTYPE_CHOICES = [
        ('1Fam', 'Single-family Detached'),
        ('2FmCon', 'Two-family Conversion; originally built as one-family dwelling'),
        ('Duplx', 'Duplex'),
        ('TwnhsE', 'Townhouse End Unit'),
        ('TwnhsI', 'Townhouse Inside Unit'),
    ]
    BldgType = forms.ChoiceField(
        label='Building Type',
        choices=BLDGTYPE_CHOICES
    )
    
    HOUSESTYLE_CHOICES = [
        ('1Story', 'One story'),
        ('1.5Fin', 'One and one-half story: 2nd level finished'),
        ('1.5Unf', 'One and one-half story: 2nd level unfinished'),
        ('2Story', 'Two story'),
        ('2.5Fin', 'Two and one-half story: 2nd level finished'),
        ('2.5Unf', 'Two and one-half story: 2nd level unfinished'),
        ('SFoyer', 'Split Foyer'),
        ('SLvl', 'Split Level'),
    ]
    HouseStyle = forms.ChoiceField(
        label='House Style',
        choices=HOUSESTYLE_CHOICES
    )
    
    OverallQual = forms.IntegerField(
        label='Overall Quality',
        min_value=1,
        max_value=10,
        help_text='Rates the overall material and finish of the house (1-10)'
    )
    
    OverallCond = forms.IntegerField(
        label='Overall Condition',
        min_value=1,
        max_value=10,
        help_text='Rates the overall condition of the house (1-10)'
    )
    
    YearBuilt = forms.IntegerField(
        label='Year Built',
        min_value=1800,
        max_value=2024,
        help_text='Original construction date'
    )
    
    YearRemodAdd = forms.IntegerField(
        label='Remodel/Addition Year',
        min_value=1800,
        max_value=2024,
        help_text='Remodel date (same as construction date if no remodeling or additions)'
    )
    
    ROOFSTYLE_CHOICES = [
        ('Flat', 'Flat'),
        ('Gable', 'Gable'),
        ('Gambrel', 'Gabrel (Barn)'),
        ('Hip', 'Hip'),
        ('Mansard', 'Mansard'),
        ('Shed', 'Shed'),
    ]
    RoofStyle = forms.ChoiceField(
        label='Roof Style',
        choices=ROOFSTYLE_CHOICES
    )
    
    ROOFMATL_CHOICES = [
        ('ClyTile', 'Clay or Tile'),
        ('CompShg', 'Standard (Composite) Shingle'),
        ('Membran', 'Membrane'),
        ('Metal', 'Metal'),
        ('Roll', 'Roll'),
        ('Tar&Grv', 'Gravel & Tar'),
        ('WdShake', 'Wood Shakes'),
        ('WdShngl', 'Wood Shingles'),
    ]
    RoofMatl = forms.ChoiceField(
        label='Roof Material',
        choices=ROOFMATL_CHOICES
    )
    
    EXTERIOR_CHOICES = [
        ('AsbShng', 'Asbestos Shingles'),
        ('AsphShn', 'Asphalt Shingles'),
        ('BrkComm', 'Brick Common'),
        ('BrkFace', 'Brick Face'),
        ('CBlock', 'Cinder Block'),
        ('CemntBd', 'Cement Board'),
        ('HdBoard', 'Hard Board'),
        ('ImStucc', 'Imitation Stucco'),
        ('MetalSd', 'Metal Siding'),
        ('Other', 'Other'),
        ('Plywood', 'Plywood'),
        ('PreCast', 'PreCast'),
        ('Stone', 'Stone'),
        ('Stucco', 'Stucco'),
        ('VinylSd', 'Vinyl Siding'),
        ('Wd Sdng', 'Wood Siding'),
        ('WdShing', 'Wood Shingles'),
    ]
    Exterior1st = forms.ChoiceField(
        label='Primary Exterior Covering',
        choices=EXTERIOR_CHOICES
    )
    
    Exterior2nd = forms.ChoiceField(
        label='Secondary Exterior Covering',
        choices=EXTERIOR_CHOICES,
        help_text='Secondary exterior covering (if different)'
    )
    
    MASVNRTYPE_CHOICES = [
        ('BrkCmn', 'Brick Common'),
        ('BrkFace', 'Brick Face'),
        ('CBlock', 'Cinder Block'),
        ('None', 'None'),
        ('Stone', 'Stone'),
    ]
    MasVnrType = forms.ChoiceField(
        label='Masonry Veneer Type',
        choices=MASVNRTYPE_CHOICES,
        required=False
    )
    
    MasVnrArea = forms.IntegerField(
        label='Masonry Veneer Area (sqft)',
        min_value=0,
        max_value=5000,
        required=False,
        help_text='Masonry veneer area in square feet'
    )
    
    EXTERQUAL_CHOICES = [
        ('Ex', 'Excellent'),
        ('Gd', 'Good'),
        ('TA', 'Average/Typical'),
        ('Fa', 'Fair'),
        ('Po', 'Poor'),
    ]
    ExterQual = forms.ChoiceField(
        label='Exterior Quality',
        choices=EXTERQUAL_CHOICES
    )
    
    ExterCond = forms.ChoiceField(
        label='Exterior Condition',
        choices=EXTERQUAL_CHOICES,
        help_text='Present condition of the material on the exterior'
    )
    
    FOUNDATION_CHOICES = [
        ('BrkTil', 'Brick & Tile'),
        ('CBlock', 'Cinder Block'),
        ('PConc', 'Poured Contrete'),
        ('Slab', 'Slab'),
        ('Stone', 'Stone'),
        ('Wood', 'Wood'),
    ]
    Foundation = forms.ChoiceField(
        label='Foundation Type',
        choices=FOUNDATION_CHOICES
    )
    
    BSMTQUAL_CHOICES = [
        ('Ex', 'Excellent (100+ inches)'),
        ('Gd', 'Good (90-99 inches)'),
        ('TA', 'Typical (80-89 inches)'),
        ('Fa', 'Fair (70-79 inches)'),
        ('Po', 'Poor (<70 inches)'),
        ('NA', 'No Basement'),
    ]
    BsmtQual = forms.ChoiceField(
        label='Basement Quality',
        choices=BSMTQUAL_CHOICES
    )
    
    BsmtCond = forms.ChoiceField(
        label='Basement Condition',
        choices=BSMTQUAL_CHOICES,
        help_text='General condition of the basement'
    )
    
    BSMTEXPOSURE_CHOICES = [
        ('Gd', 'Good Exposure'),
        ('Av', 'Average Exposure (split levels or foyers typically score average or above)'),
        ('Mn', 'Mimimum Exposure'),
        ('No', 'No Exposure'),
        ('NA', 'No Basement'),
    ]
    BsmtExposure = forms.ChoiceField(
        label='Basement Exposure',
        choices=BSMTEXPOSURE_CHOICES
    )
    
    BSMTFINTYPE_CHOICES = [
        ('GLQ', 'Good Living Quarters'),
        ('ALQ', 'Average Living Quarters'),
        ('BLQ', 'Below Average Living Quarters'),
        ('Rec', 'Average Rec Room'),
        ('LwQ', 'Low Quality'),
        ('Unf', 'Unfinshed'),
        ('NA', 'No Basement'),
    ]
    BsmtFinType1 = forms.ChoiceField(
        label='Basement Finished Area 1 Type',
        choices=BSMTFINTYPE_CHOICES
    )
    
    BsmtFinSF1 = forms.IntegerField(
        label='Basement Finished Area 1 (sqft)',
        min_value=0,
        max_value=5000,
        help_text='Type 1 finished square feet'
    )
    
    BsmtFinType2 = forms.ChoiceField(
        label='Basement Finished Area 2 Type',
        choices=BSMTFINTYPE_CHOICES,
        help_text='Rating of basement finished area (if multiple types)'
    )
    
    BsmtFinSF2 = forms.IntegerField(
        label='Basement Finished Area 2 (sqft)',
        min_value=0,
        max_value=5000,
        help_text='Type 2 finished square feet'
    )
    
    BsmtUnfSF = forms.IntegerField(
        label='Basement Unfinished Area (sqft)',
        min_value=0,
        max_value=5000,
        help_text='Unfinished square feet of basement area'
    )
    
    TotalBsmtSF = forms.IntegerField(
        label='Total Basement Area (sqft)',
        min_value=0,
        max_value=5000,
        help_text='Total square feet of basement area'
    )
    
    HEATING_CHOICES = [
        ('Floor', 'Floor Furnace'),
        ('GasA', 'Gas forced warm air furnace'),
        ('GasW', 'Gas hot water or steam heat'),
        ('Grav', 'Gravity furnace'),
        ('OthW', 'Hot water or steam heat other than gas'),
        ('Wall', 'Wall furnace'),
    ]
    Heating = forms.ChoiceField(
        label='Heating Type',
        choices=HEATING_CHOICES
    )
    
    HeatingQC = forms.ChoiceField(
        label='Heating Quality & Condition',
        choices=EXTERQUAL_CHOICES
    )
    
    CentralAir = forms.ChoiceField(
        label='Central Air Conditioning',
        choices=[('Y', 'Yes'), ('N', 'No')]
    )
    
    ELECTRICAL_CHOICES = [
        ('SBrkr', 'Standard Circuit Breakers & Romex'),
        ('FuseA', 'Fuse Box over 60 AMP and all Romex wiring (Average)'),
        ('FuseF', '60 AMP Fuse Box and mostly Romex wiring (Fair)'),
        ('FuseP', '60 AMP Fuse Box and mostly knob & tube wiring (Poor)'),
        ('Mix', 'Mixed'),
    ]
    Electrical = forms.ChoiceField(
        label='Electrical System',
        choices=ELECTRICAL_CHOICES
    )
    
    FirstFlrSF = forms.IntegerField(
        label='First Floor Square Feet',
        min_value=0,
        max_value=5000,
        help_text='First Floor square feet'
    )
    
    SecondFlrSF = forms.IntegerField(
        label='Second Floor Square Feet',
        min_value=0,
        max_value=5000,
        help_text='Second floor square feet'
    )
    
    LowQualFinSF = forms.IntegerField(
        label='Low Quality Finished Square Feet',
        min_value=0,
        max_value=5000,
        required=False,
        help_text='Low quality finished square feet (all floors)'
    )
    
    GrLivArea = forms.IntegerField(
        label='Above Grade Living Area (sqft)',
        min_value=0,
        max_value=5000,
        help_text='Above grade (ground) living area square feet'
    )
    
    BsmtFullBath = forms.IntegerField(
        label='Basement Full Bathrooms',
        min_value=0,
        max_value=5,
        help_text='Basement full bathrooms'
    )
    
    BsmtHalfBath = forms.IntegerField(
        label='Basement Half Bathrooms',
        min_value=0,
        max_value=5,
        help_text='Basement half bathrooms'
    )
    
    FullBath = forms.IntegerField(
        label='Full Bathrooms Above Grade',
        min_value=0,
        max_value=5,
        help_text='Full bathrooms above grade'
    )
    
    HalfBath = forms.IntegerField(
        label='Half Bathrooms Above Grade',
        min_value=0,
        max_value=5,
        help_text='Half baths above grade'
    )
    
    BedroomAbvGr = forms.IntegerField(
        label='Bedrooms Above Grade',
        min_value=0,
        max_value=10,
        help_text='Number of bedrooms above basement level'
    )
    
    KitchenAbvGr = forms.IntegerField(
        label='Kitchens Above Grade',
        min_value=0,
        max_value=5,
        help_text='Number of kitchens above grade'
    )
    
    KitchenQual = forms.ChoiceField(
        label='Kitchen Quality',
        choices=EXTERQUAL_CHOICES
    )
    
    TotRmsAbvGrd = forms.IntegerField(
        label='Total Rooms Above Grade',
        min_value=0,
        max_value=20,
        help_text='Total rooms above grade (does not include bathrooms)'
    )
    
    FUNCTIONAL_CHOICES = [
        ('Typ', 'Typical Functionality'),
        ('Min1', 'Minor Deductions 1'),
        ('Min2', 'Minor Deductions 2'),
        ('Mod', 'Moderate Deductions'),
        ('Maj1', 'Major Deductions 1'),
        ('Maj2', 'Major Deductions 2'),
        ('Sev', 'Severely Damaged'),
        ('Sal', 'Salvage only'),
    ]
    Functional = forms.ChoiceField(
        label='Home Functionality',
        choices=FUNCTIONAL_CHOICES
    )
    
    Fireplaces = forms.IntegerField(
        label='Number of Fireplaces',
        min_value=0,
        max_value=5,
        help_text='Number of fireplaces'
    )
    
    FIREPLACEQU_CHOICES = [
        ('Ex', 'Excellent - Exceptional Masonry Fireplace'),
        ('Gd', 'Good - Masonry Fireplace in main level'),
        ('TA', 'Average - Prefabricated Fireplace in main living area or Masonry Fireplace in basement'),
        ('Fa', 'Fair - Prefabricated Fireplace in basement'),
        ('Po', 'Poor - Ben Franklin Stove'),
        ('NA', 'No Fireplace'),
    ]
    FireplaceQu = forms.ChoiceField(
        label='Fireplace Quality',
        choices=FIREPLACEQU_CHOICES,
        required=False
    )
    
    GARAGETYPE_CHOICES = [
        ('2Types', 'More than one type'),
        ('Attchd', 'Attached to home'),
        ('Basment', 'Basement Garage'),
        ('BuiltIn', 'Built-In (Garage part of house - typically has room above garage)'),
        ('CarPort', 'Car Port'),
        ('Detchd', 'Detached from home'),
        ('NA', 'No Garage'),
    ]
    GarageType = forms.ChoiceField(
        label='Garage Type',
        choices=GARAGETYPE_CHOICES,
        required=False
    )
    
    GarageYrBlt = forms.IntegerField(
        label='Garage Year Built',
        min_value=1800,
        max_value=2024,
        required=False,
        help_text='Year garage was built'
    )
    
    GARAGEFINISH_CHOICES = [
        ('Fin', 'Finished'),
        ('RFn', 'Rough Finished'),
        ('Unf', 'Unfinished'),
        ('NA', 'No Garage'),
    ]
    GarageFinish = forms.ChoiceField(
        label='Garage Finish',
        choices=GARAGEFINISH_CHOICES,
        required=False
    )
    
    GarageCars = forms.IntegerField(
        label='Garage Car Capacity',
        min_value=0,
        max_value=10,
        required=False,
        help_text='Size of garage in car capacity'
    )
    
    GarageArea = forms.IntegerField(
        label='Garage Area (sqft)',
        min_value=0,
        max_value=2000,
        required=False,
        help_text='Size of garage in square feet'
    )
    
    GarageQual = forms.ChoiceField(
        label='Garage Quality',
        choices=EXTERQUAL_CHOICES,
        required=False
    )
    
    GarageCond = forms.ChoiceField(
        label='Garage Condition',
        choices=EXTERQUAL_CHOICES,
        required=False
    )
    
    PAVEDDRIVE_CHOICES = [
        ('Y', 'Paved'),
        ('P', 'Partial Pavement'),
        ('N', 'Dirt/Gravel'),
    ]
    PavedDrive = forms.ChoiceField(
        label='Paved Driveway',
        choices=PAVEDDRIVE_CHOICES
    )
    
    WoodDeckSF = forms.IntegerField(
        label='Wood Deck Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Wood deck area in square feet'
    )
    
    OpenPorchSF = forms.IntegerField(
        label='Open Porch Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Open porch area in square feet'
    )
    
    EnclosedPorch = forms.IntegerField(
        label='Enclosed Porch Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Enclosed porch area in square feet'
    )
    
    ThreeSsnPorch = forms.IntegerField(
        label='Three Season Porch Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Three season porch area in square feet'
    )
    
    ScreenPorch = forms.IntegerField(
        label='Screen Porch Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Screen porch area in square feet'
    )
    
    PoolArea = forms.IntegerField(
        label='Pool Area (sqft)',
        min_value=0,
        max_value=1000,
        required=False,
        help_text='Pool area in square feet'
    )
    
    POOLQC_CHOICES = [
        ('Ex', 'Excellent'),
        ('Gd', 'Good'),
        ('TA', 'Average/Typical'),
        ('Fa', 'Fair'),
        ('NA', 'No Pool'),
    ]
    PoolQC = forms.ChoiceField(
        label='Pool Quality',
        choices=POOLQC_CHOICES,
        required=False
    )
    
    FENCE_CHOICES = [
        ('GdPrv', 'Good Privacy'),
        ('MnPrv', 'Minimum Privacy'),
        ('GdWo', 'Good Wood'),
        ('MnWw', 'Minimum Wood/Wire'),
        ('NA', 'No Fence'),
    ]
    Fence = forms.ChoiceField(
        label='Fence Quality',
        choices=FENCE_CHOICES,
        required=False
    )
    
    MISC_FEATURE_CHOICES = [
        ('Elev', 'Elevator'),
        ('Gar2', '2nd Garage (if not described in garage section)'),
        ('Othr', 'Other'),
        ('Shed', 'Shed (over 100 SF)'),
        ('TenC', 'Tennis Court'),
        ('NA', 'None'),
    ]
    MiscFeature = forms.ChoiceField(
        label='Miscellaneous Feature',
        choices=MISC_FEATURE_CHOICES,
        required=False
    )
    
    MiscVal = forms.IntegerField(
        label='Miscellaneous Feature Value ($)',
        min_value=0,
        max_value=100000,
        required=False,
        help_text='Value of miscellaneous feature'
    )
    
    MoSold = forms.IntegerField(
        label='Month Sold',
        min_value=1,
        max_value=12,
        help_text='Month sold (1-12)'
    )
    
    YrSold = forms.IntegerField(
        label='Year Sold',
        min_value=2000,
        max_value=2024,
        help_text='Year sold'
    )
    
    SALETYPE_CHOICES = [
        ('WD', 'Warranty Deed - Conventional'),
        ('CWD', 'Warranty Deed - Cash'),
        ('VWD', 'Warranty Deed - VA Loan'),
        ('New', 'Home just constructed and sold'),
        ('COD', 'Court Officer Deed/Estate'),
        ('Con', 'Contract 15% Down payment regular terms'),
        ('ConLw', 'Contract Low Down payment and low interest'),
        ('ConLI', 'Contract Low Interest'),
        ('ConLD', 'Contract Low Down'),
        ('Oth', 'Other'),
    ]
    SaleType = forms.ChoiceField(
        label='Sale Type',
        choices=SALETYPE_CHOICES
    )
    
    SALECONDITION_CHOICES = [
        ('Normal', 'Normal Sale'),
        ('Abnorml', 'Abnormal Sale - trade, foreclosure, short sale'),
        ('AdjLand', 'Adjoining Land Purchase'),
        ('Alloca', 'Allocation - two linked properties with separate deeds, typically condo with a garage unit'),
        ('Family', 'Sale between family members'),
        ('Partial', 'Home was not completed when last assessed (associated with New Homes)'),
    ]
    SaleCondition = forms.ChoiceField(
        label='Sale Condition',
        choices=SALECONDITION_CHOICES
    )
    
    # Add custom clean method for validation
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate YearRemodAdd >= YearBuilt
        year_built = cleaned_data.get('YearBuilt')
        year_remod = cleaned_data.get('YearRemodAdd')
        if year_built and year_remod and year_remod < year_built:
            raise forms.ValidationError("Remodel year cannot be earlier than construction year.")
        
        # Validate TotalBsmtSF >= sum of BsmtFinSF1, BsmtFinSF2, and BsmtUnfSF
        total_bsmt = cleaned_data.get('TotalBsmtSF', 0)
        bsmt_fin1 = cleaned_data.get('BsmtFinSF1', 0)
        bsmt_fin2 = cleaned_data.get('BsmtFinSF2', 0)
        bsmt_unf = cleaned_data.get('BsmtUnfSF', 0)
        
        if total_bsmt < (bsmt_fin1 + bsmt_fin2 + bsmt_unf):
            raise forms.ValidationError(
                "Total basement area should be greater than or equal to the sum of finished and unfinished areas."
            )
        
        # Validate GrLivArea consistency
        first_flr = cleaned_data.get('FirstFlrSF', 0)
        second_flr = cleaned_data.get('SecondFlrSF', 0)
        low_qual = cleaned_data.get('LowQualFinSF', 0)
        
        if (first_flr + second_flr + low_qual) != cleaned_data.get('GrLivArea', 0):
            raise forms.ValidationError(
                "Above grade living area should equal the sum of first floor, second floor, and low quality finished areas."
            )
        
        return cleaned_data
    
    # Optional: Add widget customization for better UI
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label.lower()}'
            })
        
        # Special handling for specific fields
        self.fields['YearBuilt'].widget.attrs.update({'min': '1800', 'max': '2024'})
        self.fields['YearRemodAdd'].widget.attrs.update({'min': '1800', 'max': '2024'})
        self.fields['OverallQual'].widget.attrs.update({'min': '1', 'max': '10'})
        self.fields['OverallCond'].widget.attrs.update({'min': '1', 'max': '10'})