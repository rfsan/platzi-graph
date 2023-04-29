# Plazti Graph

## .GIF.

## How to generate the graph

1. Install Python dependencies `pip install -r requirements.txt`
1. Download the data in .csv file format  `python download_courses_data.py`
    - (optional) Generate a .xlsx file to explore more easily Platzi's courses `python generate_xlsx.py`
1. Generate the markdown files needed to create graph `python generate_markdown_files.py`
1. Install Node dependencies `npm install`
1. Generate the HTML with the graph `npm run graph`
1. To see the graph copy the complete path of the file `cosmoscope.html` and paste it in the URL search bar of your browser.

## Useful links

- [Cosma CLI Docs](https://cosma.graphlab.fr/en/docs/cli/user-manual/)
- [Platzi color palette](https://platzi.com/tutoriales/1228-fundamentos-diseno/7447-sabes-cuales-son-los-colores-de-platzi/)