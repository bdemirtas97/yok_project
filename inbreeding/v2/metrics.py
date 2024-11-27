import psycopg2
import pandas as pd
import math
import datetime
import uni_list

def fetchData_createTable(department_arg, cur, filename):
    cur.execute(f"""
        SELECT degrees.id, degrees.degree, degrees.university, degrees.years FROM scholars join degrees on scholars.id = degrees.id
        where scholars.university in ('ORTA DOĞU TEKNİK ÜNİVERSİTESİ', 'İSTANBUL TEKNİK ÜNİVERSİTESİ',
        'YILDIZ TEKNİK ÜNİVERSİTESİ', 'BOĞAZİÇİ ÜNİVERSİTESİ', 'KARADENİZ TEKNİK ÜNİVERSİTESİ',
        'HACETTEPE ÜNİVERSİTESİ', 'İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ', 'SABANCI ÜNİVERSİTESİ')
        and (scholars.department = {department_arg})
    """)
    degrees_data = cur.fetchall()
    degrees = {}
    for degree_row in degrees_data:
        scholar_id, degree, university, years = degree_row
        if scholar_id not in degrees:
            degrees[scholar_id] = []
        degrees[scholar_id].append((university, degree, years))

    # Query all scholars at once
    cur.execute(f"""
        SELECT scholars. university, scholars.id, scholars.title FROM scholars join degrees on scholars.id = degrees.id
        where scholars.university in ('ORTA DOĞU TEKNİK ÜNİVERSİTESİ', 'İSTANBUL TEKNİK ÜNİVERSİTESİ',
        'YILDIZ TEKNİK ÜNİVERSİTESİ', 'BOĞAZİÇİ ÜNİVERSİTESİ', 'KARADENİZ TEKNİK ÜNİVERSİTESİ',
        'HACETTEPE ÜNİVERSİTESİ', 'İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ')
        and (scholars.department = {department_arg}) GROUP by scholars.university, scholars.id, scholars.title
    """)
    scholar_data_raw = cur.fetchall()
    scholar_data = {}
    for row in scholar_data_raw:
        university, scholar_id, title = row
        if university not in scholar_data:
            scholar_data[university] = []
        scholar_data[university].append((scholar_id, title))

    results = {x:{
        "number_of_scholars": len(scholar_data[x]),
        "self_recruitment_ratio": 0,
        "institutional_diversity_index": 0,
        "article_tier_1": 0,
        "article_tier_2": 0,
        "project_tier_1": 0,
         "project_tier_2": 0
    } for x in scholar_data.keys()}

    self_recruitment_ratio(scholar_data, degrees, results)
    institutional_diversity_index(scholar_data, degrees, results)
    calculate_works(scholar_data, degrees, results, department_arg, cur)

    write_to_excel(results, filename)

def calculate_works(scholar_data, degrees, results, department_arg, cur):
    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        article_1_score = 0
        article_2_score = 0
        project_1_score = 0
        project_2_score = 0

        cur.execute(f"""select scholars.id, count(*) from articles join scholars on articles.id = scholars.id where scholars.university = '{university}'
            AND scholars.department = {department_arg} AND (articles.index LIKE '%SCI%' OR articles.index ILIKE '%scopus%' OR articles.index
            ILIKE '%ei%' OR articles.index ILIKE '%engineering index%' OR articles.index ILIKE '%inspec%' or articles.index ILIKE '%wos%') and articles.category = 'Özgün Makale' group by scholars.id""")
        query_result = cur.fetchall()
        article_1_data = dict(query_result)

        cur.execute(f"""select scholars.id, count(*) from articles join scholars on articles.id = scholars.id where scholars.university = '{university}'
            AND scholars.department = {department_arg} group by scholars.id""")
        query_result = cur.fetchall()

        article_total = dict(query_result)
        article_2_data = {key: article_total.get(key,0) - article_1_data.get(key,0) for key in article_total.keys()}

        cur.execute(f"""select scholars.id, count(*) from projects join scholars on projects.id = scholars.id where scholars.university = '{university}'
            AND scholars.department = {department_arg} and (projects.funder ilike '%tak%' or projects.funder ilike '%avrupa%' or projects.funder ilike '%uluslararası%') group by scholars.id""")
        query_result = cur.fetchall()

        project_1_data = dict(query_result)

        cur.execute(f"""select scholars.id, count(*) from projects join scholars on projects.id = scholars.id where scholars.university = '{university}'
            AND scholars.department = {department_arg} group by scholars.id""")
        query_result = cur.fetchall()
        project_total = dict(query_result)

        project_2_data = {key: project_total.get(key,0) - project_1_data.get(key,0) for key in project_total.keys()}

        for scholar in scholars:
            phd_year = highest_degree_finder(degrees.get(scholar[0], []), scholar[1])[1]
            if phd_year == "Unknown": continue
            else: phd_year = int(phd_year)
            # if phd_year == "Unknown": phd_year = 2024
            active_years = datetime.datetime.today().year - phd_year + 1

            article_1_score += article_1_data.get(scholar[0], 0) / active_years
            article_2_score += article_2_data.get(scholar[0], 0) / active_years
            project_1_score += project_1_data.get(scholar[0], 0) / active_years
            project_2_score += project_2_data.get(scholar[0], 0) / active_years

        results[university]["article_tier_1"] = article_1_score / len(scholars)
        results[university]["article_tier_2"] = article_2_score / len(scholars)
        results[university]["project_tier_1"] = project_1_score / len(scholars)
        results[university]["project_tier_2"] = project_2_score / len(scholars)

