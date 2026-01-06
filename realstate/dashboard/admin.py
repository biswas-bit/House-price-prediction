from django.contrib import admin
from django.utils.html import format_html
from .models import PropertySubmission, MarketInsight, UserSubmissionAnalytics
import json

@admin.register(PropertySubmission)
class PropertySubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'address', 'city', 'property_type_display', 
        'bedrooms', 'bathrooms', 'predicted_price_display',
        'verification_status_display', 'submission_date'
    ]
    list_filter = [
        'verification_status', 'property_type', 'city',
        'submission_date', 'is_verified'
    ]
    search_fields = ['address', 'city', 'neighborhood', 'contact_email', 'contact_name']
    readonly_fields = ['submission_date', 'prediction_timestamp']
    fieldsets = (
        ('Contact Information', {
            'fields': ('user', 'contact_name', 'contact_email', 'contact_phone')
        }),
        ('Property Details', {
            'fields': (
                'property_type', 'address', 'city', 'state', 'zip_code', 'neighborhood',
                'bedrooms', 'bathrooms', 'living_area', 'lot_area',
                'year_built', 'year_remodeled'
            )
        }),
        ('Quality & Features', {
            'fields': (
                'overall_quality', 'overall_condition',
                'exterior_quality', 'kitchen_quality',
                'garage_cars', 'garage_area',
                'basement_area', 'basement_quality',
                'has_pool', 'pool_quality',
                'has_fireplace', 'fireplace_quality'
            )
        }),
        ('Sale Information', {
            'fields': ('sale_price', 'sale_date', 'days_on_market', 'description')
        }),
        ('AI Prediction', {
            'fields': (
                'predicted_price', 'prediction_confidence', 
                'prediction_timestamp', 'verification_status', 'is_verified'
            )
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3'),
            'classes': ('collapse',)
        }),
    )
    actions = ['verify_selected', 'mark_as_pending', 'regenerate_predictions']
    
    def property_type_display(self, obj):
        return dict(PropertySubmission._meta.get_field('property_type').choices).get(
            obj.property_type, obj.property_type
        )
    property_type_display.short_description = 'Property Type'
    
    def predicted_price_display(self, obj):
        if obj.predicted_price:
            return f"${obj.predicted_price:,.0f}"
        return "No Prediction"
    predicted_price_display.short_description = 'Predicted Price'
    
    def verification_status_display(self, obj):
        colors = {
            'verified': 'green',
            'pending': 'orange',
            'rejected': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.verification_status, 'black'),
            obj.get_verification_status_display()
        )
    verification_status_display.short_description = 'Status'
    
    def verify_selected(self, request, queryset):
        queryset.update(verification_status='verified', is_verified=True)
        self.message_user(request, f"{queryset.count()} properties verified.")
    verify_selected.short_description = "Mark selected as verified"
    
    def mark_as_pending(self, request, queryset):
        queryset.update(verification_status='pending', is_verified=False)
        self.message_user(request, f"{queryset.count()} properties marked as pending.")
    mark_as_pending.short_description = "Mark selected as pending"
    
    def regenerate_predictions(self, request, queryset):
        count = 0
        for obj in queryset:
            if obj.predict_price():
                count += 1
        self.message_user(request, f"Predictions regenerated for {count} properties.")
    regenerate_predictions.short_description = "Regenerate predictions"


@admin.register(MarketInsight)
class MarketInsightAdmin(admin.ModelAdmin):
    list_display = ['date', 'avg_price_display', 'total_properties']
    readonly_fields = ['date', 'insights_preview']
    date_hierarchy = 'date'
    
    def avg_price_display(self, obj):
        return f"${obj.avg_price:,.0f}"
    avg_price_display.short_description = 'Average Price'
    
    def insights_preview(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.insights, indent=2))
    insights_preview.short_description = 'Insights Data'


@admin.register(UserSubmissionAnalytics)
class UserSubmissionAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total_submissions', 'verified_submissions']
    list_filter = ['date', 'user']
    date_hierarchy = 'date'