from faker import Faker

class DatagenFaker(Faker):
    def __init__(self):
        super().__init__("tr_TR")

    def phone_number(self) -> str:
        return self.numerify("+905$#$######")

    def card_type(self) -> str:
        return self.random_choices(elements=['visa', 'mastercard'], length=1)[0]

    def status(self) -> str:
        return self.random_choices(elements=['active', 'inactive'], length=1)[0]

    def gender(self) -> str:
        return self.random_choices(elements=['male', 'female'], length=1)[0]

    def role(self) -> str:
        return self.random_choices(elements=['hr', 'admin', 'flight_planner', 'passenger_services', 'ground_services'], length=1)[0]

    def flight_status(self) -> str:
        return self.random_choices(elements=['scheduled', 'delayed', 'cancelled', 'departed', 'arrived'], length=1)[0]

    def meal(self) -> str:
        return self.random_choices(elements=['standard', 'vegetarian', 'vegan', 'halal', 'kosher'], length=1)[0]

    def fare_type(self) -> str:
        return self.random_choices(elements=['economy', 'business', 'first'], length=1)[0]

    def position(self) -> str:
        return self.job()

    def birth_date(self) -> str:
        return self.date_time_between(start_date='-100y', end_date='-18y')

    def hire_date(self) -> str:
        return self.date_time_between(start_date='-2y', end_date='now')

    def seat_number(self) -> int:
        return self.random_int(min=1, max=300)
    
    def baggage_allowance(self) -> int:
        return self.random_int(min=0, max=30)

    def baggage_id(self) -> str:
        return self.bothify(text='BAG#####KG')

    def extra_baggage(self) -> int:
        return self.random_int(min=0, max=2)
    
    def pnr(self) -> str:
        return self.bothify(text='??????')
    
    def salary(self) -> float:
        return self.random_int(30000, 150000)

    def employee_id(self) -> str:
        return self.bothify(text='EMP####')
        
    def flight_id(self) -> str:
        return self.random_int(1, 1000)

    def payment_id(self) -> str:
        return self.random_int(1, 1000)

    def gate_number(self) -> str:
        return self.bothify("??##", letters="ABCD")

    def plane_registration(self) -> str:
        return self.bothify("TC-???").upper()

    def flight_price(self) -> int:
        return self.random_int(100, 2000)

    def flight_number(self) -> str:
        registration = self.random_choices(elements=['TK', 'PC', 'XQ', 'CJ'], length=1)[0]
        return self.numerify(f"{registration}-####")

    def iata(self, exclude=[]) -> str:
        return self.random_choices(elements=set(['IST', 'SAW', 'ESB', 'AYT', 'ADB']) - set(exclude), length=1)[0]
