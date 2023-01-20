from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CharField, IntegerField


class FingerPrintRequestSerializer(Serializer):
    smiles = CharField(required=True)
    degree = IntegerField(required=True)
