import requests
import pandas as pd
from Bio import Entrez, SeqIO

# Set email for Entrez API
Entrez.email = "your_email@example.com"  # Replace with your email

def fetch_protein_sequence(uniprot_id):
    """Fetch protein sequence from UniProt using its ID"""
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    response = requests.get(url)
    if response.status_code == 200:
        sequence = "".join(response.text.split("\n")[1:])  # Remove header
        return sequence
    else:
        return None

def check_alphafold_structure(uniprot_id):
    """Check if AlphaFold has a predicted structure for a given UniProt ID"""
    alphafold_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    response = requests.get(alphafold_url)
    if response.status_code == 200:
        return response.json()[0]['pdbUrl']  # Return PDB structure link
    return "No AlphaFold structure available"

def main():
    # Example: List of UniProt IDs to check
    uniprot_ids = ["P01308", "P62258", "Q9Y5Y9"]  # Insulin, Beta-2-microglobulin, Alpha-synuclein
    
    data = []
    for uniprot_id in uniprot_ids:
        sequence = fetch_protein_sequence(uniprot_id)
        structure_link = check_alphafold_structure(uniprot_id)
        data.append([uniprot_id, sequence[:50] + "...", structure_link])  # Show only first 50 chars

    # Save to CSV
    df = pd.DataFrame(data, columns=["UniProt ID", "Sequence (truncated)", "AlphaFold Structure"])
    df.to_csv("protein_structure_results.csv", index=False)

    print("Protein structure details saved to protein_structure_results.csv")

if __name__ == "__main__":
    main()
