import io
from django.http import JsonResponse,FileResponse,HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import TestReport
import pickle
import pandas as pd
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from datetime import date
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':

        # Extract form data

        username = request.POST.get('email')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        account_type = request.POST.get('account_type')

        # Determine staff and superuser status based on account type

        is_staff = account_type != 'user'
        is_superuser = False
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=is_staff,
                is_superuser=is_superuser,
                )
            is_staff = user.is_staff if hasattr(user, 'is_staff') else False 
            if is_staff:
                redirect_url = 'user/admin_dashboard'
            else:
                redirect_url = 'user/user_dashboard'

            if user is not None:
                login(request, user)
                return JsonResponse(
                    {"message": "Signup successful", "redirectUrl": redirect_url}
                )
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Error creating user',
                                'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method'},
                        status=405)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        account_type = request.POST.get("account_type")
        if account_type == "user":
            is_staff = bool(False)
            is_superuser = bool(False)
        else:
            is_staff = bool(True)
            is_superuser = bool(True)
        user = authenticate(
            request,
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        is_staff = user.is_staff if hasattr(user, 'is_staff') else False   
        if is_staff:
            redirectUrl = "user/admin_dashboard"
        else:
            redirectUrl = "user/user_dashboard"

        if user is not None:
            login(request, user)
            return JsonResponse(
                {"message": "Login successful", "redirectUrl": redirectUrl}
            )
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def user_dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, "user_dashboard.html")
    else:
        return redirect("home")
    
@login_required
def generate_pdf(request,id):
    # Generate the PDF content using a template or other method
    Reports = TestReport.objects.filter(id=id)
    template = get_template('template.html')
    current_date = date.today().strftime("%B %d, %Y") 
    context = {
                'date': current_date,
                'reports': Reports,
                'user': request.user
               }
    html_content = template.render(context)
    
    # Create a BytesIO stream to hold the PDF data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    # Generate the PDF using a library like xhtml2pdf, weasyprint, reportlab, etc.
    # Here, we assume you're using xhtml2pdf library
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    
    # Set the position of the file pointer to the beginning of the file
    # pdf_file.seek(0)
    
    # Return the PDF file as a response
    if pisa_status.err:
        return HttpResponse('An error occurred while generating the PDF')
    return response
   
@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        if new_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Update the session with the new password
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@staff_member_required
def admin_dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, "admin_dashboard.html")
    else:
        return redirect("home")
    
@staff_member_required
def get_test_report(request):
    reports = TestReport.objects.all()  # Retrieve all users from the database
    report_list = []
    for report in reports:
        report_dict = [
            report.id,
            report.nitrogen,
            report.phosphorus,
            report.potassium,
            report.temperature,
            report.humidity,
            report.ph,
            report.rainfall,
            report.result
        ]
        report_list.append(report_dict)
    return JsonResponse({'data': report_list})

@login_required
def user_test_report(request):
    if request.user.is_authenticated:
        reports = TestReport.objects.filter(account_id=request.user.id)  # Retrieve all users from the database
        report_list = []
        for report in reports:
            edit_action = f'<a href="/user/generate-pdf/{report.id}/" type="button" class="btn btn-primary download-pdf"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-download-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 4.095 0 5.555 0 7.318 0 9.366 1.708 11 3.781 11H7.5V5.5a.5.5 0 0 1 1 0V11h4.188C14.502 11 16 9.57 16 7.773c0-1.636-1.242-2.969-2.834-3.194C12.923 1.999 10.69 0 8 0zm-.354 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V11h-1v3.293l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"></path></svg></a>'
            report_dict = [
                report.id,
                report.nitrogen,
                report.phosphorus,
                report.potassium,
                report.temperature,
                report.humidity,
                report.ph,
                report.rainfall,
                report.result,
                edit_action
            ]
            report_list.append(report_dict)
        return JsonResponse({'data': report_list})
    else:
        return JsonResponse('User is not authenticated')
    
@staff_member_required
def admin_generate_report(request):
    if request.method == 'GET':
        users = User.objects.all()  # Retrieve all users from the database
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return JsonResponse({'users': user_data})
    if request.method == 'POST':
        data = request.POST
        nitrogen = data.get('nitrogen')
        phosphorus = data.get('phosphorus')
        potassium = data.get('potassium')
        temperature= data.get('temperature')
        humidity = data.get('humidity')
        ph = data.get('ph')
        rainfall = data.get('rainfall')
        user_id = data.get('user_id')
        loadedModel = pickle.load(open('D:/agriculture_lab/accounts/static/RandomForest.pkl','rb'))
        mv = pd.DataFrame([[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]])
        result = loadedModel.predict(mv)
        test_report = TestReport(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            result=result[0],
            account_id=user_id,
        )

        # Save the test report
        test_report.save()
        return JsonResponse({'message': 'Test report saved successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)

    
@login_required
def update_profile(request,user_id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_active = request.POST.get('is_active', 'off')
        if is_active == 'on':
            is_active=1
        else:
            is_active=0
        user = get_object_or_404(User, id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.save()
        return JsonResponse({'success': True})
    if request.method == 'GET':
        user = get_object_or_404(User, id=user_id)
        user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active
        }
        return JsonResponse({'user': user_data,'success': True})    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_all_users(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        buttonClass = 'btn-success' if user.is_active else 'btn-danger'
        buttonText = 'Active' if user.is_active else 'Inactive'
        is_active = '<button class="btn {}">{}</button>'.format(buttonClass, buttonText)
        edit_action = f'<button class="btn btn-info edit-user" data-user-id="{ user.id }"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16"><path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/></svg> Edit</button>'
        user_dict = [
            user.id,
            user.email,
            user.first_name,
            user.last_name,
            user.last_login,
            is_active,
            edit_action
        ]
        user_list.append(user_dict)

    return JsonResponse({'data': user_list})