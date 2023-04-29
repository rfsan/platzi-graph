import shutil
from pathlib import Path
from typing import Optional

import pandas as pd

file_ids = dict()


def get_file_id(k: str):
    file_id = file_ids.get(k, None)
    if not file_id:  # generate id and save it
        file_id = len(file_ids)
        file_ids[k] = file_id
    return file_id


def get_metadata_string(
    title: str, id: int, type: str, tags: Optional[list[str]] = None
) -> str:
    tags_md = f"tags: [{','.join(tags)}]\n" if tags else ""
    metadata = f"---\ntitle: {title}\nid: {id}\ntype: {type}\n{tags_md}---\n"
    return metadata


def create_categories_files(df: pd.DataFrame):
    categories = df["category"].unique()
    for category in categories:
        category_id = get_file_id(f"category_{category}")
        sub_df = df[df["category"] == category]
        tracks_md = []
        tracks = sub_df["track_name"].unique()
        for track in tracks:
            track_id = get_file_id(f"track_{track}")
            tracks_md.append(f"- [[{track_id}|{track}]]")
        courses_md = []
        courses = sub_df["course_name"].unique()
        for course in courses:
            course_id = get_file_id(f"course_{course}")
            courses_md.append(f"- [[{course_id}|{course}]]")
        metadata = get_metadata_string(category, category_id, "category")
        content = "## Escuelas y rutas\n"
        content += "\n".join(tracks_md)
        content += "\n## Cursos\n"
        content += "\n".join(courses_md)
        with open(f"vault/{category}.category.md", "w") as md_file:
            md_file.write(metadata + content)


def create_tracks_files(df: pd.DataFrame):
    tracks = df["track_name"].unique()
    for track in tracks:
        track_id = get_file_id(f"track_{track}")
        courses_md = []
        courses = df[df["track_name"] == track]["course_name"].unique()
        for course in courses:
            course_id = get_file_id(f"course_{course}")
            courses_md.append(f"- [[{course_id}|{course}]]")
        metadata = get_metadata_string(track, track_id, "track")
        content = "\n## Cursos\n"
        content += "\n".join(courses_md)
        with open(f"vault/{track}.track.md", "w") as md_file:
            md_file.write(metadata + content)


def create_courses_files(df: pd.DataFrame):
    courses = df["course_name"].unique()
    for course in courses:
        professor = (
            df[df["course_name"] == course]["course_professor"].unique().tolist()
        )
        course_id = get_file_id(f"course_{course}")
        metadata = get_metadata_string(course, course_id, "course", tags=professor)
        with open(f"vault/{course}.course.md", "w") as md_file:
            md_file.write(metadata)


def main():
    vault_dir = Path("./vault")
    if vault_dir.exists():
        shutil.rmtree(vault_dir)
    vault_dir.mkdir()
    df = pd.read_csv("./data/platzi_course_data.csv")
    format_columns = ["category", "track_name", "course_name"]
    df[format_columns] = df[format_columns].applymap(
        lambda s: "".join([x if x.isalnum() else "_" for x in s])
    )
    create_categories_files(df)
    create_tracks_files(df)
    create_courses_files(df)


if __name__ == "__main__":
    main()
