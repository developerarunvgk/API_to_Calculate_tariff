import pytest
import requests,json


def function_to_call_api(input_data):
    url_to_call='http://127.0.0.1:8888/gettariff?n='+json.dumps(input_data);
    print(url_to_call)
    response=requests.get(url_to_call);
    try:
        rs=json.loads(response.text);
        return rs;

    except Exception as e:
        return response.text
    

def test_basic_test():
    #Basic Test case Given in question
	rs=function_to_call_api({"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":25,"yearly_kwh_consumption":1000})
	assert rs == {"unit_price": 1.66, "grid_fees": 3.99, "kwh_price": 0.58, "total_price": 585.65}
    
def test_basic_test_1():
    #basic test based on random data in CSV
	rs=function_to_call_api({"zip_code":46221,"city":"Ost Nataliescheid","street":"Hallesche Str.","house_number":55,"yearly_kwh_consumption":1000})
	assert rs == {"unit_price": 2.82, "grid_fees": 0.21, "kwh_price": 0.42, "total_price": 423.03}

def test_Test_case_for_invalid_data():
    #Input data is modified in such a way that it is not present in CSV
	rs=function_to_call_api({"zip_code":189471,"city":"Hambug","street":"Auf dem Weierberg","house_number":44,"yearly_kwh_consumption":1000,"superstar":"Rajini"})
	assert rs == '''Details are not in DB.Area is not servicable. Kindly check the details once again'''

def test_Test_case_for_households_satisfying_multiple_rows():
    #Important Test Case.Below Input matches two rows in the CSV data store.So Average of output is calculated
	rs=function_to_call_api({"zip_code":18947,"city":"Hambug","street":"Auf dem Weierberg","house_number":44,"yearly_kwh_consumption":1000,"superstar":"Rajini"})
	assert rs == {"unit_price": 2.085, "grid_fees": 4.89, "kwh_price": 0.29000000000000004, "total_price": 296.9750000000001}

def test_Test_case_for_households_satisfying_multiple_rows_1():
    #Important Test Case.Below Input matches two rows in the CSV data store.So Average of output is calculated
	rs=function_to_call_api({"zip_code":46835,"city":"Felinaburg","street":"Schöneberger Str.","house_number":496,"yearly_kwh_consumption":1000})
	assert rs == {"unit_price": 1.71, "grid_fees": 3.3, "kwh_price": 0.49, "total_price": 495.01}
    
def test_Test_case_for_random_input():
    #A string input is given for n=value
	rs=function_to_call_api('some random data other than json')
	assert rs == '''Ensure your input has zip , postal_code,city,street and house number'''

def test_Test_case_for_random_input_1():
    #A integer input is given for n=value
	rs=function_to_call_api(5)
	assert rs == '''Ensure your input has zip , postal_code,city,street and house number'''

def test_Test_case_for_random_input_2():
    #A integer input is given for n=value
	kk=[]
	rs=function_to_call_api({"zip_code":kk,"city":"Nellischeid","street":"Torstraße","house_number":26,"yearly_kwh_consumption":1000})
	assert rs == '''Ensure your input has zip , postal_code,city,street and house number'''

def test_Test_case_for_invalid_household():
    #Test_case_for_invalid_household
	rs=function_to_call_api({"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":-26,"yearly_kwh_consumption":1000})
	assert rs == '''House is invalid'''

def test_Test_case_for_invalid_household_1():
    #Test_case_for_invalid_household
	rs=function_to_call_api({"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":960,"yearly_kwh_consumption":1000})
	assert rs == '''House is invalid'''

def test_Test_case_for_string_in_house_hold():
    #When string is given in household that cannot be casted
	rs=function_to_call_api({"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":"abcd","yearly_kwh_consumption":1000})
	assert rs == '''Ensure your input has zip , postal_code,city,street and house number'''
    
#function_to_call_api({"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":26,"yearly_kwh_consumption":1000});
#JSON Issue : try using a proper JSON