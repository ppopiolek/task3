import unittest
from project.customers.models import Customer

#testy poprawnych danych

class TestCustomerValidData(unittest.TestCase):
    def test_valid_data_complete(self):
        Customer(name="Anna Kowalska", city="Poznań", age=40, pesel="85050512345", street="Polna", appNo="23A")

    def test_valid_pesel_formats(self):
        valid_pesels = ["99010112345", "91020212345", "81111112345"]
        for pesel in valid_pesels:
            Customer(name="Jan Nowak", city="Gdańsk", age=35, pesel=pesel, street="Długa", appNo="5")

    def test_valid_complex_name(self):
        names = ["Anna-Maria Wąsowska", "Jan Krzysztof Rakoczy", "Ola Kowalska-Lewandowska"]
        for name in names:
            Customer(name=name, city="Bydgoszcz", age=36, pesel="87030312345", street="Leśna", appNo="17")

    def test_valid_complex_street(self):
        streets = ["ul. Jana Pawła II", "al. Jerozolimskie", "pl. Konstytucji"]
        for street in streets:
            Customer(name="Tomasz Nowak", city="Sopot", age=39, pesel="84121212345", street=street, appNo="13")


#testy niepoprawnych danych

class TestCustomerInvalidData(unittest.TestCase):
    def test_invalid_appNo_format(self):
        with self.assertRaises(ValueError):
            Customer(name="Krzysztof Jarzyna", city="Szczecin", age=50, pesel="77070712345", street="Morska", appNo="123AB$")

    def test_negative_age(self):
        with self.assertRaises(ValueError):
            Customer(name="Ewa Malinowska", city="Wrocław", age=-25, pesel="66060612345", street="Kwiatowa", appNo="6")
            
    def test_extremely_short_city_name(self):
        with self.assertRaises(ValueError):
            Customer(name="Monika Zielonka", city="A", age=34, pesel="85101012345", street="Parkowa", appNo="15")

    def test_invalid_pesel_characters(self):
        invalid_pesels = ["abcdefghijk", "1234!67890x", "0000000000?"]
        for pesel in invalid_pesels:
            with self.assertRaises(ValueError):
                Customer(name="Robert Lewandowski", city="Gdynia", age=31, pesel=pesel, street="Sportowa", appNo="11")

    def test_invalid_email_as_name(self):
        with self.assertRaises(ValueError):
            Customer(name="jan.kowalski@email.com", city="Kraków", age=30, pesel="85090912345", street="Main", appNo="1")



#testy wstrzyknięć

class TestCustomerSQLAndJavaScriptInjections(unittest.TestCase):
    def test_extended_sql_injection(self):
        attack_vectors = ["' OR '1'='1'; --", "' UNION SELECT * FROM users; --"]
        for vector in attack_vectors:
            with self.assertRaises(ValueError):
                Customer(name=vector, city="Kraków", age=28, pesel="88080812345", street="Zakopiańska", appNo="7")

    def test_javascript_injection_variants(self):
        scripts = ["<script>alert('XSS')</script>", "<script>console.log('Hack')</script>"]
        for script in scripts:
            with self.assertRaises(ValueError):
                Customer(name="Piotr Wiśniewski", city=script, age=30, pesel="92020212345", street="Ogrodowa", appNo="8")

#testy ekstremalnych danych

class TestCustomerExtremeData(unittest.TestCase):
    def test_extremely_long_street_name(self):
        with self.assertRaises(ValueError):
            Customer(name="Marcin Kowal", city="Lublin", age=27, pesel="90010112345", street="a" * 1000, appNo="9")

    def test_excessive_appNo_number(self):
        with self.assertRaises(ValueError):
            Customer(name="Dorota Białek", city="Kielce", age=22, pesel="97070712345", street="Słoneczna", appNo="1000000000000000")


if __name__ == '__main__':
    unittest.main()
