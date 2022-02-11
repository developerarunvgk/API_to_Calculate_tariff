#API to calculate tariff based on data from file :  File is given via email

#Input :  Json String

#Method:  Calculate tariff based on input that is given by user and display output json string

#Language Used:Python

#Technologies Used: 1.) Pandas to parse data  2.) Tornado WebFramework to Expose data to public via API 3.)pytest to automate test cases

#Output:  Json String

#Time Taken for Development : 3.5-4 hours. Development took around 2-2.5 hours,Test Cases and Documentation took rest

How to run the API & Automated TestCases
----------------------------------------
1.Download the git by using command git clone https://github.com/developerarunvgk/API_Calculate_tariff.git

2.Ensure that python3 and pip3 are installed

3.Go to the extracted folder in the Directory and install the requirements using command pip3 install  -r requirements.txt or use pip install  -r requirements.txt

4.Open the terminal in folder where git is downloaded(or use cd command to go to file path) and Start the API using python3 api_calculate_tariff.py or python api_calculate_tariff.py to expose API to public and leave that terminal.

5.As you are using localhost , go to web-browser and test it using API
127.0.0.1:8888/gettariff?n=JSON_INPUT
ex:127.0.0.1:8888/gettariff?n={"zip_code":10555,"city":"Nellischeid","street":"Torstraße","house_number":26,"yearly_kwh_consumption":1000}
output:{"unit_price": 1.66, "grid_fees": 3.99, "kwh_price": 0.58, "total_price": 585.65}

Refer Screenshot_Output for the Result outputs

6.Open a new terminal and Run Test-cases featuring various scenarios and see the expected output.All Test-cases are passed
Run the test case using python3 -m pytest pytest_for_api.py -v
Code is tested in both Windows and Linux Machines
THose eleven Test cases will require around 20 seconds to finish

7.Code is documented so it is legible to read

----------------------
Sample Ouput 
----------------------
See Screenshot_Output folder to see the result that i got when i executed the the program.

Deployment(Out of Scope of the question.But done for interest)
---------------
I have deployed this code in aws and tested the working in Cloud Instances.Refer Screenshot_Output Folder 
(It is out of scope of this question and is done as part of interest)


Possible Improvements
----------------
1.We could use AWS fargate for deployment so that it scales up and scales down with user traffic

2.We could use AWS Lambda for deployment.We could have tmp folder of aws lambda (with size of 512MB) taking data from s3 whenever new aws lambda instance are created or used Container based deployments in lambda if file size becomes an issue

3.We could use AWS Lambda accessing AWS RDBMS(after loading csv content to db).In that case size is not a concern


Alternative Methods
--------------------
1.)Instead of Pandas,we could have used AWS RDBMS by loading data from csv intially.

2.)We could use VAEX library of Python to process large data instead of pandas if we consider memory as limitation.It can process heavy datasets very easily in low Memory systems
