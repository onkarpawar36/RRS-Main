from django import forms
from .models import Room, RoomImage, RoomReview, RoomReport


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'title', 'description', 'category', 'room_type', 'price', 'security_deposit',
            'address', 'city', 'state', 'pincode',
            'area_sqft', 'bedrooms', 'bathrooms', 'max_occupancy', 'floor', 'available_from',
            'wifi', 'parking', 'ac', 'laundry', 'kitchen', 'food_included', 'gym', 'swimming_pool', 'security'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room title (e.g., Cozy 2BHK near Metro Station)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your room in detail...',
                'rows': 5
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly rent in ₹'
            }),
            'security_deposit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Security deposit amount in ₹'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Full address with landmarks...',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State name'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN Code'
            }),
            'area_sqft': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area in sq ft'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'max_occupancy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'floor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ground Floor, 1st Floor, 2nd Floor'
            }),
            'available_from': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select availability date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom styling for checkboxes
        amenity_fields = ['wifi', 'parking', 'ac', 'laundry', 'kitchen', 'food_included', 'gym', 'swimming_pool', 'security']
        for field in amenity_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-check-input',
                'id': f'id_{field}'
            })


class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ['image', 'caption', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image caption (optional)'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field not required for editing
        self.fields['image'].required = False
        self.fields['caption'].required = False
        self.fields['is_main'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        # If no image is provided, this form should be considered empty
        if not cleaned_data.get('image') and not self.instance.pk:
            # Clear all data for empty forms
            return {}
        return cleaned_data


class RoomImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        # Skip default clean to avoid validation errors on empty forms
        # Images are completely optional for both create and edit
        pass
    
    def full_clean(self):
        """Override full_clean to handle empty forms gracefully"""
        self._errors = []
        self._non_form_errors = forms.utils.ErrorList()
        
        if not self.is_bound:  # Stop here if the formset is not bound
            return
        
        # Clean each form individually, but skip validation for empty forms
        for i, form in enumerate(self.forms):
            # Only validate forms that have actual data or are existing instances
            if (form.has_changed() or form.instance.pk) and not form.empty_permitted:
                form.full_clean()
            elif form.empty_permitted:
                # For empty permitted forms, initialize errors and cleaned_data
                form._errors = forms.utils.ErrorDict()
                # Initialize cleaned_data to prevent AttributeError
                if not hasattr(form, 'cleaned_data'):
                    form.cleaned_data = {}
        
        # Skip minimum/maximum form validation since images are optional
        self._clean_form = True


# Create formset for multiple images
RoomImageFormSet = forms.inlineformset_factory(
    Room,
    RoomImage,
    form=RoomImageForm,
    formset=RoomImageFormSet,
    extra=1,  # At least 1 extra form for adding new images
    can_delete=True,
    min_num=0,  # Allow rooms without images
    validate_min=False,  # Don't enforce minimum image requirement
    max_num=5,  # Maximum 5 images
    validate_max=False  # Don't enforce maximum validation
)
class RoomReviewForm(forms.ModelForm):
    class Meta:
        model = RoomReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with this room...',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].empty_label = "Select Rating"


class RoomSearchForm(forms.Form):
    PRICE_CHOICES = [
        ('', 'Any Price'),
        ('0-10000', 'Under ₹10,000'),
        ('10000-20000', '₹10,000 - ₹20,000'),
        ('20000-30000', '₹20,000 - ₹30,000'),
        ('30000-50000', '₹30,000 - ₹50,000'),
        ('50000-100000', '₹50,000 - ₹1,00,000'),
        ('100000+', 'Above ₹1,00,000'),
    ]
    
    OCCUPANCY_CHOICES = [
        ('', 'Any'),
        ('1', '1 Person'),
        ('2', '2 People'),
        ('3', '3 People'),
        ('4', '4+ People'),
    ]

    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, city, or address...'
        })
    )
    
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Room.ROOM_CATEGORIES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    room_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Room.ROOM_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    price_range = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    
    max_occupancy = forms.ChoiceField(
        choices=OCCUPANCY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Amenity filters
    wifi = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    parking = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    ac = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    kitchen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class RoomReportForm(forms.ModelForm):
    class Meta:
        model = RoomReport
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-control',
                'id': 'reportReason'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please provide specific details about the issue...',
                'rows': 4,
                'id': 'reportDescription',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].empty_label = "Select a reason for reporting"
        self.fields['description'].required = True