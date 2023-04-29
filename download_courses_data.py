from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


def format_text(text: str) -> str:
    text = text.replace("\n", " ").strip(" ")
    text = " ".join(text.split())  # multiple whitespaces to only one
    return text


def main():
    # download HTML
    url = "https://platzi.com/cursos/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # transform HTML to tabular data
    data = list()
    base_url = "https://platzi.com"
    categories = soup.find_all("div", class_="Categories-item")
    for category in categories:
        category_name = format_text(category.h2.get_text())
        schools = category.find_all("div", class_="School")
        for school in schools:
            school_name = format_text(school.h3.get_text())
            school_url = base_url + school.find("a", class_="School-header-link").get(
                "href"
            )
            is_school = "escuela" in school_url
            courses = school.find_all("a", class_="Course")
            for course in courses:
                course_name = format_text(course.h4.get_text())
                course_url = base_url + course.get("href")
                course_prof = format_text(course.p.get_text().replace("Por ", ""))
                is_audio_course = course_name.lower().startswith("audio")
                data.append(
                    [
                        category_name,
                        school_name,
                        school_url,
                        is_school,
                        course_name,
                        course_url,
                        course_prof,
                        is_audio_course,
                    ]
                )

    df = pd.DataFrame(
        data,
        columns=[
            "category",
            "school_name",
            "school_url",
            "is_school",
            "course_name",
            "course_url",
            "course_professor",
            "is_audio_course",
        ],
    )

    # some category-school-course combinations are repeated
    df = df.drop_duplicates()

    Path("./data").mkdir(exist_ok=True)
    df.to_csv("data/platzi_course_data.csv", index=False)


if __name__ == "__main__":
    main()
