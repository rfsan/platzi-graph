import pandas as pd


def md_list(s: pd.Series) -> str:
    """Return a markdown list"""
    return "- " + "\n- ".join(s.unique())


def main():
    df = pd.read_csv("./data/platzi_course_data.csv")
    df_courses = df.groupby(["course_name", "course_professor"], as_index=False).agg(
        school_list=("school_name", md_list),
        categories=("category", md_list),
        url=("course_url", lambda x: x.mode()),
    )

    df_schools = df.groupby("school_name", as_index=False).agg(
        course_count=("course_name", lambda x: len(x.unique())),
        course_list=("course_name", md_list),
        categories=("category", md_list),
        url=("school_url", lambda x: x.mode()),
    )

    with pd.ExcelWriter("./data/cursos_platzi.xlsx", mode="w") as writer:
        df_courses.rename(
            columns={
                "course_name": "Curso",
                "course_professor": "Profesor",
                "school_list": "Escuelas y Rutas a las que pertenece",
                "categories": "Categorías",
                "url": "Link de la primera clase",
            }
        ).to_excel(writer, sheet_name="Cursos", index=False)
        df_schools.rename(
            columns={
                "school_name": "Nombre",
                "course_count": "Cantidad de cursos",
                "course_list": "Cursos",
                "categories": "Categorías",
                "url": "Link",
            }
        ).to_excel(writer, sheet_name="Escuelas y Rutas", index=False)


if __name__ == "__main__":
    main()
