from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def profile(request):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3.list_objects_v2(Bucket='b29-whistleblower')
    files = []
    is_site_admin = request.user.groups.filter(name="Site Admin").exists()  # Check once before the loop

    if 'Contents' in response:
        for item in response['Contents']:
            file_key = item['Key']
            if "uploads/" in file_key:
                continue
            url = str(file_key).replace(' ', '_')
            metadata_response = s3.head_object(Bucket='b29-whistleblower', Key=file_key)
            metadata = metadata_response.get('Metadata', {})
            if is_site_admin or request.user.username == metadata.get('username'):
                files.append({
                    'url': url,
                    'name': metadata.get('title', file_key),
                    'username': metadata.get('username', 'No User Data Available'),
                    'description': metadata.get('description', 'No Description Available.'),
                    'status': metadata.get('status', 'In Progress')
                })
    print(files)
    if is_site_admin:
        return render(request, "siteadmin.html", {'files': files})
    else:
        return render(request, "profile.html", {'files': files})
    
@csrf_exempt
@require_http_methods(["POST"])
def change_file_status(request):
    print(
        'hi'
    )
    file_name = request.POST.get('fileName')
    new_status = request.POST.get('newStatus')

    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3.head_object(Bucket='YOUR_BUCKET_NAME', Key=file_name)
    metadata = response.get('Metadata', {})
    metadata['status'] = new_status
    s3.copy_object(Bucket='b29-whistleblower', CopySource={'Bucket': 'b29-whistleblower', 'Key': file_name}, Key=file_name, Metadata=metadata, MetadataDirective='REPLACE')

    return JsonResponse({"message": "Status updated successfully"})

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def test(request):
    return redirect("/whistleblower/")