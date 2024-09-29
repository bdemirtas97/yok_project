import matplotlib.pyplot as plt
import numpy as np

def plot_scholars_by_title(title_dist_org):
    titles = list(title_dist_org.keys())
    counts = list(title_dist_org.values())

    plt.figure(figsize=(10, 6))
    plt.bar(titles, counts, color='skyblue')
    plt.xlabel('Title')
    plt.ylabel('Number of Scholars')
    plt.title('Number of Scholars by Title')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def average_of_university(title_dist_org):
    titles = list(title_dist_org.keys())
    counts = list(title_dist_org.values())

    for i in range(len(counts)):
        counts[i] = counts[i]/205

    plt.figure(figsize=(10, 6))
    plt.bar(titles, counts, color='skyblue')
    plt.xlabel('Title')
    plt.ylabel('Number of Scholars')
    plt.title('Average Scholar Distribution of a University')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_scholars_by_field(field_dist_org):
    fields = list(field_dist_org.keys())
    positions = np.arange(len(fields))
    width = 0.15

    prof_counts = [field_dist_org[field]["PROFESÖR"] for field in fields]
    doc_counts = [field_dist_org[field]["DOÇENT"] for field in fields]
    doc_og_counts = [field_dist_org[field]["DOKTOR ÖĞRETİM ÜYESİ"] for field in fields]
    og_counts = [field_dist_org[field]["ÖĞRETİM GÖREVLİSİ"] for field in fields]
    ar_counts = [field_dist_org[field]["ARAŞTIRMA GÖREVLİSİ"] for field in fields]

    plt.figure(figsize=(14, 8))
    plt.bar(positions - 2*width, prof_counts, width, label='PROFESÖR')
    plt.bar(positions - width, doc_counts, width, label='DOÇENT')
    plt.bar(positions, doc_og_counts, width, label='DOKTOR ÖĞRETİM ÜYESİ')
    plt.bar(positions + width, og_counts, width, label='ÖĞRETİM GÖREVLİSİ')
    plt.bar(positions + 2*width, ar_counts, width, label='ARAŞTIRMA GÖREVLİSİ')

    plt.xlabel('Field')
    plt.ylabel('Number of Scholars')
    plt.title('Number of Scholars by Field and Title')
    plt.xticks(positions, fields, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_works_by_title(articles_by_title, conference_by_title, project_by_title, thesis_by_title, title_dist):
    titles = list(title_dist.keys())
    articles = [articles_by_title[title] / title_dist[title] for title in titles]
    conferences = [conference_by_title[title] / title_dist[title] for title in titles]
    projects = [project_by_title[title] / title_dist[title] for title in titles]
    theses = [thesis_by_title[title] / title_dist[title] for title in titles]

    positions = np.arange(len(titles))
    width = 0.2

    plt.figure(figsize=(14, 8))
    plt.bar(positions - 1.5*width, articles, width, label='Articles')
    plt.bar(positions - 0.5*width, conferences, width, label='Conferences')
    plt.bar(positions + 0.5*width, projects, width, label='Projects')
    plt.bar(positions + 1.5*width, theses, width, label='Supervised Theses')

    plt.xlabel('Title')
    plt.ylabel('Number')
    plt.title('Articles, Conferences, Projects, and Supervised Theses by Title')
    plt.xticks(positions, titles, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_supervised_theses_by_degree(thesis_by_degree, title_dist):
    titles = list(title_dist.keys())
    yl_counts = [thesis_by_degree[title]["Yüksek Lisans"] / title_dist[title] for title in titles]
    dr_counts = [thesis_by_degree[title]["Doktora"] / title_dist[title] for title in titles]

    positions = np.arange(len(titles))
    width = 0.35

    plt.figure(figsize=(14, 8))
    plt.bar(positions - width/2, yl_counts, width, label='Yüksek Lisans')
    plt.bar(positions + width/2, dr_counts, width, label='Doktora')

    plt.xlabel('Title')
    plt.ylabel('Number of Theses')
    plt.title('Supervised Theses by Degree and Title')
    plt.xticks(positions, titles, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()


def average_num_of_scholars(group1_param, group2_param, num_of_universities, title, labels):
    group1 = {title: count / num_of_universities for title, count in group1_param.items()}
    group2 = {title: count / num_of_universities for title, count in group2_param.items()}

    # Plotting the data
    titles = list(group1.keys())
    group1_values = list(group1.values())
    group2_values = list(group2.values())

    x = range(len(titles))

    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x, group1_values, width=0.4, label=labels[0], align='center')
    bars2 = plt.bar(x, group2_values, width=0.4, label=labels[1], align='edge')

    plt.xticks(x, titles)
    plt.xlabel('Title')
    plt.ylabel('Average Number per University')
    plt.title(title)
    plt.legend()
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width(), yval + 0.5, round(yval, 2), ha='center', va='bottom')

    plt.show()

#def compare_works_by_title(scholars_work, title_dist):
def compare_works_by_title(scholars_work1, title_dist1, scholars_work2, title_dist2):
    # Plot for scholar set 1
    titles = list(title_dist1.keys())
    articles1 = [(scholars_work1["articles"][title] - scholars_work2["articles"][title]) / (title_dist1[title] - title_dist2[title]) for title in titles]
    conferences1 = [(scholars_work1["conferences"][title] - scholars_work2["conferences"][title]) / (title_dist1[title] - title_dist2[title]) for title in titles]
    projects1 = [(scholars_work1["projects"][title] - scholars_work2["projects"][title]) / (title_dist1[title] - title_dist2[title]) for title in titles]
    books1 = [(scholars_work1["books"][title] - scholars_work2["books"][title]) / (title_dist1[title] - title_dist2[title]) for title in titles]
    positions = np.arange(len(titles))
    width = 0.2

    plt.figure(figsize=(14, 16))  # Increased height for both plots
    plt.subplot(2, 1, 1)  # First plot (2 rows, 1 column, 1st plot)
    bars1 = plt.bar(positions - 1.5 * width, articles1, width, label='Articles')
    bars2 = plt.bar(positions - 0.5 * width, conferences1, width, label='Conferences')
    bars3 = plt.bar(positions + 0.5 * width, projects1, width, label='Projects')
    bars4 = plt.bar(positions + 1.5 * width, books1, width, label='Books')

    plt.xlabel('Title')
    plt.ylabel('Number')
    plt.title('Scholar Set 1: Articles, Conferences, Projects, and Books by Title')
    plt.xticks(positions, titles, rotation=45, ha='right')
    plt.legend()
    
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    # If a second set of data is provided, plot the second chart
    titles2 = list(title_dist2.keys())
    articles2 = [scholars_work2["articles"][title] / title_dist2[title] for title in titles2]
    conferences2 = [scholars_work2["conferences"][title] / title_dist2[title] for title in titles2]
    projects2 = [scholars_work2["projects"][title] / title_dist2[title] for title in titles2]
    books2 = [scholars_work2["books"][title] / title_dist2[title] for title in titles2]

    positions2 = np.arange(len(titles2))

    plt.subplot(2, 1, 2)  # Second plot (2 rows, 1 column, 2nd plot)
    bars1 = plt.bar(positions2 - 1.5 * width, articles2, width, label='Articles')
    bars2 = plt.bar(positions2 - 0.5 * width, conferences2, width, label='Conferences')
    bars3 = plt.bar(positions2 + 0.5 * width, projects2, width, label='Projects')
    bars4 = plt.bar(positions2 + 1.5 * width, books2, width, label='Books')

    plt.xlabel('Title')
    plt.ylabel('Number')
    plt.title('Scholar Set 2: Articles, Conferences, Projects, and Books by Title')
    plt.xticks(positions2, titles2, rotation=45, ha='right')
    plt.legend()

    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
    # titles = list(title_dist.keys())
    # articles = [scholars_work["articles"][title] / title_dist[title] for title in titles]
    # conferences = [scholars_work["conferences"][title] / title_dist[title] for title in titles]
    # projects = [scholars_work["projects"][title] / title_dist[title] for title in titles]
    # books = [scholars_work["books"][title] / title_dist[title] for title in titles]

    # positions = np.arange(len(titles))
    # width = 0.2

    # plt.figure(figsize=(14, 8))
    # bars1 = plt.bar(positions - 1.5*width, articles, width, label='Articles')
    # bars2 = plt.bar(positions - 0.5*width, conferences, width, label='Conferences')
    # bars3 = plt.bar(positions + 0.5*width, projects, width, label='Projects')
    # bars4 = plt.bar(positions + 1.5*width, books, width, label='Books')

    # plt.xlabel('Title')
    # plt.ylabel('Number')
    # plt.title('Articles, Conferences, Projects, and Supervised Theses by Title')
    # plt.xticks(positions, titles, rotation=45, ha='right')
    # plt.legend()
    # for bar in bars1:
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    # for bar in bars2:
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width(), yval + 0.5, round(yval, 2), ha='center', va='bottom')
    # for bar in bars3:
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')
    # for bar in bars4:
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width(), yval + 0.5, round(yval, 2), ha='center', va='bottom')
    # plt.tight_layout()
    # plt.show()
