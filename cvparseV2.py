## Nazli Uzgur
## Sara Adkins
## Jonathan Merron
## Ashley Wong

from __future__ import with_statement # for Python 2.5 and 2.6
import urllib
import re, collections
import os
import tokenize
import pdftotextmaybe
import getCategory
import difflib
import subprocess

def init():

    ############################################################
    ### Convert pdf to txt with pdf miner and start a write file
    ############################################################

    # input the file name
    filename = raw_input("Enter the name of a resume file or \
directory containing resumes: \n")

    cats = ["Programming Languages", "Computer Science", "Engineering", "Finance", "Business Management", "the Arts"]
    for i in range(len(cats)):
        path = raw_input("Please type the name of a file containing all keywords associated with "+ cats[i] + ' separated by line\n\
(leave blank for defaults)\n')
        if(path == ""):
            cats[i] = None
        else:
            with open(path, "r") as fin:
                cats[i] = fin.read().splitlines()
    
    # creates an empty tex file with the results in it
    fout = open("results.tex", "w")
    fout.write("\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\
\\title{Results}\n\\begin{document}\n\n")
    fout.close()

    # need this to work in case no input
    if filename == " ":
        return ("", "")
    elif os.path.isdir(filename):
        resumes = []
        for doc in os.listdir(filename):
            if doc.endswith(".pdf"):
                resume = pdftotextmaybe.convert(os.path.join(filename,doc))
                resumes.append(resume)
            else:
                resume = readFile(os.path.join(filename,doc)).lower()
                resumes.append(resume)
        return (resumes, cats)
    # is .pdf; need to convert to .txt    
    elif filename.endswith(".pdf"):
        resume = pdftotextmaybe.convert(filename)
    else: 
        resume = readFile(filename).lower()
    # return resume as a string with different sections

    return (resume, cats)

def category(resume, progWords = None, csWords = None, engWords = None, finWords = None, manWords = None, artWords = None):
    # Return the category that appears the most
    (cat, score) = getCategory.mainCategoryAndScore(resume, progWords, csWords, engWords, finWords, manWords, artWords)
    return (cat, score)

def overall(resume):
    overall = getCategory.getCategoriesAverage(resume)
    fout = open("results.tex", "a")
    fout.write("\\textbf{Average Score: } " + str(tenOverall(overall)) + "\\\\\n")
    fout.close()
    return overall

def tenCategory(score):
    return score / 2.5

def tenOverall(score):
    return score / 1.5


def programmingScore(resume):
    proScore = getCategory.programmingScore(resume)
    fout = open("results.tex", "a")
    fout.write("score: "+ str(tenProgScore(proScore)) + "\\\\\n")
    fout.close()
    return proScore

def tenProgScore(score):
    return score * 2

def gpaScoreCalculator(gpa):
    gpa_unweighted = gpa / 4.00
    gpa_scaled = gpa_unweighted * 10
    return gpa_scaled

def gpaScore(word_tokens):
    score = 0

    gpaFound = False
    for token in word_tokens:
        if "gpa" in token.lower():
            index = word_tokens.index(token)
            try:
                if "/" in word_tokens[index + 1]:
                    words = word_tokens[index + 1].split("/")
                    gpa = float(words[0])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
                else:
                    gpa = float(word_tokens[index + 1])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
            except:
                if "/" in word_tokens[index - 1]:
                    words = word_tokens[index - 1].split("/")
                    gpa = float(words[0])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
                else:
                    gpa = float(word_tokens[index - 1])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True

    # a resume with a GPA might indicate a lower GPA
    fout = open("results.tex", "a")
    if gpaFound == False: 
        fout.write("\\textbf{GPA: not found}\\\\\n")
        score = gpaScoreCalculator(2.5)
    else:
        fout.write("\\textbf{GPA: " + str(gpa) +"}\\\\\n")
    fout.close()
    return score

    

