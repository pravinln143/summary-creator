from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import UploadedFile
import pandas as pd
from django.template.loader import render_to_string

def file_upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        # Read the file into a pandas DataFrame
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
        
        # Custom Summary - Aggregating by 'Cust State'
        summary = data.groupby('Cust State').agg(
            count=('DPD', 'count'),
            total_dpd=('DPD', 'sum'),
            average_dpd=('DPD', 'mean'),
            max_dpd=('DPD', 'max')
        ).reset_index()

        # Convert the summary DataFrame to HTML with customized styles
        summary_html = summary.style.set_table_attributes('class="dataframe" border="1"').format(precision=2).to_html()

        # Create a summary report as an HTML email message
        email_subject = 'Customized Data Summary Report'
        email_message = render_to_string('email_report.html', {'summary_html': summary_html})

        # Send email with the summary report
        send_mail(
            subject= "Pravin Prajapati",
            message='Please find the customized summary report attached.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['tech@themedius.ai'],
            html_message=email_message,
        )

        # Render the success page
        return render(request, 'success.html')

    return render(request, 'upload.html')
