from django import forms
from .models import TTOwnerMaster,UserMaster,TTMasterNew,ProductMaster,Citymaster,FareMaster

class TTOwnerMasterForm(forms.ModelForm):
    class Meta:
        model = TTOwnerMaster
        fields = [
            'OwnerName', 'Address', 'City', 'PANGIR_Number',
            'Opening_Balance', 'Opg_Balance_Type', 'If_Insurance',
            'Number_Of_TT', 'TDS_Rate', 'If_Maintenance'
        ]
        widgets = {
            'OwnerName': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Owner Name'}),
            'Address': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Address', 'rows': 2}),
            'City': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'City'}),
            'PANGIR_Number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'PAN/GIR Number'}),
            'Opening_Balance': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Opening Balance'}),
            'Opg_Balance_Type': forms.Select(attrs={'class': 'input-field'}),
            'If_Insurance': forms.Select(attrs={'class': 'input-field'}),
            'Number_Of_TT': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Number of TT'}),
            'TDS_Rate': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'TDS Rate'}),
            'If_Maintenance': forms.Select(attrs={'class': 'input-field'}),
        }

class UserMasterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserMaster
        fields = ['user_id', 'user_name', 'password', 'user_level', 'status']

class TTMasterForm(forms.ModelForm):
    class Meta:
        model = TTMasterNew
        fields = '__all__' 
        widgets = {
            'Date_Of_Induction': forms.DateInput(attrs={'type': 'date'}),
            'Date_Of_Release': forms.DateInput(attrs={'type': 'date'}),
            'Explosive_Licence_Validity_Date': forms.DateInput(attrs={'type': 'date'}),
            'Chemical_Licence_Validity_Date': forms.DateInput(attrs={'type': 'date'}),
            'Insurance_Validity_Date': forms.DateInput(attrs={'type': 'date'}),
            'RTO_Due_Date': forms.DateInput(attrs={'type': 'date'}),
            'PAF_Due_Date': forms.DateInput(attrs={'type': 'date'}),
            'NP_Due_date': forms.DateInput(attrs={'type': 'date'}),
            'Updated_On': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ProductMasterForm(forms.ModelForm):
    class Meta:
        model = ProductMaster
        fields = ['Owner_Code','Owner_Name','Rate','Short_Name','If_Ejectt','Updated_OPn']
        widgets = {
            'Updated_OPn': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CitymasterForm(forms.ModelForm):
    class Meta:
        model = Citymaster
        fields = ['city_code','name','terminal','loc_code']

class FareMasterForm(forms.ModelForm):
    class Meta:
        model = FareMaster
        fields = '__all__'