from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import localtime, make_aware, is_naive
from django.utils.dateparse import parse_datetime
from django.db import transaction
import json
import logging
from .models import FitnessClass, Booking

logger = logging.getLogger(__name__)

 
@csrf_exempt
def classes_view(request):
    if request.method == 'GET':
        data = []
        for cls in FitnessClass.objects.all():
            local_dt = localtime(cls.date_time)
            data.append({
                "id": cls.id,
                "name": cls.name,
                "date_time": local_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "instructor": cls.instructor,
                "available_slots": cls.available_slots
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body.get('name')
            date_time = body.get('date_time')
            instructor = body.get('instructor')
            available_slots = body.get('available_slots')

            if not (name and date_time and instructor and available_slots):
                return JsonResponse({'error': 'All fields are required'}, status=400)

            dt = parse_datetime(date_time)
            if dt is None:
                return JsonResponse({'error': 'Invalid date_time format'}, status=400)

            if is_naive(dt):
                dt = make_aware(dt)

            fitness_class = FitnessClass.objects.create(
                name=name,
                date_time=dt,
                instructor=instructor,
                available_slots=available_slots
            )

            local_dt = localtime(fitness_class.date_time)
            return JsonResponse({
                "id": fitness_class.id,
                "name": fitness_class.name,
                "date_time": local_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "instructor": fitness_class.instructor,
                "available_slots": fitness_class.available_slots
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


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
                with transaction.atomic():
                    fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)

                    if fitness_class.available_slots <= 0:
                        return JsonResponse({'error': 'No slots available'}, status=400)

                    Booking.objects.create(
                        fitness_class=fitness_class,
                        client_name=client_name,
                        client_email=client_email
                    )

                    FitnessClass.objects.filter(id=class_id).update(
                        available_slots=fitness_class.available_slots - 1
                    )

                    fitness_class.refresh_from_db()

            except FitnessClass.DoesNotExist:
                return JsonResponse({'error': 'Class not found'}, status=404)

            logger.info(f"Booking successful: {client_name} for class {class_id}. Remaining slots: {fitness_class.available_slots}")

            return JsonResponse({
                'message': 'Booking successful',
                'remaining_slots': fitness_class.available_slots,
                'posted_data': {
                    'class_id': class_id,
                    'client_name': client_name,
                    'client_email': client_email
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_bookings(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

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
        return JsonResponse({'bookings': data}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
