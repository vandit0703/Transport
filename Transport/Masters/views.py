from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required

from .models import (
    UserMaster, LoginHistory, PasswordHistory, TTMasterNew,
    TTOwnerMaster, ContractorMaster, CompanyMaster,
    ProductMaster, Citymaster, FareMaster
)
from .forms import (
    TTOwnerMasterForm, UserMasterForm, TTMasterForm,
    ProductMasterForm, CitymasterForm, FareMasterForm
)

# -----------------------
# Authentication
# -----------------------

def user_login(request):
    if request.method == "POST":
        user_id = request.POST.get("username")
        user_name = request.POST.get("username1")
        password = request.POST.get("password")
        user_level = request.POST.get("user_level")

        try:
            user = UserMaster.objects.get(user_id=user_id)
        except UserMaster.DoesNotExist:
            messages.error(request, "Invalid User ID, Username, or Level")
            return render(request, 'Masters/login.html')

        if user.check_password(password):
            user.last_login_date = timezone.now()
            user.save()

            LoginHistory.objects.create(
                user=user,
                user_level=user.user_level
            )

            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name
            request.session['user_level'] = user.user_level

            return redirect('home')
        else:
            messages.error(request, "Incorrect password")
            return render(request, 'Masters/login.html')

    return render(request, 'Masters/login.html')


def home(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'Masters/home.html')


