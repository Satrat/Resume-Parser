# Resume-Parser
Analyze, score and rank a collection of PDF resumes using machine learning

Merit | Edge Resume Parser and Scorer

### Dependencies
* Must have Latex installed!
* pdfquery (`pip install pdfquey`)
* pdfminer (`pip install pdfminer`)

Our resume parser and scorer use these components to create a Latex .pdf file of results:
- Category score (what field your resume seems best suited for)
- Overall score (how well your resume scored across different fields)
- University score (how high your school is ranked)
- GPA score (how high your GPA is)
- Word count (if your resume has too few words or too many words)
- Word count per section, i.e. Experience, Leadership, and/or Projects
- Degree score (if you have a degree required for the position - mostly based on user input)

### How to Use
```
python cvparseV2.py
```
By running this program, you will be able to produce a Latex file with these results filed by resume email and will also have a total score at the bottom.

Created by: Sara Adkins, Ashley Wong, Jonathan Merrin, Nazli Uzgur for YHacks 2015
