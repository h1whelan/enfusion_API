import requests
import pandas as pd
from io import StringIO

class EnfusionAPI:
    """
    A class to interact with the Enfusion API.

    This class provides methods to retrieve data from Enfusion reports as pandas DataFrames.

    Attributes:
        admin_user_name (str): Admin username for authentication.
        admin_password (str): Admin password for authentication.
        user_name (str): User username for authentication.
        password (str): User password for authentication.
        base_url (str): Base URL for the Enfusion API.
        headers (dict): HTTP headers for API requests.

    """

    def __init__(self, admin_user_name=None, admin_password=None, user_name=None, password=None):
        """
        Initialize the EnfusionAPI instance.

        Args:
            admin_user_name (str, optional): Admin username for authentication.
            admin_password (str, optional): Admin password for authentication.
            user_name (str, optional): Regular username for authentication.
            password (str, optional): Regular password for authentication.
        """
        self.admin_user_name = admin_user_name
        self.admin_password = admin_password
        self.user_name = user_name
        self.password = password
        self.base_url = "http://127.0.0.1:18443"
        self.headers = {
            "X-Application-Name": "Excel Integrata",
            "X-ENFUSION-EXCEL_LOCAL_IPS": self._get_non_local_ip_address(),
            "X-ENFUSION-VERSION": "4.1"
        }

    def _get_non_local_ip_address(self):
        """
        Get a non-local IP address for the API request.

        Returns:
            str: A hardcoded non-local IP address.
        """
        return '20.108.23.99'

    def _process_url(self, report_web_service_url):
        """
        Process the given URL and fetch the report data.

        Args:
            report_web_service_url (str): The URL of the Enfusion report.

        Returns:
            pandas.DataFrame or None: The report data as a DataFrame if successful, None otherwise.
        """
        # Replace the base URL
        report_web_service_url = report_web_service_url.replace(
            "https://webservices.enfusionsystems.com/mobile/rest/reportservice",
            self.base_url
        )

        diff_flag = False
        # Check if the URL contains ".diff" and adjust accordingly
        if ".diff" in report_web_service_url:
            diff_flag = True
            report_web_service_url = report_web_service_url.replace("exportReport?", "exportDiffReport?")
            open_report_query = f"{report_web_service_url}&format=csv"
        else:
            open_report_query = f"{report_web_service_url}&format=csv&ExcelMacroVBA=true"

        # Check for "showTotals=true" and add it if not present
        if "showTotals=true" not in open_report_query and not diff_flag:
            open_report_query += "&showTotals=false"

        auth = None
        if self.admin_user_name and self.admin_password:
            self.headers["login.adminuser"] = self.admin_user_name
            self.headers["login.adminpassword"] = self.admin_password
            if self.user_name and self.password:
                auth = (self.user_name, self.password)

        if diff_flag and not auth:
            print("Reconciliation Reports (.diff) are not currently supported without authentication.")
            return None

        try:
            response = requests.get(open_report_query, headers=self.headers, auth=auth, timeout=300)
            response.raise_for_status()
            # Process response and convert to DataFrame
            if response.status_code == 200:
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                return df
        except requests.Timeout:
            print("Integrata Server Error: Request timeout")
        except requests.HTTPError as http_err:
            self._handle_error(response.status_code, report_web_service_url, response.text)
        except requests.RequestException as req_err:
            print(f"Integrata Server Error: {req_err}")

        return None

    def _handle_error(self, status_code, report_web_service_url, response_text):
        """
        Handle errors that occur during API requests.

        Args:
            status_code (int): The HTTP status code of the response.
            report_web_service_url (str): The URL of the report that caused the error.
            response_text (str): The text content of the error response.
        """
        if status_code == 408:
            print("Integrata Server Error: Request timeout")
        elif status_code == 401:
            print("Integrata Server Error: Incorrect User Name or Password")
        elif status_code == 404:
            print(f"Integrata Server Error: Report Path Not Found\n\n{report_web_service_url}")
        else:
            print(f"Integrata Server Error: Status = {status_code}\n\nError Code:\n\n{response_text}")

    def get_data(self, urls):
        """
        Fetch data for multiple report URLs.

        Args:
            urls (list): A list of Enfusion report URLs to fetch data from.

        Returns:
            list: A list of pandas DataFrames containing the fetched report data.
        """
        dataframes = []
        for url in urls:
            df = self._process_url(url)
            if df is not None:
                dataframes.append(df)
        return dataframes