import tornado.ioloop
import tornado.web
import logging
import time
from tornado import gen
import pandas as pd
import json
from statistics import mean



class gettariff(tornado.web.RequestHandler):
    def calculate_tariff(self,input_data={}):
        reader = pd.read_csv("location_prices.csv",low_memory=False)
        #Cleansing Data
        reader=reader.drop_duplicates()
        #'''Above statement  removes line level duplicates.Below statement removes null statement from 'postal_code','city','street','house_number' from the csv file'''
        reader=reader.dropna(subset=['postal_code','city','street','house_number'])
        #Checking input recieved and validating it 
        if(type(input_data)!="dict"):
            if(isinstance(input_data, str)):
                input_data=input_data.replace("'",'"');#Tries to resolve error in single quote error JSON by replacing ' by "
                
            try:
                input_data = json.loads(input_data)#Trying to detect convert the string recieved from GET to JSON Object for easy calculation
            except Exception as e:
                #print(str(e))
                return "JSON Issue : try using a proper JSON"
        try:#Fetching data from csv file based on input 
            data_selected = reader[(reader['postal_code']==int(input_data['zip_code'])) & (reader['city']==input_data['city']) & (reader['street']==input_data['street'])]
            house_number=int(input_data['house_number'])
        except Exception as e:
            #print(str(e))
            return "Ensure your input has zip , postal_code,city,street and house number"
            
        if(data_selected.empty):#Checking whether input recieved is available in CSV.In case it is not there return is raised
            #print("Details are not in DB.Area is not servicable. Kindly check the details once again")
            return "Details are not in DB.Area is not servicable. Kindly check the details once again"
        
        unit_price_list=[]
        grid_fees_list=[]
        kwh_price_list=[]
        total_price_list=[]
        house_validation=False
        #Iterating through selected input , and validating house number is present here
        #In case house number is present across multiple rows,then average of computed costs need to be found.
        #For that average of prices and total_price is calculated
        for index, row in data_selected.iterrows():
            #print (row["postal_code"], row["city"], row["street"],row["unit_price"],row["grid_fees"], row["kwh_price"],row["house_number"])
            upper_lower_limit=row["house_number"].split('-');
            try:
                if (house_number>=int(upper_lower_limit[0]) and house_number<=int(upper_lower_limit[1])):
                    house_validation=True;
                    unit_price_list.append(row["unit_price"])
                    grid_fees_list.append(row['grid_fees'])
                    kwh_price_list.append(row['kwh_price'])
                    total_price_list.append(row["unit_price"]+row['grid_fees']+(input_data["yearly_kwh_consumption"]*row['kwh_price']))            
                    #print("Above valid for calculation");
            except Exception as e:
                return "Some Exception Occured"
    
        if house_validation:    
            unit_price=mean(unit_price_list);
            grid_fees=mean(grid_fees_list);
            kwh_price=mean(kwh_price_list);
            total_price_1=mean(total_price_list);
            total_price=unit_price+grid_fees+(input_data["yearly_kwh_consumption"]*kwh_price)
        else:
            #print(" House is not servicable")
            return "House is invalid"

            
        #print(total_price)
        output_json={}
        output_json["unit_price"]=unit_price;
        output_json["grid_fees"]=grid_fees;
        output_json["kwh_price"]=kwh_price;
        output_json["total_price"]=total_price;
        return(output_json);
        #print(total_price_1);


    def get(self):
        #Get method of python is called by tornado 
        n=self.get_argument("n", None, True)
        result=self.calculate_tariff(n);
        self.write(result)        


def make_app():
    return tornado.web.Application([
          (r"/gettariff",gettariff)#API Routing happening here

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)#Exposing Port to Public
    print('''Server Started listening at port 8888 ''')
    print('''1.) If you want to call API,Call api from browser[GET Request] with n beign user input,ex: http://127.0.0.1:8888/gettariff?n={"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":26,"yearly_kwh_consumption":1000}''')
    print('''2.) If you want to run test cases , open new prompt and run python3 -m pytest pytest_for_api.py -v or python -m pytest pytest_for_api.py -v''')
    tornado.ioloop.IOLoop.current().start()