def change_password(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user = UserMaster.objects.get(user_id=request.session['user_id'])

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not user.check_password(old_password):
            messages.error(request, "Current password is incorrect")
            return render(request, 'Masters/change_password.html')

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match")
            return render(request, 'Masters/change_password.html')

        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.last_password_change_date = timezone.now()
        user.save()

        PasswordHistory.objects.create(
            user=user,
            password=hashed_password,
            change_date=user.last_password_change_date
        )

        messages.success(request, "Password changed successfully")
        return redirect('home')

    return render(request, 'Masters/change_password.html')


# -----------------------
# TT Owner
# -----------------------

def ttowner_list(request):
    query = request.GET.get('q', '')
    if query:
        owners = TTOwnerMaster.objects.filter(
            Q(OwnerName__icontains=query) |
            Q(City__icontains=query) |
            Q(PANGIR_Number__icontains=query)
        )
    else:
        owners = TTOwnerMaster.objects.all()
    return render(request, 'Masters/ttowner_list.html', {'owners': owners})


def ttowner_add(request):
    if request.method == "POST":
        form = TTOwnerMasterForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.Updated_By = request.session.get("user_name", "System")
            owner.Updated_On = timezone.now()
            owner.save()
            messages.success(request, "TT Owner added successfully")
            return redirect('ttowner_list')
    else:
        form = TTOwnerMasterForm()
    return render(request, 'Masters/ttowner.html', {'form': form, 'title': 'Add TT Owner'})


def ttowner_edit(request, id):
    owner = get_object_or_404(TTOwnerMaster, IDNumber=id)
    if request.method == "POST":
        form = TTOwnerMasterForm(request.POST, instance=owner)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.Updated_By = request.session.get("user_name", "System")
            owner.Updated_On = timezone.now()
            owner.save()
            messages.success(request, "TT Owner updated successfully")
            return redirect('ttowner_list')
    else:
        form = TTOwnerMasterForm(instance=owner)
    return render(request, 'Masters/ttowner.html', {'form': form, 'edit': True})


def ttowner_delete(request, id):
    owner = get_object_or_404(TTOwnerMaster, IDNumber=id)
    if request.method == "POST":
        owner.delete()
        messages.success(request, "TT Owner deleted successfully")
        return redirect('ttowner_list')
    return render(request, 'Masters/ttowner_confirm_delete.html', {'owner': owner})


# -----------------------
# User Registration
# -----------------------

def register_user(request):
    if request.method == 'POST':
        form = UserMasterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User registered successfully!")
            return redirect('home')
    else:
        form = UserMasterForm()
    return render(request, 'Masters/register.html', {'form': form})


# -----------------------
# Company
# -----------------------

def company_add(request):
    if request.method == "POST":
        company = CompanyMaster(
            CompanyName=request.POST.get("company_name"),
            City=request.POST.get("city"),
            OpeningBalance=request.POST.get("opening_balance"),
            OpeningBalanceType=request.POST.get("opening_balance_type"),
            Bill_LU=request.POST.get("bill_lu"),
            If_Hire=request.POST.get("if_hire"),
            Updated_On=timezone.now(),
            Updated_By=request.session.get("user_name", "System"),
        )
        company.save()
        return redirect('company_list')

    return render(request, 'Masters/company_form.html')


def company_list(request):
    query = request.GET.get('q', '')
    if query:
        companies = CompanyMaster.objects.filter(
            Q(CompanyName__icontains=query) |
            Q(City__icontains=query) |
            Q(OpeningBalanceType__icontains=query) |
            Q(Updated_By__icontains=query)
        )
    else:
        companies = CompanyMaster.objects.all()
    return render(request, 'Masters/company_list.html', {'companies': companies})


def company_edit(request, pk):
    company = get_object_or_404(CompanyMaster, IdNumber=pk)
    if request.method == "POST":
        company.CompanyName = request.POST.get("company_name")
        company.City = request.POST.get("city")
        company.OpeningBalance = request.POST.get("opening_balance")
        company.OpeningBalanceType = request.POST.get("opening_balance_type")
        company.Bill_LU = request.POST.get("bill_lu")
        company.If_Hire = request.POST.get("if_hire")
        company.Updated_By = request.session.get("user_name", "System")
        company.Updated_On = timezone.now()
        company.save()
        return redirect('company_list')
    return render(request, 'Masters/company_form.html', {'company': company})


def company_delete(request, pk):
    company = get_object_or_404(CompanyMaster, IdNumber=pk)
    if request.method == "POST":
        company.delete()
        return redirect('company_list')
    return render(request, 'Masters/company_confirm_delete.html', {'company': company})


# -----------------------
# Contractor
# -----------------------

def contractor_list(request):
    query = request.GET.get('q', '')
    if query:
        contractors = ContractorMaster.objects.filter(
            Q(ContractorName__icontains=query) |
            Q(City__icontains=query) |
            Q(EmailID__icontains=query) |
            Q(MobileNumber__icontains=query) |
            Q(Updated_By__icontains=query)
        )
    else:
        contractors = ContractorMaster.objects.all()
    return render(request, 'Masters/contractor_list.html', {'contractors': contractors})


def contractor_add(request):
    if request.method == 'POST':
        contractor = ContractorMaster(
            ContractorName=request.POST.get('ContractorName'),
            Address=request.POST.get('Address'),
            City=request.POST.get('City'),
            PhoneNumber_1=request.POST.get('PhoneNumber_1'),
            PhoneNumber_2=request.POST.get('PhoneNumber_2'),
            MobileNumber=request.POST.get('MobileNumber'),
            EmailID=request.POST.get('EmailID'),
            TPTR_Code=request.POST.get('TPTR_Code'),
            Bill_Prefix=request.POST.get('Bill_Prefix'),
            BillNumber=request.POST.get('BillNumber'),
            If_Own=request.POST.get('If_Own', 'N'),
            Updated_By=request.session.get("user_name", "System"),
        )
        contractor.save()
        return redirect('contractor_list')
    return render(request, 'Masters/contractor_form.html')


def contractor_edit(request, pk):
    contractor = get_object_or_404(ContractorMaster, IdNumber=pk)
    if request.method == 'POST':
        contractor.ContractorName = request.POST.get('ContractorName')
        contractor.Address = request.POST.get('Address')
        contractor.City = request.POST.get('City')
        contractor.PhoneNumber_1 = request.POST.get('PhoneNumber_1')
        contractor.PhoneNumber_2 = request.POST.get('PhoneNumber_2')
        contractor.MobileNumber = request.POST.get('MobileNumber')
        contractor.EmailID = request.POST.get('EmailID')
        contractor.TPTR_Code = request.POST.get('TPTR_Code')
        contractor.Bill_Prefix = request.POST.get('Bill_Prefix')
        contractor.BillNumber = request.POST.get('BillNumber')
        contractor.If_Own = request.POST.get('If_Own', 'N')
        contractor.Updated_By = request.session.get("user_name", "System")
        contractor.save()
        return redirect('contractor_list')
    return render(request, 'Masters/contractor_form.html', {'contractor': contractor})


def contractor_delete(request, pk):
    contractor = get_object_or_404(ContractorMaster, IdNumber=pk)
    if request.method == 'POST':
        contractor.delete()
        return redirect('contractor_list')
    return render(request, 'Masters/contractor_confirm_delete.html', {'contractor': contractor})


# -----------------------
# TT Master
# -----------------------

def ttmaster_list(request):
    query = request.GET.get('q', '')
    if query:
        ttmasters = TTMasterNew.objects.filter(
            Q(Truck_No__icontains=query) |
            Q(Owner_Name__icontains=query) |
            Q(TT_Type__icontains=query)
        ).order_by('-IDNumber')
    else:
        ttmasters = TTMasterNew.objects.all().order_by('-IDNumber')
    return render(request, 'Masters/ttmaster_list.html', {'ttmasters': ttmasters})


def ttmaster_add(request):
    if request.method == 'POST':
        form = TTMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'TT record added successfully.')
            return redirect('ttmaster_list')
    else:
        form = TTMasterForm()
    return render(request, 'Masters/ttmaster_form.html', {'form': form, 'title': 'Add TT'})


