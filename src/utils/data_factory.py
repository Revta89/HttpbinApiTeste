from faker import Faker
import random
import string
import uuid
from typing import Dict, Any, Optional

fake = Faker()


class DataFactory:
    """Test data generator with more utilities"""

    @staticmethod
    def generate_headers(custom_headers: Optional[Dict] = None) -> Dict[str, str]:
        """Generate random headers"""
        base_headers = {
            'X-Request-ID': str(uuid.uuid4()),
            'X-Test-Run': f'test-{fake.word()}',
            'User-Agent': fake.user_agent()
        }

        if custom_headers:
            base_headers.update(custom_headers)

        return base_headers

    @staticmethod
    def generate_user_data(include_address: bool = True) -> Dict[str, Any]:
        """Generate comprehensive user data"""
        user_data = {
            'id': fake.random_int(min=1, max=1000),
            'name': fake.name(),
            'email': fake.email(),
            'username': fake.user_name(),
            'phone': fake.phone_number(),
            'date_joined': fake.iso8601()
        }

        if include_address:
            user_data['address'] = {
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'zipcode': fake.zipcode(),
                'country': fake.country()
            }
        return user_data

    @staticmethod
    def generate_random_string(length: Optional[int] = None, charset: str = string.ascii_letters + string.digits) -> str:
        """Generate random string with custom charset"""
        if length is None:
            length = random.randint(4, 20)
        return ''.join(random.choices(charset, k=length))

    @staticmethod
    def generate_json_payload(
            num_fields: int = 5,
            nested: bool = False
    ) -> Dict[str, Any]:
        """Generate random JSON payload"""
        payload = {}
        field_types = ['string', 'number', 'boolean', 'null']

        for i in range(num_fields):
            field_name = f"field_{i + 1}"
            field_type = random.choice(field_types)

            if field_type == 'string':
                payload[field_name] = fake.word()
            elif field_type == 'number':
                payload[field_name] = random.randint(1, 1000)
            elif field_type == 'boolean':
                payload[field_name] = random.choice([True, False])
            else:
                payload[field_name] = None

        if nested and num_fields > 2:
            # Create a nested object
            payload['nested_data'] = DataFactory.generate_json_payload(
                num_fields=3,
                nested=False
            )

        return payload

    @staticmethod
    def generate_query_params(num_params: int = 3) -> Dict[str, str]:
        """Generate random query parameters"""
        params = {}
        for i in range(num_params):
            params[f"param_{i + 1}"] = DataFactory.generate_random_string(
                length=random.randint(3, 10)
            )
        return params


data_generator = DataFactory()