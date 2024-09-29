def get_personal_info(tree, scholar):
        id_tag = tree.css_first("span.pull-right.greenOrcid")
        id = id_tag.text(deep=False).split(':')[1].strip()
        scholar["scholar_id"] = id

        authorInfoTable = tree.css_first("#authorlistTb")

        scholar["name"] = authorInfoTable.css_first("h4").text()
        scholar["title"] = authorInfoTable.css_first("h6").text()
        field_tag = authorInfoTable.css_first("span.label-success")
        scholar["field"] = field_tag.text() if field_tag != None else None
        department_tag = authorInfoTable.css_first("span.label-primary")
        scholar["department"] = department_tag.text() if department_tag != None else None

        post_and_edu_info = tree.css(".col-md-6 .timeline")

        post_year_tags = post_and_edu_info[0].css(".bg-light-blue")
        post_tags = post_and_edu_info[0].css(".btn-success.btn-xs")
        post_detail_tags = post_and_edu_info[0].css(".timeline-item")

        edu_year_tags = post_and_edu_info[1].css(".bg-light-blue")
        edu_tags = post_and_edu_info[1].css(".btn-info.btn-xs")
        edu_detail_tags = post_and_edu_info[1].css(".timeline-item")

        scholar["posts"] = list()
        scholar["degrees"] = list()

        for i in range(len(post_tags)):
            scholar["posts"]+=[
                {
                    "post": post_tags[i].text(),
                    "year": post_year_tags[i].text(),
                    "university": post_detail_tags[i].css_first("h4").text(),
                    "department": post_detail_tags[i].css_first("div > h5").text(),
                }
            ]

        for i in range(len(edu_tags)):
            scholar["degrees"]+=[
                {
                        "degree": edu_tags[i].text(),
                        "years": edu_year_tags[i].text().strip(),
                        "university": edu_detail_tags[i].css_first("h4").text(),
                        "department": edu_detail_tags[i].css_first("div > h5").text(),
                }
            ]

def get_books(tree, scholar):
    book_nodes = tree.css(".projects > .row")

    scholar["books"] = list()

    for node in book_nodes:
        name_tag = node.css_first("strong")
        year_tag = node.css_first(".label-info")
        if year_tag == None: return
        category_tag = node.css_first(".label-primary")
        scope_tag = node.css_first(".label-success")

        scholar["books"] += [
            {
                "name": name_tag.text().split(".")[1].strip(),
                "year": year_tag.text().strip(),
                "category": None if category_tag == None else category_tag.text().strip(),
                "scope": None if scope_tag == None else scope_tag.text().strip(),
            }
        ]

def get_articles(tree, scholar):
    article_nodes = tree.css_first(".searchable").css("tr > td:nth-child(2)")

    scholar["articles"] = list()

    for node in article_nodes:
        title_tag = node.css_first("a")
        national_tag = node.css_first(".label-info")
        referee_tag = node.css_first(".label-primary")
        index_tag = node.css_first(".label-success")
        category_tag = node.css_first(".label-default")

        scholar["articles"] += [
             {
                  "title": title_tag.text().strip(),
                  "national": None if national_tag == None else national_tag.text().strip(),
                  "referee": None if referee_tag == None else referee_tag.text().strip(),
                  "index": None if index_tag == None else ' '.join(index_tag.text().strip().split("\n")),
                  "category": None if category_tag == None else category_tag.text().strip(),
             }
        ]


def get_papers(tree, scholar):
     paper_nodes = tree.css_first(".searchable").css("tr > td:nth-child(2)")

     scholar["papers"] = list()

     for node in paper_nodes:
          title_tag = node.css_first("a")
          national_tag = node.css_first(".label-info")
          category_tag = node.css_first(".label-success")

          scholar["papers"] += [
             {
                  "title": title_tag.text().strip(),
                  "national": national_tag.text().strip(),
                  "category": None if category_tag == None else category_tag.text().strip()
             }
        ]
          
def get_projects(tree, scholar):
     project_nodes = tree.css(".projects .projectmain")

     scholar["projects"] = list()

     for node in project_nodes:
          title_tag = node.css_first("strong")
          hirer_tag = node.css_first(".label-primary")
          institution_tag = node.css_first(".label-default")
          complete_tag = node.css_first(".label-success")

          scholar["projects"] += [
               {
                    "title": title_tag.text(),
                    "hirer": None if hirer_tag == None or hirer_tag.text() == "" else hirer_tag.text(),
                    "institution": None if institution_tag == None or institution_tag.text() == "" else institution_tag.text(),
                    "complete": None if complete_tag == None or complete_tag.text() == "" else complete_tag.text(),
               }
          ]

