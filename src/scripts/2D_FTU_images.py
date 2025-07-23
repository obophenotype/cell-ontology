import requests
import csv

# Define the API URL
API_URL = "https://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/hra/ftu-parts"

# Function to download CSV from the API
def download_csv(url):
    headers = {"Accept": "text/csv"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        return None

# Function to process and filter the CSV
def process_and_filter_csv(csv_text, processed_output_file):
    lines = csv_text.splitlines()
    reader = csv.DictReader(lines)

    filtered_rows = []
    for row in reader:
        iri = row.get("ftu_part_iri", "")
        if iri.startswith("http://purl.obolibrary.org/obo/CL_"):
            cl_id = iri.replace("http://purl.obolibrary.org/obo/CL_", "CL:")
            
            ftu_digital_object_doi = row.get("ftu_digital_object_doi", "").strip()
            if ftu_digital_object_doi.startswith("https://doi.org/"):
                ftu_digital_object_doi = ftu_digital_object_doi.replace("https://doi.org/", "doi:")

            filtered_rows.append({
                "ftu_part_id": cl_id,
                "image_url": row.get("image_url", ""),
                "ftu_digital_object_doi": ftu_digital_object_doi
            })

    with open(processed_output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # First header line (column labels)
        writer.writerow(["ftu_part_id", "ftu_digital_object_doi", "image_url", "license"])
        # Second header line (ROBOT template syntax)
        writer.writerow(["ID", "A foaf:depiction", ">A oboInOwl:hasDbXref", ">AI dc:licence"])

        # Data rows
        for row in filtered_rows:
            writer.writerow([
                row["ftu_part_id"],
                row["image_url"],
                row["ftu_digital_object_doi"],
                "http://creativecommons.org/licenses/by/4.0/"
            ])

    print(f"Filtered ROBOT template CSV saved to {processed_output_file}")

# Main execution
def main():
    processed_file = "../templates/2DFTU_HRA_illustrations.csv"

    print("Downloading and processing CSV...")
    csv_text = download_csv(API_URL)
    
    if csv_text:
        process_and_filter_csv(csv_text, processed_file)

if __name__ == "__main__":
    main()