def collegeScore(word_tokens):
    university = ["Carnegie Mellon University", "Princeton University",
    "Harvard University", "Yale University", "Columbia University",
    "Stanford University", "University of Chicago",
    "Massachusetts Institute of Technology", "Duke University",
    "University of Pennsylvania", "California Institute of Technology",
    "Johns Hopkins University", "Dartmouth College", "Northwestern University",
    "Brown University", "Cornell University", "Vanderbilt University",
    "Washington University in St. Louis", "Rice University",
    "University of Notre Dame", "University of California-Berkeley",
    "Emory University", "Georgetown University",
    "University of California-Los Angeles", "University of Southern California",
    "University of Virginia", "Tufts University", "Wake Forest University",
    "University of Michigan-Ann Arbor", "Boston College",
    "University of North Carolina-Chapel Hill", "New York University", "University of Rochester",
    "Brandeis University", "College of William and Mary", "Georgia Institute of Technology",
    "Case Western Reserve University", "University of California-Santa Barbara",
    "University of California-San Diego", "Boston University", "Rensselaer Polytechnic Institute",
    "Tulane University", "University of California-Davis", "University of Illinois-Urbana-Champaign",
    "University of Wisconsin-Madison", "Lehigh University", "Northeastern University",
    "Pennsylvania State University-University Park", "University of Florida", "University of Miami",
    "Ohio State University-Columbus", "Pepperdine University", "University of Texas-Austin",
    "University of Washington", "Yeshiva University", "George Washington University",
    "University of Connecticut", "University of Maryland-College Park",
    "Worchester Polytechnic Institute", "Clemson University", "Purdue University-West Lafayette",
    "Southern Methodist University", "Syracuse University", "University of Georgia",
    "Brigham Young University-Provo", "Fordham University", "University of Pittsburgh",
    "University of Minnesota-Twin Cities", "Texas A&M University-College Station", "Virginia Tech",
    "American University", "Baylor University", "Rutgers, The State University of New Jersey-New Brunswick",
    "Clark University", "Colorado School of Mines", "Indiana University-Bloomington",
    "Michigan State University", "Stevens Institute of Technology", "University of Delaware",
    "University of Massachusetts-Amherst", "Miami University-Oxford", "Texas Christian University",
    "University of California-Santa Cruz", "University of Iowa", "Marquette University",
    "University of Denver", "University of Tulsa", "Binghamton University-SUNY",
    "North Carolina State University-Raleigh", "Stony Brook University-SUNY",
    "SUNY College of Environmental Science and Forestry", "University of Colorado-Boulder",
    "University of San Diego", "University of Vermont", "Florida State University", "Saint Louis University",
    "University of Alabama", "Drexel University", "Loyola University Chicago", "University at Buffalo-SUNY",
    "Auburn University", "University of Missouri", "University of Nebraska-Lincoln",
    "University of New Hampshire", "University of Oregon", "University of Tennessee",
    "Illinois Institute of Technology", "Iowa State University", "University of Dayton",
    "University of Oklahoma", "University of San Francisco", "University of South Carolina",
    "University of the Pacific", "Clarkson University", "Duquesne University", "Temple University",
    "University of Kansas", "University of St. Thomas", "University of Utah", "University of Arizona",
    "University of California-Riverside", "The Catholic University of America", "DePaul University",
    "Michigan Technological University", "Seton Hall University", "Colorado State University", "New School",
    "Arizona State University-Tempe", "Louisiana State University-Baton Rouge", "University at Albany-SUNY",
    "University of Arkansas", "University of Illinois-Chicago", "University of Kentucky",
    "George Mason University", "Hofstra University", "Howard University", "Ohio University",
    "Oregon State University", "New Jersey Institute of Technology",
    "Rutgers, The State University of New Jersey-Newark", "University of Cincinnati",
    "University of Mississippi", "University of Texas-Dallas", "Washington State University",
    "Kansas State University", "Missouri University of Science & Technology", "St. John Fisher College",
    "Illinois State University", "Oklahoma State University", "San Diego State University",
    "University of Alabama-Birmingham", "Adelphi University", "Southern Illinois University-Carbondale",
    "St. John's University", "University of Maryland-Baltimore County", "University of Massachusetts-Lowell",
    "University of South Florida", "Virginia Commonwealth University", "University of La Verne",
    "Biola University", "Florida Institute of Technology", "Immaculata University",
    "Maryville University of St. Louis", "Mississippi State University", "University of Hawaii-Manoa",
    "University of Rhode Island", "Ball State University", "Texas Tech University",
    "University of Central Florida", "University of Idaho", "University of Louisville", "University of Maine",
    "University of Wyoming", "Andrews University", "Azusa Pacific University", "Edgewood College",
    "Kent State University", "West Virginia University", "Pace University",
    "St. Mary's University of Minnesota", "University of New Mexico", "University of North Dakota",
    "University of South Dakota", "Bowling Green State University", "North Dakota State University",
    "South Dakota State University", "University of Alabama-Huntsville", "University of Houston",
    "University of Nevada-Reno", "University of North Carolina-Greensboro", "Western Michigan University",
    "Widener University", "Central Michigan University", "East Carolina University",
    "South Carolina State University", "University of Missouri-Kansas City",
    "University of North Carolina-Charlotte", "Ashland University",
    "Indiana University-Purdue University-Indianapolis", "Louisiana Tech University",
    "New Mexico State University", "University of Colorado-Denver"]
    short_words = ["university", "for", "and", "get", "the", "art", "ice", "town", "park", "van", "los"]
    i = 0
    fout = open("results.tex", "a")
    for college in university:
        for word in word_tokens:
            if((word.lower() not in short_words) and (word in college) and (len(word) > 2)):
                fout.write("\\textbf{"+ college + "}")
                
                i = university.index(college)
                i = i + 1
                break   
        if(i != 0):
            break
    score = ((200-i)/200.0) * 15   
    fout.write(" \\textbf{score:} " + str(tenUniversity(score)) + "\\\\\n")
    fout.close()
    return score

