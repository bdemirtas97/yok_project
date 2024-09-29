import psycopg2
import pandas as pd
import math

def write_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def highest_degree_finder(degrees, scholar_id, title):
    degree_map = degrees.get(scholar_id, [])

    if title in ['ARAŞTIRMA GÖREVLİSİ', 'ÖĞRETİM GÖREVLİSİ']:
        for degree in degree_map:
            if degree[1] in [' Yüksek Lisans-İkinci Öğretim Tezsiz', ' Yüksek Lisans-Tezli', ' Yüksek Lisans-Tezsiz']:
                return degree[0]  # Assuming the first element is university
        # Fallback to undergraduate degrees
        for degree in degree_map:
            if degree[1] in [' Lisans-Anadal', ' Lisans-ÇiftAnadal', ' Lisans-Yandal', ' Önlisans']:
                return degree[0]
    else:
        for degree in degree_map:
            if degree[1] in [' Bütünleşik Doktora', ' Diş Hekimliğinde Uzmanlık', ' Doğrudan Doktora', ' Doktora', 
                          ' Eczacılıkta Uzmanlık', ' Sanatta Yeterlik', ' Tıpta Uzmanlık']:
                return degree[0]

    return "Unknown"


def self_recruitment_ratio(scholar_data, degrees):
    result = []

    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0

        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees, scholar[0], scholar[1])
            if highest_degree_univ == university:
                score += 1

        ratio = score / len(scholars) if len(scholars) > 0 else 0
        result.append({
            "university": university,
            "ratio": ratio
        })

    return result

def institutional_diversity_index(scholar_data, degrees):
    result = []

    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0
        scholars_grouped_by_univ = dict()

        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees, scholar[0], scholar[1])
            if(highest_degree_univ not in scholars_grouped_by_univ.keys()): scholars_grouped_by_univ[highest_degree_univ] = 1
            else: scholars_grouped_by_univ[highest_degree_univ] += 1
        for key, value in scholars_grouped_by_univ.items():
            if(key == "Unknown"): continue
            portion = value / len(scholars)
            score += portion * math.log(portion)
        
        result.append({
            "university": university,
            "index": score * -1
        })
    
    return result

def alumni_representational_index(scholar_data, degrees, num_of_all_scholars):
    index_data = {x: {"inbred": 0, "total": 0} for x in scholar_data.keys()}
    index_data["Unknown"] = {"total": 0}

    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees, scholar[0], scholar[1])
            if highest_degree_univ == university: index_data[university]["inbred"] += 1
            if(highest_degree_univ in index_data.keys()): index_data[highest_degree_univ]["total"] += 1

            
    results = []
    for key,value in index_data.items():
        num_of_scholars = len(scholar_data.get(key, []))
        if(key == "Unknown" or num_of_scholars == 0): continue
        ratio = (value["inbred"] / num_of_scholars) / (value["total"] / num_of_all_scholars) if value["total"] != 0 else 0
        results.append({
            "university": key,
            "index": ratio
        })

    return results
        
def multi_degree_inbredding(scholar_data, degrees):
    result = []

    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0

        for scholar in scholars:
            degree_map = degrees.get(scholar[0], [])
            degree_count = 0
            for degree in degree_map:
                if(degree[0] == university): degree_count +=1
            if degree_count > 1:
                score += 1

        ratio = score / len(scholars) if len(scholars) > 0 else 0
        result.append({
            "university": university,
            "ratio": ratio
        })

    return result

def foreign_degree_ratio(scholar_data, degrees):
    result = []

    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0

        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees, scholar[0], scholar[1])
            if len(highest_degree_univ) < 10: continue
            if(highest_degree_univ not in scholar_data.keys() and not ("hastane" in highest_degree_univ.lower()
                    or "tıp" in highest_degree_univ.lower() or "tip" in highest_degree_univ.lower())):
                print(highest_degree_univ)
                score += 1

        ratio = score / len(scholars) if len(scholars) > 0 else 0
        result.append({
            "university": university,
            "ratio": ratio
        })

    return result





if __name__ == "__main__":
    conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
    cur = conn.cursor()

    # Query all degrees at once
    cur.execute("""
        SELECT id, degree, university 
        FROM degrees
    """)
    degrees_data = cur.fetchall()
    degrees = {}
    for degree_row in degrees_data:
        scholar_id, degree, university = degree_row
        if scholar_id not in degrees:
            degrees[scholar_id] = []
        degrees[scholar_id].append((university, degree))

    # Query all scholars at once
    cur.execute("""
        SELECT university, id, title
        FROM scholars
    """)
    scholar_data_raw = cur.fetchall()
    num_of_all_scholars = len(scholar_data_raw)
    scholar_data = {}
    for row in scholar_data_raw:
        university, scholar_id, title = row
        if university not in scholar_data:
            scholar_data[university] = []
        scholar_data[university].append((scholar_id, title))


    # Compute self-recruitment ratio
    #self_recruitment_by_universities = self_recruitment_ratio(scholar_data, degrees)
    #write_to_excel(self_recruitment_by_universities, "self_recruitment_ratios.xlsx")

    #Compute diversity index
    #institutional_diversity_index_by_universities = institutional_diversity_index(scholar_data, degrees)
    #write_to_excel(institutional_diversity_index_by_universities, "institutional_diversity_index.xlsx")

    #Compute Alumni Representation Index
    #alumni_representational_index_by_universities = alumni_representational_index(scholar_data, degrees, num_of_all_scholars)
    #write_to_excel(alumni_representational_index_by_universities, "alumni_representational_index.xlsx")

    #Multi-degree inbreeding
    #multi_degree_inbredding_by_universities = multi_degree_inbredding(scholar_data, degrees)
    #write_to_excel(multi_degree_inbredding_by_universities, "multi_degree_inbredding_ratio.xlsx")

    #Foreign Degree Ratio
    #foreign_degree_ratio_by_universities = foreign_degree_ratio(scholar_data, degrees)
    #write_to_excel(foreign_degree_ratio_by_universities, "foreign_degree_ratio.xlsx")
    cur.close()
    conn.close()