def self_recruitment_ratio(scholar_data, degrees, results):
    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0

        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees.get(scholar[0], []), scholar[1])[0]
            if highest_degree_univ == university:
                score += 1

        ratio = score / len(scholars) if len(scholars) > 0 else 0
        results[university]["self_recruitment_ratio"] = ratio

def institutional_diversity_index(scholar_data, degrees, results):
    for university in scholar_data.keys():
        scholars = scholar_data.get(university, [])
        score = 0
        scholars_grouped_by_univ = dict()

        for scholar in scholars:
            highest_degree_univ = highest_degree_finder(degrees.get(scholar[0], []), scholar[1])[0]
            if(highest_degree_univ not in scholars_grouped_by_univ.keys()): scholars_grouped_by_univ[highest_degree_univ] = 1
            else: scholars_grouped_by_univ[highest_degree_univ] += 1
        num_of_scholars = len(scholars) - scholars_grouped_by_univ.get("Unknown", 0)
        for key, value in scholars_grouped_by_univ.items():
            if(key == "Unknown"): continue
            portion = value / num_of_scholars
            score += portion * math.log(portion)
        
        results[university]["institutional_diversity_index"] = score * -1
        

def write_to_excel(data, filename):
    df = pd.DataFrame.from_dict(data, orient='index')

    df.to_excel(filename, index=True)

def highest_degree_finder(degree_map, title):
    priority_map = {
        ' Önlisans': 0,
        ' Lisans-Anadal': 1,
        ' Lisans-ÇiftAnadal': 1,
        ' Lisans-Yandal': 1,
        ' Önlisans': 1,
        ' Yüksek Lisans-İkinci Öğretim Tezsiz': 2,
        ' Yüksek Lisans-Tezli': 2,
        ' Yüksek Lisans-Tezsiz': 2,
        ' Bütünleşik Doktora': 3,
        ' Diş Hekimliğinde Uzmanlık': 3,
        ' Doğrudan Doktora': 3,
        ' Doktora': 3, 
        ' Eczacılıkta Uzmanlık': 3,
        ' Sanatta Yeterlik': 3,
        ' Tıpta Uzmanlık': 3
    }
    

    if len(degree_map) == 0: return "Unknown", "Unknown"

    degree_univ = 'Unknown'
    degree_year = 'Unknown'
    degree_level = 0
    degree_map.sort(key=lambda x: x[2].split('-')[-1])

    for degree in degree_map:
        if priority_map.get(degree[1], -1) > degree_level or (priority_map.get(degree[1], -1) == degree_level and int(degree_year) < int(degree[2].split('-')[-1])): 
            degree_univ = degree[0]
            degree_year = degree[2].split('-')[-1]
            degree_level = priority_map[degree[1]]

        if degree_level == 3: break

    if title == 'ÖĞRETİM GÖREVLİSİ' or degree_level == 3:
        return degree_univ, degree_year
    
    return 'Unknown', 'Unknown'


conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
cur = conn.cursor()
uni_list = uni_list.get_universities()


fetchData_createTable('\'Bilgisayar Bilimleri ve Mühendisliği\'', cur, "bilgisayar.xlsx")
# fetchData_createTable('\'Kimya Mühendisliği\'', cur, "kimya.xlsx")
# fetchData_createTable('\'Endüstri Mühendisliği\'', cur, "endüstri.xlsx")
# fetchData_createTable('\'Makine Mühendisliği\'', cur, "makine.xlsx")
# fetchData_createTable('\'İnşaat Mühendisliği\'', cur, "inşaat.xlsx")
# fetchData_createTable('\'Elektrik-Elektronik Mühendisliği\' or scholars.department = \'Elektrik-Elektronik ve Haberleşme Mühendisliği\'', cur, "elektronik.xlsx")