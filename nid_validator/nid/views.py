from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .EgyptianNationalIdValidator import EgyptianNationalIdValidator

class NationalIdValidatorAPIView(APIView):
    def get(self, request, id: str):
        try:
            validator = EgyptianNationalIdValidator(id)
        except ValueError:
            return Response({'error': 'Invalid National Id'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(validator.data, status=status.HTTP_200_OK)
