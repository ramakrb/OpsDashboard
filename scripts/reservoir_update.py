import requests
import pandas as pd
from datetime import datetime
import subprocess 
import os

def get_latest_reservoir_data():
    """
    Fetches data for multiple sites from the USBR API, combines data from two API calls,
    and returns a dictionary with the latest data point for each site,
    using the overall latest timestamp. Timestamps are formatted as mm/dd/yyyy.
    """

    url1 = "https://www.usbr.gov/pn-bin/hdb/hdb.pl?svr=lchdb&sdi=1721,2086,2087&tstp=DY&t1=-4&t2=-1&table=R&mrid=0&format=json"
    url2 = "https://www.usbr.gov/pn-bin/hdb/hdb.pl?svr=uchdb2&sdi=1719&tstp=DY&t1=-4&t2=-1&table=R&mrid=0&format=json"

    try:
        response1 = requests.get(url1)
        response1.raise_for_status()
        data1 = response1.json()

        response2 = requests.get(url2)
        response2.raise_for_status()
        data2 = response2.json()

        data_dict = {}  # Dictionary to store the latest data for each site
        all_timestamps = [] #list to store all timestamps

        # Process data from the first API call
        for series in data1["Series"]:
            sdi = series["SDI"]
            site_name = series["SiteName"]
            column_label = f"{sdi}-{site_name}"
            timestamps = [item["t"] for item in series["Data"]]
            values = [item["v"] for item in series["Data"]]

            data_dict[column_label] = {"timestamps": timestamps, "values": values}
            all_timestamps.extend(timestamps)

        # Process data from the second API call
        for series in data2["Series"]:
            sdi = series["SDI"]
            site_name = series["SiteName"]
            column_label = f"{sdi}-{site_name}"
            timestamps = [item["t"] for item in series["Data"]]
            values = [item["v"] for item in series["Data"]]

            data_dict[column_label] = {"timestamps": timestamps, "values": values}
            all_timestamps.extend(timestamps)

        # Find the overall latest timestamp
        overall_latest_timestamp = max(all_timestamps)

        #Format the timestamp
        latest_date_obj = datetime.strptime(overall_latest_timestamp, "%m/%d/%Y %I:%M:%S %p")
        formatted_timestamp = latest_date_obj.strftime("%m/%d/%Y")

        #Create the dictionary containing the latest data.
        latest_data = {"timestamp": formatted_timestamp}
        for column_label, data in data_dict.items():
            if overall_latest_timestamp in data["timestamps"]:
                index = data["timestamps"].index(overall_latest_timestamp)
                latest_data[column_label] = data["values"][index]
            else:
                latest_data[column_label] = None

        return latest_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error parsing JSON: {e}")
        return None
    except ValueError as e:
        print(f"Error formatting timestamp: {e}")
        return None

if __name__ == "__main__":
    latest_reservoir_data = get_latest_reservoir_data()

    if latest_reservoir_data is not None:
        try:
            lake_powell_value = round(float(latest_reservoir_data.get("1719-LAKE POWELL", 0)))
            lake_mead_value = round(float(latest_reservoir_data.get("1721-Lake Mead", 0)))
            lake_mohave_value = round(float(latest_reservoir_data.get("2086-Lake Mohave", 0)))
            lake_havasu_value = round(float(latest_reservoir_data.get("2087-Lake Havasu", 0)))
            
            formatted_timestamp = latest_reservoir_data["timestamp"]

            res_attrib = [
                {'label': 'Lake Powell', 'upper_left': (2320, 170), 'size': 7.0, 'max_fill': 23313800, 'current_fill': lake_powell_value, 'date': formatted_timestamp},
                {'label': 'Lake Mead', 'upper_left': (1300, 310), 'size': 7.0, 'max_fill': 26120000, 'current_fill': lake_mead_value, 'date': formatted_timestamp},
                {'label': 'Lake Mohave', 'upper_left': (1580, 620), 'size': 2.5, 'max_fill': 1809800, 'current_fill': lake_mohave_value, 'date': formatted_timestamp},
                {'label': 'Lake Havasu', 'upper_left': (1680, 890), 'size': 2.0, 'max_fill': 619400, 'current_fill': lake_havasu_value, 'date': formatted_timestamp}
            ]
            
            scripts_dir = "scripts"
            os.makedirs(scripts_dir, exist_ok=True) #creates the scripts directory if it does not exist.

            reservoirsa_path = os.path.join(scripts_dir, "reservoirsa.py")

            with open(reservoirsa_path, "w") as f:
                f.write("res_attrib = [\n")
                for item in res_attrib:
                    f.write(f"    {item},\n")
                f.write("]\n")
            
            print("reservoirsa.py created successfully in the scripts directory.")
            
            # Run LCTeacup.py
            try:
                subprocess.run(["python", os.path.join(scripts_dir, "LCTeacup.py")], check=True)
                print("LCTeacup.py executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing LCTeacup.py: {e}")
            except FileNotFoundError:
                print("Error: LCTeacup.py not found.")
            

        except (TypeError, ValueError) as e:
            print(f"Error processing data: {e}")
    else:
        print("Failed to retrieve reservoir data.")