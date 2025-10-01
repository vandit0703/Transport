from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class UserMaster(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )

    user_id = models.CharField(primary_key=True, max_length=50)  
    user_name = models.CharField(max_length=150) 
    password = models.CharField(max_length=256)
    user_level = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    last_login_date = models.DateTimeField(null=True, blank=True)
    last_password_change_date = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.last_password_change_date = timezone.now()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.user_name} ({self.user_id})"

class LoginHistory(models.Model):
    user = models.ForeignKey(
        'UserMaster',
        on_delete=models.CASCADE,
        related_name='login_history'
    )
    user_level = models.IntegerField()
    login_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user_id} - Level {self.user_level} - {self.login_date.strftime('%Y-%m-%d %H:%M:%S')}"

class PasswordHistory(models.Model):
    user = models.ForeignKey(
        'UserMaster',  
        on_delete=models.CASCADE,
        related_name='password_history'
    )
    password = models.CharField(max_length=256)  
    change_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user_id} - {self.change_date.strftime('%Y-%m-%d %H:%M:%S')}"


class TTOwnerMaster(models.Model):
    IDNumber = models.AutoField(primary_key=True)
    OwnerName = models.CharField(max_length=200)
    Address = models.TextField()
    City = models.CharField(max_length=100)
    PANGIR_Number = models.CharField(max_length=50, blank=True, null=True)
    Opening_Balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    Opg_Balance_Type = models.CharField(max_length=1, choices=[('D', 'Debit'), ('C', 'Credit')], default='D')
    If_Insurance = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    Number_Of_TT = models.IntegerField(default=0)
    TDS_Rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    If_Maintenance = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    Updated_On = models.DateTimeField(default=timezone.now)
    Updated_By = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.OwnerName} ({self.IDNumber})"

class ContractorMaster(models.Model):
    IdNumber = models.AutoField(primary_key=True)
    ContractorName = models.CharField(max_length=150)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=100,null=True)
    PhoneNumber_1 = models.CharField(max_length=15, blank=True, null=True)
    PhoneNumber_2 = models.CharField(max_length=15, blank=True, null=True)
    MobileNumber = models.CharField(max_length=15, blank=True, null=True)
    EmailID = models.CharField(max_length=100, blank=True, null=True)
    TPTR_Code = models.CharField(max_length=10, blank=True, null=True)
    Bill_Prefix = models.CharField(max_length=10, blank=True, null=True)
    BillNumber = models.IntegerField(default=0)
    If_Own = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    Updated_On = models.DateTimeField(default=timezone.now)
    Updated_By = models.CharField(max_length=10)

    def __str__(self):
        return self.ContractorName
    
class CompanyMaster(models.Model):
    IdNumber = models.AutoField(primary_key=True)  # Auto Increment primary key
    CompanyName = models.CharField(max_length=100)
    City = models.CharField(max_length=20)
    OpeningBalance = models.DecimalField(max_digits=12, decimal_places=2)
    OpeningBalanceType = models.CharField(max_length=1, blank=True, null=True)
    Bill_LU = models.CharField(max_length=1, blank=True, null=True)
    If_Hire = models.CharField(max_length=1, blank=True, null=True)
    Updated_On = models.DateTimeField(auto_now=True)
    Updated_By = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.CompanyName

class OwnerMasterNew(models.Model):
    OwnerCode = models.CharField(max_length=10, primary_key=True)
    OwnerName = models.CharField(max_length=100)

    def __str__(self):
        return self.OwnerName

class TTMasterNew(models.Model):
    IDNumber = models.AutoField(primary_key=True)
    TT_Registration_Number = models.CharField(max_length=15, unique=True)
    If_Own_TT = models.CharField(max_length=1, choices=[('Y','Yes'),('N','No')])
    Owner_Code = models.ForeignKey(OwnerMasterNew, on_delete=models.CASCADE)
    TT_KL_Size = models.PositiveIntegerField()
    Date_Of_Induction = models.DateField()
    Date_Of_Release = models.DateField(null=True, blank=True)
    TT_Make = models.CharField(max_length=20)
    TT_Model = models.CharField(max_length=20)
    Engine_Serial_Number = models.CharField(max_length=15)
    Chassis_Number = models.CharField(max_length=15)
    Whether_Dedicated = models.CharField(max_length=1, choices=[('Y','Yes'),('N','No')])
    Explosive_Licence_Number = models.CharField(max_length=15, null=True, blank=True)
    Explosive_Licence_Validity_Date = models.DateField(null=True, blank=True)
    Chemical_Licence_Validity_Date = models.DateField(null=True, blank=True)
    Insurance_Policy_Number = models.CharField(max_length=15)
    Insurance_Validity_Date = models.DateField()
    Insurance_Company = models.CharField(max_length=20)
    RTO_Due_Date = models.DateField()
    PAF_Due_Date = models.DateField()
    NP_Due_date = models.DateField()
    National_Permit_1 = models.CharField(max_length=10, null=True, blank=True)
    National_Permit_2 = models.CharField(max_length=10, null=True, blank=True)
    National_Permit_3 = models.CharField(max_length=10, null=True, blank=True)
    National_Permit_4 = models.CharField(max_length=10, null=True, blank=True)
    If_Hire = models.CharField(max_length=1, choices=[('Y','Yes'),('N','No')])
    If_Maintenance = models.CharField(max_length=1, choices=[('Y','Yes'),('N','No')])
    KM_Reading = models.PositiveIntegerField()
    Updated_On = models.DateTimeField(default=timezone.now)
    Update_By = models.CharField(max_length=10)

    def __str__(self):
        return self.TT_Registration_Number

class ProductMaster(models.Model):
    IDNumber = models.AutoField(primary_key=True)  
    Owner_Code = models.CharField(max_length=5)   
    Owner_Name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=12, decimal_places=2) 
    Short_Name = models.CharField(max_length=4)  
    If_Ejectt = models.CharField(max_length=1)    
    Updated_OPn = models.DateTimeField()        
    Updated_By = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.Owner_Code} - {self.Owner_Name}"

class Citymaster(models.Model):
    id_number = models.AutoField(primary_key=True)
    city_code = models.CharField(max_length=4)
    name = models.CharField(max_length=30)
    # t_zone = models.CharField(max_length=15)
    terminal = models.CharField(max_length=10)
    loc_code = models.CharField(max_length=5)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class FareMaster(models.Model):
    effective_date = models.DateField()
    owner_code = models.CharField(max_length=5)
    fare_from = models.ForeignKey(Citymaster, on_delete=models.CASCADE, related_name="fare_from")
    fare_to = models.ForeignKey(Citymaster, on_delete=models.CASCADE, related_name="fare_to")
    fare_rate = models.DecimalField(max_digits=12, decimal_places=2)
    fare_company = models.ForeignKey(CompanyMaster, on_delete=models.CASCADE)
    fare_product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE)
    if_nett = models.CharField(max_length=1)
    fare_type = models.CharField(max_length=1)
    rtd_kms = models.DecimalField(max_digits=4, decimal_places=0)
    product_type = models.CharField(max_length=1)
    range1_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range2_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range3_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range4_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range1_discount_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range2_discount_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range3_discount_fare = models.DecimalField(max_digits=12, decimal_places=2)
    range4_discount_fare = models.DecimalField(max_digits=12, decimal_places=2)
    if_hire = models.CharField(max_length=1)
    discount_fare = models.DecimalField(max_digits=12, decimal_places=2)
    shortage_full_deduction = models.CharField(max_length=1)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=10,blank=True, null=True)
