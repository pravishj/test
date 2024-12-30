import requests
import re
import json

# Define the login URL and the credentials
base_url = "https://myaccount.esbnetworks.ie/MicrosoftIdentity/Account/SignIn"  # Replace with the actual login endpoint
login_url = "https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/SelfAsserted?tx="
username = "EMAIL"  # Replace with your username
password = "PASSWORD"  # Replace with your password

# Create a session to persist cookies and headers
session = requests.Session()
print("-" * 10)

# Fetch the login page to get any required tokens (if needed)
login_page = session.get(base_url)
print("Found the login page status Code is: ", login_page.status_code)
if login_page.status_code != 200:
    print("Failed to load the login page.")
    exit()

# Extract settings from the page
result = re.findall(r"(?<=var SETTINGS = )\S*;", str(login_page.content))
settings = json.loads(result[0][:-1])  # Removing the trailing semicolon
url = login_url + settings['transId'] + '&p=B2C_1A_signup_signin'
print("Login URL: ", url)

# Attempt to log in
login = session.post(
    url,
    data={
        'signInName': username,
        'password': password
    },
    headers={
        'x-csrf-token': settings['csrf'],
    },
    allow_redirects=True
)
print(login.text)
data = re.sub(r'}\s*?{', '},{', str(login.text))
print(data)
try:
    response_data = json.loads(login.text)  # Parse the JSON response
    status_code= response_data.get("status", "Unknown Error Code")
    if status_code != 200:
      error_code = response_data.get("errorCode", "Unknown Error Code")
      message = response_data.get("message", "Unknown Error Message")
      # Display the error message and code
      print(f"Login failed! Error Code: {error_code}, Message: {message}")
      exit()
except json.JSONDecodeError:
    print("Failed to parse the server response. Response may not be in JSON format.")
    print("Raw Response: ", login.text)


#confirm_login = session.get(
#    'https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/api/CombinedSigninAndSignup/confirmed',
#      'rememberMe': False,
#     params={
#      'csrf_token': settings['csrf'],
#      'tx': settings['transId'],
#      'p': 'B2C_1A_signup_signin',
#    }
#  )

#soup = BeautifulSoup(confirm_login.content, 'html.parser')
#print("soup: ", soup)

print("-"*10)