import psycopg2
import plotter

def fetch_data(query):
    cur.execute(query)
    raw_data = cur.fetchall()
    return dict((x,y) for x, y in raw_data)

conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
cur = conn.cursor()

num_of_departments_query = cur.execute("SELECT COUNT(DISTINCT department) FROM scholars")
num_of_departments = cur.fetchone()[0]
num_of_universities_query = cur.execute("SELECT COUNT(DISTINCT university) FROM scholars")
num_of_universities = cur.fetchone()[0]

#Queris for different departments
all_scholars = fetch_data("SELECT scholars.title, count(*) from scholars GROUP by scholars.title")
cmp_scientists = fetch_data("SELECT scholars.title, count(*) from scholars WHERE scholars.department = 'Bilgisayar Bilimleri ve Mühendisliği' GROUP BY scholars.title")
elec_scientists = fetch_data("SELECT scholars.title, count(*) from scholars WHERE scholars.department = 'Elektrik-Elektronik ve Haberleşme Mühendisliği' or scholars.department = 'Elektrik-Elektronik Mühendisliği' GROUP BY scholars.title")


# Queries for different categories of work
all_scholars_work = {
    "articles": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN articles ON scholars.id = articles.id GROUP BY scholars.title"),
    "conferences": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN conferences ON scholars.id = conferences.id GROUP BY scholars.title"),
    "projects": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN projects ON scholars.id = projects.id GROUP BY scholars.title"),
    "books": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN books ON scholars.id = books.id GROUP BY scholars.title")
}

cmp_scientists_work = {
    "articles": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN articles ON scholars.id = articles.id WHERE scholars.department = 'Bilgisayar Bilimleri ve Mühendisliği' GROUP BY scholars.title"),
    "conferences": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN conferences ON scholars.id = conferences.id WHERE scholars.department = 'Bilgisayar Bilimleri ve Mühendisliği' GROUP BY scholars.title"),
    "projects": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN projects ON scholars.id = projects.id WHERE scholars.department = 'Bilgisayar Bilimleri ve Mühendisliği' GROUP BY scholars.title"),
    "books": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN books ON scholars.id = books.id WHERE scholars.department = 'Bilgisayar Bilimleri ve Mühendisliği' GROUP BY scholars.title")
}

elec_scientists_work = {
    "articles": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN articles ON scholars.id = articles.id WHERE scholars.department = 'Elektrik-Elektronik Mühendisliği' OR scholars.department = 'Elektrik-Elektronik ve Haberleşme Mühendisliği' GROUP BY scholars.title"),
    "conferences": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN conferences ON scholars.id = conferences.id WHERE scholars.department = 'Elektrik-Elektronik Mühendisliği' OR scholars.department = 'Elektrik-Elektronik ve Haberleşme Mühendisliği' GROUP BY scholars.title"),
    "projects": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN projects ON scholars.id = projects.id WHERE scholars.department = 'Elektrik-Elektronik Mühendisliği' OR scholars.department = 'Elektrik-Elektronik ve Haberleşme Mühendisliği' GROUP BY scholars.title"),
    "books": fetch_data("SELECT scholars.title, count(*) FROM scholars JOIN books ON scholars.id = books.id WHERE scholars.department = 'Elektrik-Elektronik Mühendisliği' OR scholars.department = 'Elektrik-Elektronik ve Haberleşme Mühendisliği' GROUP BY scholars.title")
}

#plotter.average_num_of_scholars(all_scholars, cmp_scientists, num_of_universities, "Average Number of All Scholars vs Computer Scientists per University (by Title)", ('Average Scholars','Average Computer Scientists'))
#plotter.average_num_of_scholars(all_scholars, elec_scientists, num_of_universities, "Average Number of All Scholars and Electronic Engineers per University (by Title)", ('Average Scholars', 'Average Electronic Engineers'))
#plotter.average_num_of_scholars(cmp_scientists, elec_scientists, num_of_universities, "Average Number of Computer Scientists vs Electronic Engineers per University (by Title)", ('Average Computer Scientists', 'Average Electronic Engineers'))
#plotter.compare_works_by_title(all_scholars_work, all_scholars, cmp_scientists_work, cmp_scientists)
#plotter.compare_works_by_title(all_scholars_work, all_scholars, elec_scientists_work, elec_scientists)
#plotter.compare_works_by_title(cmp_scientists_work, cmp_scientists, elec_scientists_work, elec_scientists)

cur.close()
conn.close()