from rest_framework.response import Response
from rest_framework.views import APIView
from api.fingerprint.serializers import FingerPrintRequestSerializer
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from api.fingerprint.examples import EXAMPLE_REQUEST


class FingerPrint(APIView):
    serializer_class = FingerPrintRequestSerializer

    def get(self, request):
        return Response(
            {
                "fingerprint": "qwjkkqw",
            }
        )

    @extend_schema(
        examples=[
            OpenApiExample(name="Example", value=EXAMPLE_REQUEST, request_only=True)
        ]
    )
    def post(self, request):
        requestSerializer = FingerPrintRequestSerializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)
        smiles = requestSerializer.validated_data["smiles"]
        degree = requestSerializer.validated_data["degree"]
        print(smiles)
        print(degree)
        return Response({"smile": smiles, "degree": degree})
