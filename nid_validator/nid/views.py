from django.shortcuts import render
from django.http import JsonResponse
from .EgyptianNationalIdValidator import EgyptianNationalIdValidator 

def index(request, id: str) -> JsonResponse:
    """
    Validate the national ID and return a JSON response.
    """
        
    try:
        national_id: EgyptianNationalIdValidator = EgyptianNationalIdValidator(id)
    except:
        return JsonResponse({'error': 'Invalid National Id'}, status=400)

    return JsonResponse(national_id.data)