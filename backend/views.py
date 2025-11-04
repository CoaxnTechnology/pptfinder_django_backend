from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import time

def api_keywords(request):
    keywords = {"categories":[{"category":"Engineering","fields":[{"occupation":"Computer Engineer","thumb":"computer engineer.png","keywords":["Data Structures","Algorithms","Machine Learning","Artificial Intelligence","Networking","Operating Systems","Database Management","Software Engineering","Cybersecurity","Cloud Computing"]},{"occupation":"Civil Engineer","thumb":"civilengineer.png","keywords":["Structural Analysis","Geotechnical Engineering","Hydraulics","Surveying","Construction Materials","Transportation Engineering","Environmental Engineering","Project Management","Building Information Modeling (BIM)","Urban Planning"]},{"occupation":"Mechanical Engineer","thumb":"mechanicalengineer.png","keywords":["Thermodynamics","Fluid Mechanics","Heat Transfer","Manufacturing Processes","Dynamics","Mechanical Design","Control Systems","Materials Science","Robotics","Energy Systems"]},{"occupation":"Electrical Engineer","thumb":"electrical-energy.png","keywords":["Circuit Analysis","Electromagnetics","Power Systems","Control Systems","Signal Processing","Analog Electronics","Digital Electronics","Microelectronics","Renewable Energy","Telecommunications"]},{"occupation":"Electronics Engineer","thumb":"electronicengineer.png","keywords":["Semiconductor Devices","Digital Circuits","Microcontrollers","Embedded Systems","Signal Processing","Communication Systems","VLSI Design","Analog Electronics","Instrumentation","Optoelectronics"]},{"occupation":"Chemical Engineer","thumb":"chemical engineer.png","keywords":["Chemical Reactions","Process Engineering","Thermodynamics","Fluid Dynamics","Materials Science","Biochemical Engineering","Petroleum Engineering","Environmental Engineering","Process Control","Catalysis"]}]},{"category":"Medical","fields":[{"occupation":"Medical","thumb":"medical.png","keywords":["Anatomy","Physiology","Pathology","Pharmacology","Biochemistry","Surgery","Internal Medicine","Pediatrics","Radiology","Public Health"]},{"occupation":"Dental","thumb":"dental.png","keywords":["Oral Anatomy","Periodontology","Oral Surgery","Dental Materials","Orthodontics","Endodontics","Prosthodontics","Oral Radiology","Community Dentistry","Oral Pathology"]},{"occupation":"Nursing","thumb":"nursing.png","keywords":["Patient Care","Clinical Assessment","Pharmacology","Nursing Ethics","Critical Care","Pediatrics","Obstetrics","Geriatrics","Mental Health","Community Health"]},{"occupation":"Pharmacy","thumb":"pharmacy.png","keywords":["Pharmacology","Pharmaceutical Chemistry","Clinical Pharmacy","Pharmaceutics","Pharmacokinetics","Pharmaceutical Biotechnology","Pharmacy Practice","Pharmacognosy","Pharmaceutical Analysis","Toxicology"]}]},{"category":"Business","fields":[{"occupation":"Business Administration","thumb":"business administration.png","keywords":["Management Principles","Business Ethics","Marketing Strategy","Financial Management","Organizational Behavior","Human Resource Management","Operations Management","Strategic Planning","Business Analytics","Supply Chain Management"]},{"occupation":"Finance","thumb":"finance.png","keywords":["Corporate Finance","Financial Markets","Investment Banking","Portfolio Management","Risk Management","Financial Analysis","Taxation","Accounting","Personal Finance","Econometrics"]},{"occupation":"Marketing","thumb":"marketing.png","keywords":["Consumer Behavior","Market Research","Digital Marketing","Brand Management","Product Development","Social Media Marketing","Advertising","Public Relations","SEO","Sales Strategies"]},{"occupation":"Accounting","thumb":"accounting.png","keywords":["Financial Accounting","Management Accounting","Auditing","Taxation","Cost Accounting","Forensic Accounting","International Accounting","Accounting Information Systems","Ethical Issues in Accounting","Financial Reporting Standards"]},{"occupation":"Economics","thumb":"economic.png","keywords":["Microeconomics","Macroeconomics","Game Theory","Development Economics","Labor Economics","International Trade","Public Economics","Behavioral Economics","Monetary Policy","Environmental Economics"]}]}],"general":{"keywords":["Leadership","Time Management","Communication Skills","Teamwork","Critical Thinking","Project Management","Problem Solving","Creativity","Innovation","Negotiation"]}}
    return JsonResponse(keywords)

def api_check_keyword(request):
    keyword = request.GET.get('keyword', '').strip()
    if not keyword:
        return JsonResponse({'exists': False, 'object': None})
    from backend.models import Pptdata
    exists = Pptdata.objects.filter(keyword=keyword).exists()
    return JsonResponse({'exists': exists, 'object': json.loads(Pptdata.objects.filter(keyword=keyword).first().object) if exists else None})

@csrf_exempt
def api_save_data(request):
    if request.method == 'POST':
        try:
            from backend.models import Pptdata
            pptdata = Pptdata(
                keyword=request.POST.get('keyword'),
                object=request.POST.get('object'),
                timestamp=int(time.time())
            )
            pptdata.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def api_privacy_policy(request):
    return render(request, 'privacy_policy_pptfinder.html')

@require_http_methods(["GET"])
def serve_png(request, filename):
    # Security: Ensure it ends with .png and doesn't contain path traversal
    if not filename.endswith('.png') or '..' in filename or filename.startswith('/'):
        raise Http404("Invalid file")

    # Try to find the file using Django's staticfiles finder
    try:
        full_path = staticfiles_storage.path(filename)
    except (ValueError, NotImplementedError):
        # staticfiles_storage.path() may not be available (e.g. on S3 in prod)
        raise Http404("Static file storage does not support path access")

    if not os.path.isfile(full_path):
        raise Http404("PNG not found")

    with open(full_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')