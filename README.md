# Enfusion API

A Python package to interact with the Enfusion API and retrieve data as pandas DataFrames. This package uses the same mechanism as the excel plug-in.

## Installation

You can install the Enfusion API package using pip:

```bash
pip install enfusion_api
```

## Usage
Here are examples of how to use the Enfusion API package:

## Without Authentication (When Already Logged In)
If you're already logged into the Enfusion software on your machine, you can use the API without providing credentials:

```python
from enfusion_api import EnfusionAPI

# Create an instance of EnfusionAPI without authentication
api = EnfusionAPI()

# Define the webservice URLs you want to fetch data from
urls = ["https://your-enfusion-report-url.com"]

# Get the data
dataframes = api.get_data(urls)

# Process the dataframes
for df in dataframes:
    print(df.head())
```

Webservice URLs are accessed from within Enfusion on My Reports, right click and "Copy Web Service URL":

![WebService URL Location](image.png)

## With Authentication
If you need to provide authentication details:

```python
from enfusion_api import EnfusionAPI

# Create an instance of EnfusionAPI with authentication
api = EnfusionAPI(
    admin_user_name="your_admin_username",
    admin_password="your_admin_password",
    user_name="your_username",
    password="your_password"
)

# Define the URLs you want to fetch data from
urls = ["https://your-enfusion-report-url.com"]

# Get the data
dataframes = api.get_data(urls)

# Process the dataframes
for df in dataframes:
    print(df.head())
```
Note: Reconciliation Reports (.diff) are not currently supported without authentication.

## License
This project is licensed under the MIT License - see the LICENSE file for details.