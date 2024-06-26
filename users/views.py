from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from botocore.exceptions import ClientError
from datetime import datetime
from collections import defaultdict, OrderedDict
from whistleblower_app.forms import UploadFileForm
from whistleblower_app.models import UploadedFile, Submission
from django.core.paginator import Paginator, Page



def profile(request):
    if(not request.user.is_authenticated):
        return redirect("index")
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3.list_objects_v2(Bucket='b29-whistleblower')
    submissions = defaultdict(list)
    is_site_admin = request.user.groups.filter(name="Site Admin").exists()  # Check once before the loop
    sort_key = request.GET.get('sort', 'default')
    if 'Contents' in response:
        for item in response['Contents']:
            file_key = item['Key']
            if "uploads/" in file_key:
                continue
            url = str(file_key).replace(' ', '_').replace('(', '').replace(')', '').replace('=','').replace('+', '').replace('#', '')
            idx = url.find('_')
            url = url [idx+1:]
        
            metadata_response = s3.head_object(Bucket='b29-whistleblower', Key=file_key)
            metadata = metadata_response.get('Metadata', {})
            submission_id = metadata.get('submission_id', "Old Files")
            if submission_id != None and request.user.username == metadata.get('username'):
                submissions[(submission_id, metadata.get('title'), metadata.get('username', 'No User Data Available'), metadata.get('description', 'No Description Available.'), metadata.get('tag', 'Other'))].append({
                    'url': url,
                    'username': metadata.get('username', 'No User Data Available'),
                    'description': metadata.get('description', 'No Description Available.'),
                    'status': metadata.get('status', 'In Progress'),
                    'note': metadata.get('note', ''),
                    'tag': metadata.get('tag', 'Other'),
                    'time': metadata.get('time', 'No Time Data Available.')
                })
            elif (is_site_admin and submission_id != None):
                submissions[(submission_id, metadata.get('title'), metadata.get('username', 'No User Data Available'), metadata.get('description', 'No Description Available.'), metadata.get('tag', 'Other'))].append({
                    'url': url,
                    'username': metadata.get('username', 'No User Data Available'),
                    'description': metadata.get('description', 'No Description Available.'),
                    'status': metadata.get('status', 'In Progress'),
                    'note': metadata.get('note', ''),
                    'tag': metadata.get('tag', 'Other'),
                    'time': metadata.get('time', 'No Time Data Available.')
                })

    status_order = {
        'New': 1,
        'In Progress': 2,
        'Resolved': 3
    }
    if sort_key == 'status':
        submissions = OrderedDict(sorted(submissions.items(), key=lambda x: status_order.get(x[1][0]['status'], 999)))
    elif sort_key == 'date':
        submissions = OrderedDict(sorted(submissions.items(), key=sort_time)[::-1])
    else:
        submissions = OrderedDict(submissions)
    paginator = Paginator(list(submissions.items()), 5)  # 5 submissions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if is_site_admin:
        return render(request, "users/siteadmin.html", {'page_obj': page_obj, 'selected_sort': sort_key})
    return render(request, "users/profile.html", {'page_obj': page_obj, 'selected_sort': sort_key, 'form': UploadFileForm})
def sort_time(item):
    time_str = item[1][0]['time']
    time_obj = None
    try: 
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %I:%M %p")
        hours = time_obj.hour + (12 if time_obj.strftime('%p') == 'AM' else 0)
        new_time = time_obj.replace(hour=hours % 24)
    except:
        new_time = datetime(2000, 1, 1)
    return new_time

