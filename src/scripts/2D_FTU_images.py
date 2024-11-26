import csv
from SPARQLWrapper import SPARQLWrapper, JSON

# Define SPARQL endpoint and query (from https://github.com/hubmapconsortium/ccf-grlc/blob/main/hra/ftu-parts.rq)
SPARQL_ENDPOINT = "https://lod.humanatlas.io/sparql"  # Update if necessary
SPARQL_QUERY = """
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ccf: <http://purl.org/ccf/>
PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX HRA: <https://purl.humanatlas.io/collection/hra>
PREFIX LOD: <https://lod.humanatlas.io>

SELECT DISTINCT ?ftu_digital_object ?ftu_digital_object_doi ?image_url ?organ_iri ?ftu_iri ?ftu_part_iri
FROM HRA:
WHERE {
  ?ftu_illustration a ccf:FtuIllustration ;
  	a ?ftu_iri ;
  	ccf:ccf_located_in ?organ_id ;
    ccf:illustration_node [ a ?ftu_part_iri ] ;
    ccf:image_file [
      ccf:file_format ?format ;
      ccf:file_url ?image_url
    ] .

  HRA: prov:hadMember ?versioned_ftu .

  GRAPH LOD: {
    ?versioned_ftu prov:wasDerivedFrom [
      ccf:doi ?ftu_digital_object_doi
    ] .
  }

  BIND(IRI(REPLACE(?organ_id, 'UBERON:', STR(UBERON:))) as ?organ_iri)
  BIND(IRI(REPLACE(STR(?ftu_illustration), "#primary", "")) as ?ftu_digital_object)
  
  FILTER(?format = "image/png") # or "image/svg+xml"
  FILTER(STRSTARTS(STR(?ftu_iri), STR(obo:)))
  FILTER(STRSTARTS(STR(?ftu_part_iri), STR(obo:)))
  FILTER(STRSTARTS(STR(?versioned_ftu), STR(?ftu_digital_object)))
}
"""

# Function to run SPARQL query and fetch results
def fetch_sparql_results(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

# Function to generate ROBOT template CSV
def generate_robot_template(data, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header for ROBOT template
        writer.writerow([
            "FTU_IRI", "FTU_part_IRI", "Organ_IRI", "FTU_digital_object", "DOI", 
            "Image_URL",
        ])
        # Process each row in data
        for row in data:
            ftu_iri = row["ftu_iri"]["value"]
            ftu_part_iri = row["ftu_part_iri"]["value"]
            organ_iri = row["organ_iri"]["value"]
            image_url = row["image_url"]["value"]
            doi = row["ftu_digital_object_doi"]["value"]
            ftu_digital_object = row["ftu_digital_object"]["value"]
            
            # Add to ROBOT template
            writer.writerow([
                ftu_iri,  # ID
                ftu_part_iri,  # Label (last part of IRI)
                organ_iri,  # Definition
                ftu_digital_object,  # Comment
                doi,  # Annotation:source
                image_url,  # Annotation:image_url
            ])

# Main execution
def main():
    print("Fetching SPARQL results...")
    data = fetch_sparql_results(SPARQL_ENDPOINT, SPARQL_QUERY)
    print(f"Fetched {len(data)} records.")
    
    output_file = "robot_template.csv"
    print(f"Generating ROBOT template: {output_file}")
    generate_robot_template(data, output_file)
    print(f"Template saved to {output_file}")

if __name__ == "__main__":
    main()