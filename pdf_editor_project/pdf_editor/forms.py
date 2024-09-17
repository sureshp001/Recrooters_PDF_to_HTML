from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Upload PDF', widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))
