import psycopg2
import plotter

def title_organizer(dist):
    organized = {"Eğitim Bilimleri Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Fen Bilimleri ve Matematik Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Filoloji Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Güzel Sanatlar Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Hukuk Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "İlahiyat Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Mimarlık-Planlama-Tasarım": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Mühendislik Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Sağlık Bilimleri Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Sosyal-Beşeri ve İdari Bilimler Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Spor Bilimleri Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Ziraat ve Orman ve Su Ürünleri Temel Alanı": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            },
                 "Tanımsız": {
                            "PROFESÖR": 0,
                            "DOÇENT": 0,
                            "DOKTOR ÖĞRETİM ÜYESİ": 0,
                            "ÖĞRETİM GÖREVLİSİ": 0,
                            "ARAŞTIRMA GÖREVLİSİ": 0
                            }
                }
    
    for i in range(len(dist)):
        title = dist[i][0]
        field = dist[i][1] or "Tanımsız"
        if "doçent" in title.lower():
            organized[field]["DOÇENT"] += dist[i][2]
        elif "ÖĞRETİM GÖREVLİSİ" in title:
            organized[field]["ÖĞRETİM GÖREVLİSİ"] += dist[i][2]
        else:
            organized[field][title] += dist[i][2]
    
    return organized

def work_organizer(query):
    title_obj = {
        "PROFESÖR": 0,
        "DOÇENT": 0,
        "DOKTOR ÖĞRETİM ÜYESİ": 0,
        "ÖĞRETİM GÖREVLİSİ": 0,
        "ARAŞTIRMA GÖREVLİSİ": 0
    }

    for i in range(len(query)):
        title = query[i][0]
        if "doçent" in title.lower():
            title_obj["DOÇENT"] += query[i][1]
        elif "ÖĞRETİM GÖREVLİSİ" in title:
            title_obj["ÖĞRETİM GÖREVLİSİ"] += query[i][1]
        else:
            title_obj[title] += query[i][1]

    return title_obj

def supervised_thesis_organizer(query):
    thesis_obj = {
        "PROFESÖR": {"Yüksek Lisans": 0,
                     "Doktora": 0},
        "DOÇENT": {"Yüksek Lisans": 0,
                     "Doktora": 0},
        "DOKTOR ÖĞRETİM ÜYESİ": {"Yüksek Lisans": 0,
                     "Doktora": 0},
        "ÖĞRETİM GÖREVLİSİ": {"Yüksek Lisans": 0,
                     "Doktora": 0},
        "ARAŞTIRMA GÖREVLİSİ": {"Yüksek Lisans": 0,
                     "Doktora": 0},
    }

    for i in range(len(query)):
        title = query[i][0]
        degree  = 'Doktora' if query[i][1] != 'Yüksek Lisans' else 'Yüksek Lisans'
        if "doçent" in title.lower():
            thesis_obj["DOÇENT"][degree] += query[i][2]
        elif "ÖĞRETİM GÖREVLİSİ" in title:
            thesis_obj["ÖĞRETİM GÖREVLİSİ"][degree] += query[i][2]
        else:
            thesis_obj[title][degree] += query[i][2]

    return thesis_obj


if __name__ == "__main__":
    conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
    cur = conn.cursor()

    cur.execute("SELECT scholars.title, count(*) from scholars GROUP by scholars.title")
    title_dist = cur.fetchall()

    title_dist_org = dict()
    title_dist_org['ARAŞTIRMA GÖREVLİSİ'] = title_dist[0][1]
    title_dist_org['ÖĞRETİM GÖREVLİSİ'] = title_dist[5][1] + title_dist[8][1] + title_dist[9][1]
    title_dist_org['DOKTOR ÖĞRETİM ÜYESİ'] = title_dist[3][1]
    title_dist_org['DOÇENT'] = title_dist[2][1] + title_dist[4][1] + title_dist[6][1] + title_dist[7][1]
    title_dist_org['PROFESÖR'] = title_dist[10][1]

    cur.execute("SELECT scholars.title, scholars.field, count(*) from scholars GROUP by scholars.title, scholars.field order by scholars.field")
    field_dist = cur.fetchall()
    field_dist_org = title_organizer(field_dist)

    cur.execute("SELECT scholars.title, count(*) from scholars join articles on scholars.id = articles.id GROUP by scholars.title order by scholars.title")
    article_query = cur.fetchall()
    cur.execute("SELECT scholars.title, count(*) from scholars join conferences on scholars.id = conferences.id GROUP by scholars.title order by scholars.title")
    conference_query = cur.fetchall()
    cur.execute("SELECT scholars.title, count(*) from scholars join projects on scholars.id = projects.id GROUP by scholars.title order by scholars.title")
    project_query = cur.fetchall()
    cur.execute("SELECT scholars.title, count(*) from scholars join supervised_thesises on scholars.id = supervised_thesises.id GROUP by scholars.title order by scholars.title")
    thesis_query = cur.fetchall()

    cur.execute("SELECT scholars.title, supervised_thesises.degree_name, count( * ) from scholars join supervised_thesises on scholars.id = supervised_thesises.id GROUP by scholars.title, supervised_thesises.degree_name order by scholars.title desc")
    thesis_by_degree_query = cur.fetchall()

    articles_by_title = work_organizer(article_query)
    conference_by_title = work_organizer(conference_query)
    project_by_title = work_organizer(project_query)
    thesis_by_title = work_organizer(thesis_query)

    thesis_by_degree = supervised_thesis_organizer(thesis_by_degree_query)

    # plotter.plot_scholars_by_title(title_dist_org)
    #plotter.average_of_university(title_dist_org)
    # plotter.plot_scholars_by_field(field_dist_org)
    #plotter.plot_works_by_title(articles_by_title, conference_by_title, project_by_title, thesis_by_title, title_dist_org)
    # plotter.plot_supervised_theses_by_degree(thesis_by_degree, title_dist_org)