import os
from Bio import Entrez
from Bio import SeqIO
import sys

def get_genome(accession, out):
    ipg = os.path.join(out, accession)
    cmd = "esearch -db ipg -query {0} | efetch -format ipg > {1}".format(accession, ipg)
    os.system(cmd)
    f = open(ipg).read().split("\n")[1:-1]
    for i in f:
        info = i.split("\t")
        Nucleotide_Accession = info[2]
        codon_s = int(info[3]); end = int(info[4]); strand = info[5]
        Protein_accession = info[6]
        if Protein_accession == accession:
            func = info[7]
            Organism = info[8]
            strain = info[9]
            handle = Entrez.efetch(db="nuccore", id=Nucleotide_Accession, rettype="gb", retmode="text", style='withparts')
            records = SeqIO.read(handle, "genbank")
            ids = []; products = []; translations = []; locations=[]
            for i in records.features:
                if i.type=="CDS":
                    qualifiers = i.qualifiers
                    location = i.location
                    locations.append(location)
                    if "protein_id" in qualifiers:
                        protein_id = qualifiers["protein_id"][0]
                    else:
                        protein_id = qualifiers["locus_tag"][0]
                    ids.append(protein_id)
                    product = qualifiers["product"][0]
                    products.append(product)
                    if "translation" in qualifiers:
                        translation = qualifiers["translation"][0]
                    else:
                        translation="-"
                    translations.append(translation)
                    
            target_index = ids.index(Protein_accession)
            current_gene = Protein_accession
            current_location = locations[target_index]
            current_product = products[target_index]
            current_translate = translations[target_index]
            flanking_current = [Organism + " " +  strain]
            
            if target_index + 1 == len(ids):
                up_index = target_index-1
                up_gene = ids[up_index]; down_gene = "NA"
                up_location = locations[up_index]; down_location="NA"
                up_product = products[up_index]; down_product="NA"
                up_translation = translations[up_index]; down_translation = "NA"
                flanking_current.extend([str(up_gene), str(up_location), str(up_product), str(up_translation)])
                flanking_current.extend([str(current_gene), str(current_location), str(current_product), str(current_translate)])
                flanking_current.extend([str(down_gene), str(down_location), str(down_product), str(down_translation)])
                target_info =  flanking_current
                return target_info
            if target_index == 0:
                down_index = target_index +1
                up_gene = "NA"; down_gene = ids[down_index]
                up_location = "NA"; down_location=locations[down_index]
                up_product = "NA"; down_product= products[down_index]
                up_translation = "NA"; down_translation=translations[down_index]
                flanking_current.extend([str(up_gene), str(up_location), str(up_product), str(up_translation)])
                flanking_current.extend([str(current_gene), str(current_location), str(current_product), str(current_translate)])
                flanking_current.extend([str(down_gene), str(down_location), str(down_product), str(down_translation)])
                target_info =  flanking_current
                return target_info
            else:
                up_index = target_index-1
                down_index = target_index +1
                up_gene = ids[up_index]; down_gene=ids[down_index]
                up_location = locations[up_index]; down_location=locations[down_index]
                up_product = products[up_index]; down_product = products[down_index]
                up_translation = translations[up_index]; down_translation = translations[down_index]
                #print(Organism, strain)
                #print(up_gene, up_location, up_product, up_translation)
                #print(current_gene, current_location, current_product, current_translate)
                #print(down_gene, down_location, down_product, down_translation)
                #print("\n")
                flanking_current.extend([str(up_gene), str(up_location), str(up_product), str(up_translation)])
                flanking_current.extend([str(current_gene), str(current_location), str(current_product), str(current_translate)])
                flanking_current.extend([str(down_gene), str(down_location), str(down_product), str(down_translation)])
                target_info =  flanking_current
                return target_info

def remote_blast():
    cmd = "blastp -db nr -query {0} -seg no -evalue 0.000001 -max_target_seqs 100000 -outfmt '7 qseqid sseqid sallseqid slen sstart send evalue pident qcovs qseq sseq qstart qend score sscinames stitle' -entrez_query 'prokaryotes[Organism]' -remote > ./data/blast_result".format(query)
    os.system(cmd)
    
def parse_blast(inblast, outfile):
    OUT = open(outfile, "w")
    f = open(inblast).read().split("\n")
    for i in f:
        if "#" not in i:
            info = i.split("\t")
            hit = info[1].split("|")[1]
            align_parameter = info[6:9]
            try:
                target_info = get_genome(hit, "./data")
                align_parameter.extend(target_info)
                #print("\t".join(align_parameter))
                OUT.write("\t".join(align_parameter) + "\n")
            except Exception:
                #print("Error:" + i)
                OUT.write("Error:" + i + "\n")
    OUT.close()
    
if __name__ == "__main__":
    # input file and the user email to query NCBI
    inblast = "error"
    outfile = "neighbour_error"
    query = "/home/chuand/other/chenwenqing/PenG.fa"
    Entrez.email="1677416166@qq.com"
    
    #remote_blast()
    parse_blast(inblast, outfile)
