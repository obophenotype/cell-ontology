import csv
import requests

# Define the API URL
API_URL = "https://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/hra/ftu-parts"

# Function to fetch CSV data from the API
def fetch_api_data(url):
    headers = {"Accept": "text/csv"}  # Request CSV format
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Return the CSV data as text
        return response.text
    else:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        return None

# Function to parse CSV data into a list of rows
def parse_csv_data(csv_data):
    rows = []
    # Use csv.reader to parse the CSV content
    for row in csv.reader(csv_data.splitlines()):
        rows.append(row)
    return rows

# Function to generate ROBOT template CSV from API data
def generate_robot_template(data, header, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header directly from the API response to the ROBOT template
        writer.writerow(header)
        
        # Process each row in the API data
        for row in data:
            writer.writerow(row)  # Write the row without modification

# Main execution
def main():
    print("Fetching data from the API...")
    csv_data = fetch_api_data(API_URL)
    if csv_data:
        # Parse the CSV data into rows
        rows = parse_csv_data(csv_data)
        print(f"Fetched {len(rows)} rows from the API.")
        
        # The first row is the header, so we use it directly
        header = rows[0]
        # All the remaining rows are the data
        data = rows[1:]
        
        output_file = "robot_template.csv"
        print(f"Generating ROBOT template: {output_file}")
        generate_robot_template(data, header, output_file)
        print(f"Template saved to {output_file}")

if __name__ == "__main__":
    main()