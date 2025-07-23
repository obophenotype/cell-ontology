import requests
import csv
import os

# Define the API URL
API_URL = "https://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/hra/ftu-parts"

# Load curated image URLs from the curated file
def load_curated_image_urls(curated_file_path):
    curated_urls = set()
    if os.path.exists(curated_file_path):
        with open(curated_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                url = row.get("HRA_2D_FTU", "").strip()
                if url:
                    curated_urls.add(url)
    return curated_urls

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
def process_and_filter_csv(csv_text, output_file, curated_urls):
    lines = csv_text.splitlines()
    reader = csv.DictReader(lines)

    new_rows = []
    for row in reader:
        iri = row.get("ftu_part_iri", "")
        if iri.startswith("http://purl.obolibrary.org/obo/CL_"):
            cl_id = iri.replace("http://purl.obolibrary.org/obo/CL_", "CL:")
            image_url = row.get("image_url", "").strip()

            if image_url in curated_urls or not image_url:
                continue  # Skip already curated or empty URLs

            doi = row.get("ftu_digital_object_doi", "").strip()
            if doi.startswith("https://doi.org/"):
                doi = doi.replace("https://doi.org/", "doi:")

            new_rows.append({
                "ftu_part_id": cl_id,
                "image_url": image_url,
                "ftu_digital_object_doi": doi
            })

    file_exists = os.path.exists(output_file)
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            # Write headers only if the file is new
            writer.writerow(["ftu_part_id", "image_url", "ftu_digital_object_doi", "license", "label"])
            writer.writerow(["ID", "A foaf:depiction", ">A oboInOwl:hasDbXref", ">AI dc:licence", ""])

        for row in new_rows:
            writer.writerow([
                row["ftu_part_id"],
                row["image_url"],
                row["ftu_digital_object_doi"],
                "http://creativecommons.org/licenses/by/4.0/",
                ""  # label column is empty
            ])

    print(f"Appended {len(new_rows)} new entries to {output_file}")

# Main execution
def main():
    processed_file = "../templates/2DFTU_HRA_illustrations.csv"
    curated_file = "../../images/HRA_curated_images.csv"

    print("Loading curated image URLs...")
    curated_urls = load_curated_image_urls(curated_file)

    print("Downloading and processing CSV from API...")
    csv_text = download_csv(API_URL)

    if csv_text:
        process_and_filter_csv(csv_text, processed_file, curated_urls)

if __name__ == "__main__":
    main()