def ttmaster_edit(request, id):
    tt = get_object_or_404(TTMasterNew, IDNumber=id)
    if request.method == 'POST':
        form = TTMasterForm(request.POST, instance=tt)
        if form.is_valid():
            form.save()
            messages.success(request, 'TT record updated successfully.')
            return redirect('ttmaster_list')
    else:
        form = TTMasterForm(instance=tt)
    return render(request, 'Masters/ttmaster_form.html', {'form': form, 'title': 'Edit TT'})


def ttmaster_delete(request, id):
    tt = get_object_or_404(TTMasterNew, IDNumber=id)
    if request.method == 'POST':
        tt.delete()
        messages.success(request, 'TT record deleted successfully.')
        return redirect('ttmaster_list')
    return render(request, 'Masters/ttmaster_confirm_delete.html', {'tt': tt})


# -----------------------
# Product Master
# -----------------------

def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = ProductMaster.objects.filter(
            Q(Owner_Code__icontains=query) |
            Q(Owner_Name__icontains=query) |
            Q(Short_Name__icontains=query) |
            Q(Updated_By__icontains=query)
        ).order_by('-IDNumber')
    else:
        products = ProductMaster.objects.all().order_by('-IDNumber')
    return render(request, 'Masters/product_list.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        form = ProductMasterForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # set Updated_By as login user from session
            product.Updated_By = request.session.get('user_name', 'System')
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('product_list')
    else:
        form = ProductMasterForm()
    return render(request, 'Masters/Product_form.html', {'form': form})


def product_edit(request, pk):
    product = get_object_or_404(ProductMaster, pk=pk)
    if request.method == 'POST':
        form = ProductMasterForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.Updated_By = request.session.get('user_name', 'System')
            product.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
    else:
        form = ProductMasterForm(instance=product)
    return render(request, 'Masters/Product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(ProductMaster, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'Masters/product_confirm_delete.html', {'product': product})


# -----------------------
# City Master
# -----------------------

def citymaster_list(request):
    query = request.GET.get('q', '')
    if query:
        cities = Citymaster.objects.filter(
            Q(city_name__icontains=query) |
            Q(state__icontains=query) |
            Q(updated_by__icontains=query)
        )
    else:
        cities = Citymaster.objects.all()
    return render(request, 'Masters/citymaster_list.html', {'cities': cities})


def citymaster_create(request):
    if request.method == 'POST':
        form = CitymasterForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.updated_by = request.session.get("user_name", "System")
            city.save()
            return redirect('citymaster_list')
    else:
        form = CitymasterForm()
    return render(request, 'Masters/citymaster_form.html', {'form': form})


def citymaster_edit(request, id):
    city = get_object_or_404(Citymaster, id_number=id)
    if request.method == 'POST':
        form = CitymasterForm(request.POST, instance=city)
        if form.is_valid():
            city = form.save(commit=False)
            city.updated_by = request.session.get("user_name", "System")
            city.updated_on = timezone.now()
            city.save()
            return redirect('citymaster_list')
    else:
        form = CitymasterForm(instance=city)
    return render(request, 'Masters/citymaster_form.html', {'form': form})


def citymaster_delete(request, id):
    city = get_object_or_404(Citymaster, id_number=id)
    if request.method == 'POST':
        city.delete()
        return redirect('citymaster_list')
    return render(request, 'Masters/citymaster_confirm_delete.html', {'city': city})


# -----------------------
# Fare Master
# -----------------------

def fare_list(request):
    query = request.GET.get('q', '')
    if query:
        fares = FareMaster.objects.filter(
            Q(owner_code__icontains=query) |
            Q(fare_from__city_name__icontains=query) |
            Q(fare_to__city_name__icontains=query) |
            Q(fare_company__CompanyName__icontains=query) |
            Q(fare_product__Owner_Name__icontains=query) |
            Q(updated_by__icontains=query)
        ).order_by('-effective_date')
    else:
        fares = FareMaster.objects.all().order_by('-effective_date')
    return render(request, 'Masters/fare_list.html', {'fares': fares})


def fare_create(request):
    cities = Citymaster.objects.all()
    companies = CompanyMaster.objects.all()
    products = ProductMaster.objects.all()

    if request.method == "POST":
        fare_from = request.POST.get("Fare_From")
        fare_to = request.POST.get("Fare_To")

        if fare_from == fare_to:
            messages.error(request, "Fare From and Fare To cannot be the same city.")
            return render(request, "Masters/fare_form.html", {
                "fare": None, "cities": cities, "companies": companies, "products": products
            })

        FareMaster.objects.create(
            effective_date=request.POST.get("Effective_Date"),
            owner_code=request.POST.get("Owner_Code"),
            fare_from_id=fare_from,
            fare_to_id=fare_to,
            fare_rate=request.POST.get("Fare_Rate"),
            fare_company_id=request.POST.get("Fare_Company"),
            fare_product_id=request.POST.get("Fare_Product"),
            if_nett=request.POST.get("If_Nett"),
            fare_type=request.POST.get("Fare_Type"),
            rtd_kms=request.POST.get("RTD_Kms"),
            product_type=request.POST.get("Product_Type"),
            range1_fare=request.POST.get("Range1_Fare"),
            range2_fare=request.POST.get("Range2_Fare"),
            range3_fare=request.POST.get("Range3_Fare"),
            range4_fare=request.POST.get("Range4_Fare"),
            range1_discount_fare=request.POST.get("Range1_Discount_Fare"),
            range2_discount_fare=request.POST.get("Range2_Discount_Fare"),
            range3_discount_fare=request.POST.get("Range3_Discount_Fare"),
            range4_discount_fare=request.POST.get("Range4_Discount_Fare"),
            if_hire=request.POST.get("If_Hire"),
            discount_fare=request.POST.get("Discount_Fare"),
            shortage_full_deduction=request.POST.get("Shortage_Full_Deduction"),
            updated_by=request.session.get("user_name", "System"),
        )
        return redirect("fare_list")

    return render(request, "Masters/fare_form.html", {
        "fare": None, "cities": cities, "companies": companies, "products": products
    })


def fare_edit(request, id):
    fare = get_object_or_404(FareMaster, id=id)
    cities = Citymaster.objects.all()
    companies = CompanyMaster.objects.all()
    products = ProductMaster.objects.all()

    if request.method == "POST":
        if request.POST.get("Fare_From") == request.POST.get("Fare_To"):
            messages.error(request, "Fare From and Fare To cannot be the same city.")
            return render(request, "Masters/fare_form.html", {
                "fare": fare, "cities": cities, "companies": companies, "products": products
            })

        fare.effective_date = request.POST.get("Effective_Date")
        fare.owner_code = request.POST.get("Owner_Code")
        fare.fare_from_id = request.POST.get("Fare_From")
        fare.fare_to_id = request.POST.get("Fare_To")
        fare.fare_rate = request.POST.get("Fare_Rate")
        fare.fare_company_id = request.POST.get("Fare_Company")
        fare.fare_product_id = request.POST.get("Fare_Product")
        fare.if_nett = request.POST.get("If_Nett")
        fare.fare_type = request.POST.get("Fare_Type")
        fare.rtd_kms = request.POST.get("RTD_Kms")
        fare.product_type = request.POST.get("Product_Type")
        fare.range1_fare = request.POST.get("Range1_Fare")
        fare.range2_fare = request.POST.get("Range2_Fare")
        fare.range3_fare = request.POST.get("Range3_Fare")
        fare.range4_fare = request.POST.get("Range4_Fare")
        fare.range1_discount_fare = request.POST.get("Range1_Discount_Fare")
        fare.range2_discount_fare = request.POST.get("Range2_Discount_Fare")
        fare.range3_discount_fare = request.POST.get("Range3_Discount_Fare")
        fare.range4_discount_fare = request.POST.get("Range4_Discount_Fare")
        fare.if_hire = request.POST.get("If_Hire")
        fare.discount_fare = request.POST.get("Discount_Fare")
        fare.shortage_full_deduction = request.POST.get("Shortage_Full_Deduction")
        fare.updated_by = request.session.get("user_name", "System")
        fare.save()
        return redirect("fare_list")

    return render(request, "Masters/fare_form.html", {
        "fare": fare, "cities": cities, "companies": companies, "products": products
    })


def fare_delete(request, id):
    fare = get_object_or_404(FareMaster, id=id)
    if request.method == "POST":
        fare.delete()
        return redirect("fare_list")
    return render(request, "Masters/fare_confirm_delete.html", {'fare': fare})