def tenUniversity(score):
    return score / 1.5

def wordCountScore(tokens):
    score = 10
    # number of words
    count = 0
    # word count
    for tok in tokens:
        if tok != "":
            count += 1
    # 475 words -> average amount of words on one page
    if count == 400: score -= 0
    # accounts for resumes too short and too long
    else:
        score -= min(abs(400 - count) / 20, 5)
    return score

def degreeScore(word_tokens):
    score = 10
    desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
    word_tokens_lower = [x.lower() for x in word_tokens]
    # searches for similar words
    degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
    close_match_fail = False
    close_match = ""
    if degree == []:
        for word in word_tokens_lower:
            if (desiredDegree.lower() in word):
                close_match_fail = True
                close_match = word
                break
    stop_search = False
    while (not stop_search):
        if degree == [] and close_match_fail == False: 
            answer2 = raw_input("There are no matches. Search again? (Y/N) \n")
            if answer2 == "Y" or answer2 == "y" or answer2 == "yes" or answer2 == "Yes":
                desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
                degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
            else:
                stop_search = True
        else:
            if close_match_fail == True:
                print("Closest match to " + desiredDegree + " is " +
                close_match + ".")
                stop_search = True
            else:
                print("Closest match to " + desiredDegree + " is " +
                    degree[0] + ".")
                stop_search = True
    close_match_fail = False
    close_match = ""
    stop_search = False
    while (not stop_search):
        answer1 = raw_input("Would you like to search for another degree? (Y/N)\n")
        if answer1 == "Y" or answer1 == "y" or answer1 == "yes" or answer1 == "Yes":
            desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
            degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
            if degree == []:
                for word in word_tokens_lower:
                    if (desiredDegree.lower() in word):
                        close_match_fail = True
                        close_match = word
                        break
            if degree == [] and close_match_fail == False:
                answer3 = raw_input("There are no matches. Search again? (Y/N) \n")
                if answer3 == "Y" or answer3 == "y" or answer3 == "yes" or answer3 == "Yes":
                    desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
                    degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
                else:
                    stop_search = True
            else:  
                if close_match_fail == True:
                    print("Closest match to " + desiredDegree + " is " +
                        close_match + ".")
                else:
                    print("Closest match to " + desiredDegree + " is " +
                            degree[0] + ".")
        else:
            stop_search = True
    degreeFound = False
    answer4 = raw_input("Would you like to search the word 'degree'? (Y/N) \n")
    if answer4 == "Y" or answer4 == "y" or answer4 == "yes" or answer4 == "Yes":
        print("Searching 'degree' and returning adjacent words...") 
        for word in word_tokens_lower:
            if ("degree" in word):
                index = word_tokens_lower.index(word)
                if index - 1 >= 0 and index + 1 < len(word_tokens_lower):
                    prev_word = word_tokens_lower[index - 1]
                    after_word = word_tokens_lower[index + 1]
                    print("Word before 'degree': " + prev_word)
                    print("Word after 'degree': " + after_word)
                    degreeFound = True
                    break
                elif index - 1 >= 0 and index + 1 >= len(word_tokens_lower):
                    prev_word = word_tokens_lower[index - 1]
                    print("Word before 'degree': " + prev_word + "\n")
                    print("No word found after 'degree'.")
                    degreeFound = True
                    break
                elif index - 1 < 0 and index + 1 < len(word_tokens_lower):
                    after_word = word_tokens_lower[index + 1]
                    print("Word after 'degree': " + after_word + "\n")
                    print("No word found before 'degree'.")
                    degreeFound = True
                    break
                else:
                    # should not happen
                    print("The only word in the resume is 'degree'.")
                    degreeFound = True
                    break
        if degreeFound == False:
            print("The word 'degree' does not appear in the resume.")
    else:
        pass
    answer = raw_input("Did you find the degree you were looking for? (Y/N)\n")
    # yes if desired degree found else degree not attained or present
    if answer == "yes" or answer == "Y" or answer == "y" or answer == "Yes": score -= 0
    else: score -= 10
    return score

