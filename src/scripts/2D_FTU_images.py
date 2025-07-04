import requests

# Define the API URL
API_URL = "https://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/hra/ftu-parts"

# Function to fetch CSV data from the API and save it directly to a file
def fetch_and_save_csv(url, output_file):
    headers = {"Accept": "text/csv"}  # Request CSV format
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Write the CSV data directly to the output file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            file.write(response.text)
        print(f"CSV data saved to {output_file}")
    else:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")

# Main execution
def main():
    output_file = "robot_template.csv"
    print(f"Fetching and saving CSV template to {output_file}...")
    fetch_and_save_csv(API_URL, output_file)

if __name__ == "__main__":
    main()