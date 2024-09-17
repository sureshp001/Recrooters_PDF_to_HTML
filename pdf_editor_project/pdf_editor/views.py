from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.http import HttpResponse, FileResponse
from .forms import PDFUploadForm
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from weasyprint import HTML


# Upload folder
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'uploads/')
OUTPUT_FOLDER = os.path.join(settings.MEDIA_ROOT, 'output/')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Create your views here.

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file
            pdf_file = form.cleaned_data['pdf_file']
            file_path = os.path.join(UPLOAD_FOLDER, pdf_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Convert PDF to HTML
            html_content = convert_pdf_to_html(file_path)

            return render(request, 'pdf_editor/edit_pdf.html', {
                'html_content': html_content,
                'file_name': pdf_file.name,
            })
    else:
        form = PDFUploadForm()
    
    return render(request, 'pdf_editor/upload_pdf.html', {'form': form})

def convert_pdf_to_html(pdf_path):
    doc = fitz.open(pdf_path)
    html_pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        html_content = page.get_text("html")
        html_pages.append(html_content)

    complete_html = ''.join(html_pages)
    soup = BeautifulSoup(complete_html, 'html.parser')

    return soup.prettify()

def convert_back_to_pdf(request):
    if request.method == 'POST':
        html_content = request.POST['html_content']
        file_name = request.POST['file_name']
        output_html_path = os.path.join(OUTPUT_FOLDER, 'edited_' + file_name + '.html')

        # Save edited HTML
        with open(output_html_path, 'w') as html_file:
            html_file.write(html_content)

        # Convert back to PDF
        output_pdf_path = os.path.join(OUTPUT_FOLDER, 'edited_' + file_name + '.pdf')
        HTML(output_html_path).write_pdf(output_pdf_path)

        return FileResponse(open(output_pdf_path, 'rb'), as_attachment=True)

    return redirect('upload_pdf')
