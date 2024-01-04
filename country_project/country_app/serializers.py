# myapp/serializers.py
from rest_framework import serializers
from .models import *
from django.db import transaction

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    my_state__name = serializers.CharField(source='get_my_state_name', read_only=True)

    def get_my_state_name(self, state):
        return state.state.name
    
    def validate(self, data):
        state = self.context['state']
        city_name = data.get('name')
        existing_cities = City.objects.filter(state=state, name=city_name)
        if self.instance:
            existing_cities = existing_cities.exclude(id=self.instance.id)

        if existing_cities.exists():
            raise serializers.ValidationError(f'This city already exists in the state {state.name}')

        return data

    class Meta:
        model = City
        fields = '__all__'
        # fields += ['my_state_name']


class StateSerializer(serializers.ModelSerializer):
    my_country__name = serializers.CharField(source='get_my_country_name', read_only=True)
    my_country__my_user__name = serializers.CharField(source='get_my_country_my_user_name', read_only=True)

    cities = CitySerializer(many=True, read_only=True)

    def get_my_country_name(self, state):
        return state.country.name
    
    def get_my_country_my_user_name(self, state):
        return state.country.my_user.email
    
    def validate(self, data):
        country = self.context['country']
        state_name = data.get('name')
        existing_states = State.objects.filter(country=country, name=state_name)
        if self.instance:
            existing_states = existing_states.exclude(id=self.instance.id)

        if existing_states.exists():
            raise serializers.ValidationError(f'This state already exists in the country {country.name}')

        return data

    class Meta:
        model = State
        fields = '__all__'
        # fields += ['my_country__name', 'my_country__my_user__name']


class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    # @transaction.atomic
    # def create(self, validated_data):
    #     states_data = validated_data.pop('states')
    #     country = Country.objects.create(**validated_data)

    #     states = []
    #     cities = []

    #     for state_data in states_data:
    #         cities_data = state_data.pop('cities', [])

    #         state = State(country=country, **state_data)
    #         states.append(state)

    #         for city_data in cities_data:
    #             cities.append(City(state=state, **city_data))

    #     State.objects.bulk_create(states)
    #     City.objects.bulk_create(cities)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.curr_symbol = validated_data.get('curr_symbol', instance.curr_symbol)
        instance.phone_code = validated_data.get('phone_code', instance.phone_code)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        State.objects.filter(country=instance).delete()
        City.objects.filter(state__country=instance).delete()

        states_data = self.initial_data.get('states', [])
        new_states = []

        for state_data in states_data:
            cities_data = state_data.pop('cities', [])

            state = State(country=instance, **state_data)
            new_states.append(state)

            new_cities = [City(state=state, **city_data) for city_data in cities_data]
            City.objects.bulk_create(new_cities)

        State.objects.bulk_create(new_states)

        return instance
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code', 'states']

