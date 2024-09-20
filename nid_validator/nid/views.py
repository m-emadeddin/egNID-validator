from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .EgyptianNationalIdValidator import EgyptianNationalIdValidator
from .serializers import NationalIdValidatorSerializer


class NationalIdValidatorAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Validate and extract data from an Egyptian National ID",
        responses={200: NationalIdValidatorSerializer(many=False), 400: 'Invalid National ID'},
    )
        
        
    def get(self, request, id: str):
        try:
            validator = EgyptianNationalIdValidator(id)
        except ValueError:
            return Response({'error': 'Invalid National Id'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(validator.data, status=status.HTTP_200_OK)
