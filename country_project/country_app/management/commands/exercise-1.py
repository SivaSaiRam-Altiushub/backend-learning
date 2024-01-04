from country_app.models import *
from django.db.models import Q


# 1 - Creation for Single Instance

country_data = {"name":"India", "country_code":"IND", "curr_symbol":"IND-SYMBOL", "phone_code":"+91"}
state_data = {"name":"Andhra Pradesh", "state_code":"AP", "gst_code":"GST-AP", "country_id":1}
city_data = {"name":"Guntur", "city_code":"GNT", "phone_code":"GNT-PHN", "population":10000, "avg_age":65.5, "num_of_adult_males":5000, "num_of_adult_females":5000, "state_id":1}

try:
    country_obj, is_created = Country.objects.get_or_create(**country_data)
except Exception as e:
    print(e)


try:
    state_obj, is_created = State.objects.get_or_create(**state_data)
except Exception as e:
    print(e)

try:
    city_obj, is_created = City.objects.get_or_create(**city_data)
except Exception as e:
    print(e)

# 2 - Creation for Multiple Instances
    
country_data = [{"name":"America", "country_code":"USA", "curr_symbol":"USA-SYMBOL", "phone_code":"+1"},
                {"name":"South Africa", "country_code":"RSA", "curr_symbol":"RSA-SYMBOL", "phone_code":"+2"}]
state_data = [{"name":"California", "state_code":"CAL", "gst_code":"GST-CAL", "country_id":2},
              {"name":"Cape Town", "state_code":"CT", "gst_code":"GST-CT", "country_id":3}]
city_data = [{"name":"Los Angels", "city_code":"LA", "phone_code":"LA-PHN", "population":10000, "avg_age":65.5, "num_of_adult_males":5000, "num_of_adult_females":5000, "state_id":2},
             {"name":"Some City", "city_code":"ST", "phone_code":"ST-PHN", "population":10000, "avg_age":65.5, "num_of_adult_males":5000, "num_of_adult_females":5000, "state_id":3}]

try:
    countries = Country.objects.bulk_create([Country(**data) for data in country_data])
except Exception as e:
    print(e)

try:
    states = State.objects.bulk_create([State(**data) for data in state_data])
except Exception as e:
    print(e)

try:
    cities = City.objects.bulk_create([City(**data) for data in city_data])
except Exception as e:
    print(e)

# 3 - Bulk Update
    
Country.objects.filter(name__startswith='A').update(is_active=False)
State.objects.filter(name__startswith='A').update(is_active=False)
City.objects.filter(name__startswith='A').update(is_active=False)

# 4 - Fetch All

country_set = Country.objects.all()
state_set = State.objects.all()
city_set = City.objects.all()

# 5 - Fetch All Cities of a State
state = 'California'
cities_of_state = City.objects.filter(state__name=state)

# 6 - Fetch All States of a Country
country = 'India'
states_of_country = State.objects.filter(country__name=country)

# 7 - Fetch All Cities of a country
country = 'America'
cities_of_country = City.objects.filter(state__country__name=country)


# 8 - City of a Country with Minimum and Maximum Population
country = 'South Africa'

min_population_city = City.objects.filter(state__country__name=country).order_by('population').first()
max_population_city = City.objects.filter(state__country__name=country).order_by('-population').first()


# # Type Dict Generic Implementation

from typing import Type, TypeVar, Union, List, Dict

T = TypeVar('T')

class TypeDict:
    def __init__(self, data: Union[Dict[str, Type[T]], Type[T]]):
        self.data = data

    def get_type(self, key: str) -> Type[T]:
        if isinstance(self.data, dict):
            return self.data.get(key, Any)
        else:
            return self.data
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# For Class and Dict
person_type_dict = TypeDict({'name': str, 'age': int})
person_instance = Person(name="John", age=30)


name_type: Type[str] = person_type_dict.get_type('name')
age_type: Type[int] = person_type_dict.get_type('age')

# For List
list_type_dict = TypeDict(List[int])
list_instance = [1, 2, 3]


list_element_type: Type[int] = list_type_dict.get_type('')

# For Primitive Types
int_type_dict = TypeDict(int)
float_type_dict = TypeDict(float)


int_value: Type[int] = int_type_dict.get_type('')
float_value: Type[float] = float_type_dict.get_type('')

# For Function
def add_numbers(x: int, y: int) -> int:
    return x + y

add_numbers_type_dict = TypeDict(add_numbers)


x_type: Type[int] = add_numbers_type_dict.get_type('x')
y_type: Type[int] = add_numbers_type_dict.get_type('y')
return_type: Type[int] = add_numbers_type_dict.get_type('')