def sectionScore(resume):
    section_tokens = tokenize.input_file_words(resume,[])
    currentIndex = -1
    wordCount = [0,0,0]
    for x in section_tokens: 
        x = x.lower()
        if(x.strip("!@#$%^&*()_+|}{:?") in ["work experience", "employment", "experience"] and currentIndex != 0):
            currentIndex = 0
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["publications", "projects", "research"] and currentIndex != 1):
            currentIndex = 1
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["leadership","leadership experience"] and currentIndex != 2):
            currentIndex = 2    
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["education","activites","skils", "interests", "extracurricular", "honors", "references", "awards", "acheivements"]):
            currentIndex = -1
        else:
            wordCount[currentIndex] += 1

    return  min(((sum(wordCount) - min(wordCount))) / 450.0, 1.0) * 10

def main(resume, cats):
    # initialize variables 
    # have the words as tokens in a list
    tokens = tokenize.input_file_lines(resume,[])
    word_tokens = tokenize.input_file_words(resume,[])
    score = 0


    
    # get email
    email = ""
    for token in word_tokens:
        if "@" in token:
            email = token
            break


    fout = open("results.tex", "a")
    fout.write("\\section{" + email +"}\n")
    fout.close()
    # category score
    (cat, category_score) = category(resume, cats[0],cats[1],cats[2],cats[3],cats[4],cats[5])

    # overall score
    overall_score = overall(resume)

    # programming languages score
    programming_score = programmingScore(resume)

    # GPA score
    gpa_score = gpaScore(word_tokens)

    # university score
    college_score = collegeScore(word_tokens)

    # word count score
    word_count_score = wordCountScore(tokens)

    # degree score
    degree_score = degreeScore(word_tokens)

    # sectional score
    section_score = sectionScore(resume)

    print "Finished parsing."
    score = category_score + overall_score + programming_score + \
            gpa_score + college_score + word_count_score + \
            degree_score + section_score

    
    fout = open("results.tex", "a")
    fout.write("\\textbf{Best category: } "+cat+"\\\\\n\
\\textbf{Overall Score: }"+ str(score/ 10.0) + " (out of 10)")
    fout.close()

    return (cat, score, email)

def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

(resume, cats) = init()

if type(resume) == list:
    for i in range(len(resume)):
        print main(resume[i], cats)
    fout = open("results.tex", "a")
    fout.write("\\end{document}")
    fout.close()
    subprocess.call('pdflatex results.tex')
elif resume != "":
    print main(resume, cats)
    fout = open("results.tex", "a")
    fout.write("\\end{document}")
    fout.close()
    subprocess.call('pdflatex results.tex')
