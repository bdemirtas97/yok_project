import psycopg2

def create_tables():
    conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS scholars(
                id integer primary key,
                title varchar(600) not null,
                name varchar(600) not null,
                university varchar(600) not null,
                field varchar(600),
                department varchar(600)

    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS posts(
                id integer references scholars,
                post varchar(600) not null,
                year varchar(600) not null,
                university varchar(600),
                department varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS degrees(
                id integer references scholars,
                degree varchar(600) not null,
                years varchar(600) not null,
                university varchar(600),
                department varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS books(
                id integer references scholars,
                name varchar(1000) not null,
                year integer,
                category varchar(600),
                scope varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS articles(
                id integer references scholars,
                title varchar(1000) not null,
                national varchar(600),
                referee varchar(600),
                index varchar(600),
                category varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS conferences(
                id integer references scholars,
                title varchar(1000) not null,
                national varchar(600),
                category varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                id integer references scholars,
                title varchar(1000) not null,
                funder varchar(600),
                institution varchar(600),
                complete varchar(600)      
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS lectures(
                id integer references scholars,
                term varchar(600),
                name varchar(600),
                language varchar(600),
                hours integer,
                level_name varchar(600)     
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS supervised_thesises(
                id integer references scholars,
                degree_name varchar(1000),
                year integer,
                writer varchar(600),
                title varchar(600),
                university varchar(600)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS rewards(
                id integer references scholars,
                title varchar(1000) not null,
                institution varchar(600),
                detail varchar(600),
                year integer     
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS patents(
                id integer references scholars,
                name varchar(1000) not null,
                category varchar(600),
                section varchar(600) 
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS memberships(
                id integer references scholars,
                institution varchar(600) not null,
                role varchar(600),
                year integer     
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS artistic_activities(
                id integer references scholars,
                name varchar(1000) not null,
                national varchar(600),
                category varchar(600),
                dates varchar(600)     
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS administrative_duties(
                id integer references scholars,
                title varchar(600) not null,
                years varchar(600),
                university varchar(600),
                department varchar(600)   
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS non_college_experience(
                id integer references scholars,
                institution varchar(600),
                title varchar(1000) not null,
                dates varchar(600),
                scope varchar(600)    
    );""")

    conn.commit()
    cur.close()
    conn.close()

def insert_scholar(scholar):
    conn = psycopg2.connect("dbname=Scholars_Updated user=postgres password=root host=localhost port=5432")
    cur = conn.cursor()
    

    cur.execute("INSERT INTO scholars (id, title, name, university, field, department) VALUES (%s, %s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), scholar["title"], scholar["name"], scholar["university"], scholar["field"], scholar["department"]))

    for post in scholar["posts"]:
        cur.execute("INSERT INTO posts (id, post, year, university, department) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), post["post"], post["year"], post["university"], post["department"]))
        
    for degree in scholar["degrees"]:
        cur.execute("INSERT INTO degrees (id, degree, years, university, department) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), degree["degree"], degree["years"], degree["university"], degree["department"]))
        
    for book in scholar["books"]:
        cur.execute("INSERT INTO books (id, name, year, category, scope) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), book["name"], int(book["year"]), book["category"], book["scope"]))
        
    for article in scholar["articles"]:
        cur.execute("INSERT INTO articles (id, title, national, referee, index, category) VALUES (%s, %s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), article["title"], article["national"], article["referee"], article["index"], article["category"]))
        
    for paper in scholar["papers"]:
        cur.execute("INSERT INTO conferences (id, title, national, category) VALUES (%s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), paper["title"], paper["national"], paper["category"]))
        
    for project in scholar["projects"]:
        cur.execute("INSERT INTO projects (id, title, funder, institution, complete) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), project["title"], project["hirer"], project["institution"], project["complete"]))
        
    for lecture in scholar["lectures"]:
        cur.execute("INSERT INTO lectures (id, term, name, language, hours, level_name) VALUES (%s, %s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), lecture["term"], lecture["name"], lecture["language"], 0 if lecture["hours"] == '' else int(lecture["hours"]), lecture["level_name"]))
        
    for thesis in scholar["supervised_thesises"]:
        cur.execute("INSERT INTO supervised_thesises (id, degree_name, year, writer, title, university) VALUES (%s, %s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), thesis["degree_name"], int(thesis["year"]), thesis["writer"], thesis["title"], thesis["university"]))
        
    for reward in scholar["rewards"]:
        cur.execute("INSERT INTO rewards (id, title, institution, detail, year) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), reward["title"], reward["institution"], reward["detail"], int(reward["year"])))
        
    for patent in scholar["patents"]:
        cur.execute("INSERT INTO patents (id, name, category, section) VALUES (%s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), patent["name"], patent["category"], patent["section"]))
        
    for membership in scholar["memberships"]:
        cur.execute("INSERT INTO memberships (id, institution, role, year) VALUES (%s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), membership["institution"], membership["role"], int(membership["year"])))
        
    for activity in scholar["artistic_activities"]:
        cur.execute("INSERT INTO artistic_activities (id, name, national, category, dates) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), activity["name"], activity["national"], activity["category"], activity["dates"]))
        
    for duty in scholar["administrative_duties"]:
        cur.execute("INSERT INTO administrative_duties (id, title, years, university, department) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), duty["title"], duty["years"], duty["university"], duty["department"]))
        
    for experience in scholar["non_college_experience"]:
        cur.execute("INSERT INTO non_college_experience (id, institution, title, dates, scope) VALUES (%s, %s, %s, %s, %s)", 
                (int(scholar["scholar_id"]), experience["institution"], experience["title"], experience["dates"], experience["scope"]))
        
    conn.commit()
    cur.close()
    conn.close()
    