def get_lectures(tree, scholar):
     levels = tree.css(".panel-default")

     scholar["lectures"] = list()

     for level in levels:
          level_name = level.css_first("a").text().strip()
          lectures = level.css("tbody > tr")

          for lecture in lectures:
               scholar["lectures"] += [
                    {
                         "term": lecture.css_first("td:nth-child(1)").text(),
                         "name": lecture.css_first("td:nth-child(2)").text(),
                         "language": lecture.css_first("td:nth-child(3)").text(),
                         "hours": lecture.css_first("td:nth-child(4)").text(),
                         "level_name": level_name,
                    }
               ]

def get_supervised_thesises(tree, scholar):
     degrees = tree.css(".panel-default")

     scholar["supervised_thesises"] = list()

     for degree in degrees:
          degree_name = degree.css_first("a").text().strip()
          thesises = degree.css("tbody > tr")

          for thesis in thesises:
               thesis_tag = thesis.css_first("td:nth-child(3) > a") or thesis.css_first("td:nth-child(3)")
               scholar["supervised_thesises"] += [
                    {
                         "year": thesis.css_first("td:nth-child(1)").text(),
                         "writer": thesis.css_first("td:nth-child(2)").text(),
                         "title": thesis_tag.text(),
                         "university": thesis.css_first("td:nth-child(4)").text(),
                         "degree_name": degree_name
                    }
               ]

def get_rewards(tree, scholar):
     reward_nodes = tree.css("ul.timeline > li")

     scholar["rewards"] = list()
     current_year = None

     def detail_extractor(str):
          words = str.split("\n")
          return words[1].strip() + words[2].strip()

     for node in reward_nodes:
          title_tag = node.css_first(".timeline-title")
          institution_tag = node.css_first(".text-muted")
          detail_tag = node.css_first(".timeline-body > p")
          year_tag = node.css_first(".timeline-badge")
          if(year_tag != None): current_year = year_tag.text()

          scholar["rewards"] += [
               {
                    "title": title_tag.text(),
                    "institution": None if institution_tag == None else institution_tag.text(),
                    "detail": None if detail_tag == None else detail_extractor(detail_tag.text()),
                    "year": current_year
               }
          ]

def get_patents(tree, scholar):
     patent_nodes = tree.css(".projects .projectmain")

     scholar["patents"] = list()

     for node in patent_nodes:
          scholar["patents"] += [
               {
                    "name": node.css_first(".projectTitle > strong").text(),
                    "category": node.css_first(".projectType > .label-info").text(),
                    "section": node.css_first(".projectType > .label-success").text().strip(),
               }
          ]

def get_memberships(tree, scholar):
     membership_nodes = tree.css("#callout-stacked-modals")

     scholar["memberships"] = list()

     for node in membership_nodes:
          role_and_year = node.css_first("p").text().split("\n")
          role = role_and_year[0]
          year = role_and_year[1]
          scholar["memberships"] += [
               {
                    "institution": node.css_first("h4").text(),
                    "role": role,
                    "year": year,
               }
          ]

def get_artistic_activities(tree, scholar):
     activity_nodes = tree.css(".listRowmain")

     scholar["artistic_activities"] = list()

     def date_extractor(str):
          words = str.split("\n")
          return words[0] + words[1].strip()
     

     for node in activity_nodes:
          dates_raw = node.css_first(".listRowAuthor > .label-info").text()
          dates = None if dates_raw == "" else date_extractor(dates_raw)
          scholar["artistic_activities"] += [
               {
                    "name": node.css_first("h5").text(),
                    "national": node.css_first(".label-info").text(),
                    "category": node.css_first(".label-primary").text(),
                    "dates": dates,
               }
          ]

def get_administrative_duties(tree, scholar):
     years = tree.css(".bg-light-blue")
     titles = tree.css(".btn-success")
     details = tree.css(".timeline-item")

     scholar["administrative_duties"] = list()

     for i in range(len(years)):
          scholar["administrative_duties"] += [
               {
                    "title": titles[i].text(),
                    "years": years[i].text().strip(),
                    "university": details[i].css_first("h4").text().strip(),
                    "department": details[i].css_first("h5").text().strip(),
               }
          ]

def get_non_college_experience(tree, scholar):
     experience_nodes = tree.css(".listRowmain")

     scholar["non_college_experience"] = list()

     for node in experience_nodes:
          scholar["non_college_experience"] += [
               {
                    "institution": node.css_first("h5").text(),
                    "title": node.css_first("strong").text(),
                    "dates": node.css_first(".label-info").text().strip(),
                    "scope": node.css_first(".label-primary").text(),
               }
          ]