@csrf_exempt
@require_http_methods(["POST"])
def change_file_status(request, submission_id):
    print("Received submission_id:", submission_id)
    new_status = request.POST.get('newStatus')
    note = request.POST.get('userNote')

    if not submission_id:
        render(request, 'users/siteadmin.html', {'any_error': 'Submission ID is missing'})
    
    if not new_status:
        render(request, 'users/siteadmin.html', {'any_error': 'Status is missing'})

    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    try:
        response = s3.list_objects_v2(Bucket='b29-whistleblower')
        if 'Contents' in response:
            for item in response['Contents']: 
                file_key = item['Key']
                if "uploads/" in file_key:
                    continue
                metadata_response = s3.head_object(Bucket='b29-whistleblower', Key=file_key)
                metadata = metadata_response.get('Metadata', {})
                if submission_id == metadata.get('submission_id', "Old Files"):
                    if metadata.get('status') == "Resolved":
                        continue
                    metadata['status'] = new_status
                    metadata['note'] = note if note is not None else metadata.get('note', '')

                    s3.copy_object(
                        Bucket='b29-whistleblower', 
                        CopySource={'Bucket': 'b29-whistleblower', 'Key': file_key},
                        Key=file_key, 
                        Metadata=metadata, 
                        MetadataDirective='REPLACE'
                    )
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return render(request, 'login', {'any_error': error_message})

    return redirect('login')
    

def edit_submission(request, submission_id):
    if request.method == 'POST':
        title = request.POST.get('edit-title')
        description = request.POST.get('edit-description')
        tag = request.POST.get('edit-tag')
        
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        try:
            response = s3.list_objects_v2(Bucket='b29-whistleblower')
            if 'Contents' in response:
                for item in response['Contents']: 
                    file_key = item['Key']
                    if "uploads/" in file_key:
                        continue
                    metadata_response = s3.head_object(Bucket='b29-whistleblower', Key=file_key)
                    metadata = metadata_response.get('Metadata', {})
                    if submission_id == metadata.get('submission_id', "Old Files"):
                        # print(note)
                        metadata['title'] = title
                        metadata['description'] = description
                        metadata['tag'] = tag
                        
                        s3.copy_object(
                            Bucket='b29-whistleblower', 
                            CopySource={'Bucket': 'b29-whistleblower', 'Key': file_key},
                            Key=file_key, 
                            Metadata=metadata, 
                            MetadataDirective='REPLACE'
                        )
            
            return redirect('login')
        
        except Submission.DoesNotExist:
            return render(request, 'users/templates/profile.html', {'any_error': 'The provided submission does not exist.'})
    
    else:
        return render(request, 'users/templates/profile.html', {'any_error': 'Stale request. Please try again'})


def delete_submission(request, submission_id):
    is_site_admin = request.user.groups.filter(name="Site Admin").exists()  # Check once before the loop
    if request.method == 'POST':
        try:
            # Initialize S3 client
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            
            # Retrieve all S3 objects in the bucket
            response = s3.list_objects_v2(Bucket='b29-whistleblower')

            # Iterate over S3 objects to find and delete the associated files
            for item in response.get('Contents', []):
                file_key = item['Key']
                metadata_response = s3.head_object(Bucket='b29-whistleblower', Key=file_key)
                metadata = metadata_response.get('Metadata', {})
                
                if metadata.get('submission_id') == str(submission_id):
                    # Delete the file from S3
                    s3.delete_object(Bucket='b29-whistleblower', Key=file_key)
                    print(f"Deleted S3 object: {file_key}")

                    # Delete the database entry (UploadedFile)
                    UploadedFile.objects.filter(submission_id=submission_id).delete()
                    print(f"Deleted UploadedFile entry for submission_id: {submission_id}")
            
            # Finally, delete the Submission itself
            Submission.objects.filter(id=submission_id).delete()
            print(f"Deleted Submission with id: {submission_id}")

            # If using Django storage, remove files from storage (example for FileSystemStorage)
            # Replace 'file' with the field name in UploadedFile model that stores the file
            uploaded_files = UploadedFile.objects.filter(submission_id=submission_id)
            for uploaded_file in uploaded_files:
                if uploaded_file.file:
                    uploaded_file.file.delete()  # Delete file from storage

            submissions = defaultdict(list)
            if is_site_admin:
                return render(request, "users/siteadmin.html",{'submissions': dict(submissions)})
            else:
                return redirect('login')
        
        except ClientError as e:
            error_message = e.response['Error']['Message']
            return render(request, 'login', {'any_error': error_message})



def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def test(request):
    return redirect("/whistleblower/")