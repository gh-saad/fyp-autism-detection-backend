from rest_framework import viewsets
from .models import Consultant, Slot, Appointments
from .serializers import ConsultantSerializer, SlotSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView


class ConsultantViewSet(viewsets.ModelViewSet):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer


class ConsultantWithSlotsView(APIView):
    def get(self, request):
        consultants = Consultant.objects.all()
        data = []
        for consultant in consultants:
            slots = Slot.objects.filter(consultant_id=consultant.id, is_booked=False)
            slot_serializer = SlotSerializer(slots, many=True)
            consultant_serializer = ConsultantSerializer(consultant)
            consultant_data = consultant_serializer.data
            consultant_data['slots'] = slot_serializer.data if slots.exists() else []
            data.append(consultant_data)
        return Response(data, status=status.HTTP_200_OK)


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get_queryset(self):
        consultant_id = self.request.query_params.get('consultant_id')
        if consultant_id:
            return Slot.objects.filter(consultant_id=consultant_id)
        return Slot.objects.all()


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        consultant_id = self.request.query_params.get('consultant_id')
        patient_id = self.request.query_params.get('patient_id')
        queryset = Appointments.objects.all()
        if consultant_id:
            queryset = queryset.filter(consultant_id=consultant_id)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def book(self, request):
        consultant_id = request.data.get('consultant_id')
        patient_id = request.data.get('patient_id')
        slot_id = request.data.get('slot_id')

        if not (consultant_id and patient_id and slot_id):
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot = Slot.objects.get(id=slot_id, consultant_id=consultant_id)
        except Slot.DoesNotExist:
            return Response({'error': 'Slot not found.'}, status=status.HTTP_404_NOT_FOUND)

        if slot.is_booked:
            return Response({'error': 'Slot already booked.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment = Appointments.objects.create(
            consultant_id_id=consultant_id,
            patient_id_id=patient_id,
            slot_id_id=slot_id
        )
        slot.is_booked = True
        slot.save()

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)