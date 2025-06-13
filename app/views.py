from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import localtime
from .models import *
import json
import logging
from pytz import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive

logger = logging.getLogger(__name__)

@csrf_exempt
def classes_view(request):
    if request.method == 'GET':
        user_tz = request.GET.get('timezone', 'Asia/Kolkata')
        tz = timezone(user_tz)
        data = []
        for cls in FitnessClass.objects.all():
            data.append({
                "id": cls.id,
                "name": cls.name,
                "date_time": cls.date_time.astimezone(tz).strftime("%Y-%m-%dT%H:%M:%S"),
                "instructor": cls.instructor,
                "available_slots": cls.available_slots
            })
        return JsonResponse(data, safe=False)





@csrf_exempt
def post_book_class(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            class_id = body.get('class_id')
            client_name = body.get('client_name')
            client_email = body.get('client_email')

            if not (class_id and client_name and client_email):
                return JsonResponse({'error': 'All fields are required'}, status=400)

            try:
                fitness_class = FitnessClass.objects.get(id=class_id)
            except FitnessClass.DoesNotExist:
                return JsonResponse({'error': 'Class not found'}, status=404)

            if fitness_class.available_slots <= 0:
                return JsonResponse({'error': 'No slots available'}, status=400)

            booking = Booking.objects.create(
                fitness_class=fitness_class,
                client_name=client_name,
                client_email=client_email
            )

            fitness_class.available_slots -= 1
            fitness_class.save()

            logger.info(f"Booking successful: {client_name} for class {class_id}. Remaining slots: {fitness_class.available_slots}")
            return JsonResponse({
                'message': 'Booking successful',
                'remaining_slots': fitness_class.available_slots
            })

        except json.JSONDecodeError:
            return 
        
        
@csrf_exempt
def get_bookings(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        bookings = Booking.objects.filter(client_email=email)
        if not bookings.exists():
            return JsonResponse({'message': 'No bookings found for this email'}, status=404)

        data = [
            {
                "class_name": b.fitness_class.name,
                "date_time": localtime(b.fitness_class.date_time).strftime("%Y-%m-%dT%H:%M:%S"),
                "instructor": b.fitness_class.instructor,
                "client_name": b.client_name,
                "client_email": b.client_email,
            } for b in bookings
        ]
        return JsonResponse({'bookings': data}, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
