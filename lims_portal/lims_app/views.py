from django.contrib import admin
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q

import csv
import hashlib
import boto3
import os
from django.http import HttpResponse
from django.conf import settings
from .models import reader  # Make sure the model is named `reader`

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = 'library-exports-priyanshu'
REGION = 'ap-south-1'


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

def ensure_bucket_exists():
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except s3.exceptions.ClientError:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )

def export_readers_to_s3(request):
    ensure_bucket_exists()

    readers = reader.objects.all()
    total = readers.count()

    if total == 0:
        return HttpResponse("⚠️ No reader data available.")

    def hash_row(row):
        return hashlib.md5(",".join(str(i) for i in row).encode()).hexdigest()

    chunk_size = max(int(total * 0.1), 1)  
    uploaded_count = 0
    index = 0

    new_hashes = []

    for r in readers:
        row = [r.reference_id,r.reader_name,r.reader_contact,r.reader_address]  
        row_hash = hash_row(row)
        key = f"{row_hash}.csv"

        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=key)
        except:
            new_hashes.append((key, row))

        index += 1

        if index % chunk_size == 0 or index == total:
            if new_hashes: 
                filename = f"readers_chunk_{index}.csv"
                path = os.path.join("/tmp", filename)

                with open(path, "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Reference ID", "Name", "Contact", "Address"])  # Customize headers
                    for _, row in new_hashes:
                        writer.writerow(row)

                for key, _ in new_hashes:
                    s3.upload_file(path, BUCKET_NAME, key)
                    uploaded_count += 1

                new_hashes = []

    if uploaded_count:
        return HttpResponse(f"✅ Exported {uploaded_count} unique readers to S3 in chunks.")
    else:
        return HttpResponse("⚠️ No new unique readers to export.")




# Create your views here.

def home(request):
    return render(request, "home.html", context={"current_page": "home"})

def readers(request):
    return render(request, "readers.html", context={"current_page": "readers"})

def save_student(request):
    student_name = request.POST.get("student_name")
    return render(request, "welcome.html", context={'student_name': student_name})

def readers_tab(request):
    if request.method == "POST":
        query = request.POST.get("query", "")
        readers = reader.objects.filter(reader_name__icontains=query)
    else:
        query = ""
        readers = reader.objects.all()
    
    paginator = Paginator(readers, 6)  # Show 6 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "readers.html", {"readers": page_obj, "query": query})


def save_reader(request):
    reader_item = reader(reference_id =request.POST["reader_ref_id"],
                         reader_name=request.POST["reader_name"],
                         reader_contact=request.POST["reader_contact"],
                         reader_address=request.POST["reader_address"],
                         active=True
    )
    reader_item.save()
    return redirect("/readers")

def edit_reader(request, reader_id):
    reader_obj = get_object_or_404(reader, id=reader_id)
    page = request.GET.get("page", 1)

    if request.method == "POST":
        reader_obj.reader_name = request.POST.get("reader_name")
        reader_obj.reader_contact = request.POST.get("reader_contact")
        reader_obj.reference_id = request.POST.get("reader_ref_id")
        reader_obj.reader_address = request.POST.get("reader_address")
        reader_obj.save()
        return redirect(f"/readers?page={page}")

    return render(request, 'edit_reader.html', {"reader": reader_obj, "page": page})


def delete_reader(request, reader_id):
    reader_obj = get_object_or_404(reader, id=reader_id)
    reader_obj.delete()

    # After deletion, count remaining readers
    total_readers = reader.objects.count()
    page = int(request.GET.get("page", 1))

    # Adjust page if current page becomes empty
    last_page = (total_readers // 6) + (1 if total_readers % 6 else 0)
    if page > last_page:
        page = last_page

    return redirect(f"/readers?page={page}")
