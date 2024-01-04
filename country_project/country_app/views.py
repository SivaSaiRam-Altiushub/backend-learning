from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import CustomUser
from .serializers import *
from .permissions import IsCountryMyUser, IsStateMyUser, IsCityMyUser
from django.core.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from django.db.models import Prefetch


# class CountryListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = CountrySerializer
#     # authentication_classes = [TokenAuthentication, BasicAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Country.objects.filter(my_user=self.request.user)
    
#     def perform_create(self, serializer):
#         data = self.request.data
#         states_data = data.pop('states')
#         country = Country.objects.create(**data, my_user = self.request.user)
#         country.save()
#         for state_data in states_data:
#             cities_data = state_data.pop('cities')
#             state = State.objects.create(**state_data, country=country)
#             for city_data in cities_data:
#                 City.objects.create(state=state, **city_data)
#         return country

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         countries_data = serializer.data
#         temp = []
#         for country_data in countries_data:
#             states_data = StateSerializer(State.objects.filter(country__id=country_data['id']), many=True).data
#             for state_data in states_data:
#                 cities_data = CitySerializer(City.objects.filter(state__id=state_data['id']), many=True).data
#                 state_data["cities"] = cities_data
#             country_data["states"] = state_data
#             temp.append(country_data)
#         return Response(temp)

# class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CountrySerializer
#     queryset = Country.objects.all()
#     permission_classes = [IsCountryMyUser]

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
    
#     def perform_update(self, serializer):
#         serializer.save()

#     def perform_destroy(self, instance):
#         instance.delete()

class CountryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(my_user=self.request.user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            country = serializer.save(my_user=self.request.user)
            states_data = self.request.data.pop('states')
            states = []
            cities = []
            for state_data in states_data:
                cities_data = state_data.pop('cities', [])

                state = State(country=country, **state_data)
                states.append(state)

                for city_data in cities_data:
                    cities.append(City(state=state, **city_data))

            State.objects.bulk_create(states)
            City.objects.bulk_create(cities)

    # def perform_update(self, serializer):
    #     import pdb;pdb.set_trace()
        # instance.name = validated_data.get('name', instance.name)
        # instance.country_code = validated_data.get('country_code', instance.country_code)
        # instance.curr_symbol = validated_data.get('curr_symbol', instance.curr_symbol)
        # instance.phone_code = validated_data.get('phone_code', instance.phone_code)
        # instance.is_active = validated_data.get('is_active', instance.is_active)
        # instance.save()

        # instance.states.all().delete()

        # states_data = validated_data.get('states', [])
        # new_states = []

        # for state_data in states_data:
        #     cities_data = state_data.pop('cities', [])

        #     state = State(country=instance, **state_data)
        #     new_states.append(state)

        #     new_cities = [City(state=state, **city_data) for city_data in cities_data]
        #     City.objects.bulk_create(new_cities)

        # State.objects.bulk_create(new_states)

        # return instance

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        countries_data = serializer.data
        temp = []
        for country_data in countries_data:
            states_data = StateSerializer(State.objects.filter(country__id=country_data['id']), many=True).data
            country_data["states"] = []
            for state_data in states_data:
                cities_data = CitySerializer(City.objects.filter(state__id=state_data['id']), many=True).data
                state_data["cities"] = cities_data
                country_data["states"].append(state_data)
            temp.append(country_data)
        return Response(temp)

class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [IsCountryMyUser]

    def retrieve(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        country_data = serializer.data
        states_data = StateSerializer(State.objects.filter(country__id=country_data['id']), many=True).data
        country_data["states"] = []
        for state_data in states_data:
            cities_data = CitySerializer(City.objects.filter(state__id=state_data['id']), many=True).data
            state_data["cities"] = cities_data
            country_data["states"].append(state_data)
        return Response(country_data)
    
    def perform_destroy(self, instance):
        instance.delete()

class StateListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        return State.objects.filter(country__my_user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()

class StateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = [IsStateMyUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class CityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(state__country__my_user=self.request.user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            data = serializer.validated_data
            if data['num_of_adult_males']+data['num_of_adult_females'] < data['population']:
                serializer.save()
            else:
                raise ValidationError('Summation of Male and Female population should be less than Total Population')

class CityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [IsCityMyUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CursorPagination
    permission_classes = [permissions.AllowAny]

class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserSignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        if Token.objects.filter(key=request.headers['Authorization']).exists():
            user = Token.objects.get(key=request.headers['Authorization']).user
            response = {}
            response['user_id'] = user.id
            response['email'] = user.email
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error':"Token Not Found"}, status=status.HTTP_400_BAD_REQUEST)

class UserSignOutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Successfully signed out."}, status=status.HTTP_200_OK)
