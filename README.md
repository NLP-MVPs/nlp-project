# Predict the Code - An NLP Project
## Table of Contents
- [Predict the Code - An NLP Project](#predict-the-code---an-nlp-project)
  - [Table of Contents](#table-of-contents)
- [Goal](#goal)
- [Wrangle](#wrangle)
  - [Acquire](#acquire)
  - [Prepare](#prepare)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [Visualizations](#visualizations)
  - [Hypothesis Testing & Feature Selection](#hypothesis-testing--feature-selection)
- [Modeling](#modeling)
- [Results & Conclusion](#results--conclusion)
  - [Next Steps](#next-steps)

# Goal
The goal of this project is predict the primary code type used in a GitHub repository based on the text contained within a readme. For this, the team decided to focus in on repositories who's primary coding language, as determined by GitHub, was either JavaScript or Python. 

We will deliver the following:
  * A Jupyter notebook containing detailing to every step of this project
  * A 5-minute presentation about the project, including slides


# Wrangle


## Acquire
To acquire the data, the team first needed to decide on a method for gathering our sample data. We originally choose to manually find repos belonging to various news organizations and then scrape their repos for 5 coding languages: python, JavaScript, HTML, PHP, and Ruby. However, this proved to be too small of a sample size to work with. We then changed our approach to focusing in on repositories that were determined to be either JavaScript or Python by GitHub. 

To gather our data, we conducted two separate scraping operations. First, from the [most starred repos](https://github.com/search?q=stars%3A%3E0&s=stars&type=Repositories) for both [JavaScript](https://github.com/search?l=JavaScript&q=stars%3A%3E0&s=stars&type=Repositories) and [Python](https://github.com/search?l=Python&q=stars%3A%3E0&s=stars&type=Repositories), we scrapped the repo links of the first 20 pages of results. Our second scrape operations involved taking those link and then scraping 'markdown-body entry-content container-lg' for the readme contents and 'd-inline-flex flex-items-center flex-nowrap link-gray no-underline text-small mr-3' for the primary code used and the percentage of the repo it represents. If a repo did not contain a useable readme file, it was skipped.

Each iteration of scrapping process produced a dictionary object that was then appended to the a list. Each dictionary has the shape below.
```
{"body":text from the readme, "top_code":the first entry from the code block}
```
Once the list of dictionaries created, we create a [gitMDv2.json](gitMDsv2.json) file and reads the list of dictionaries into a DataFrame. The full code and its explanation can be found at [acquire.py](https://github.com/NLP-MVPs/nlp-project/blob/main/acquire.py) in this repo.

## Prepare
Once the data was acquire, the prepare.py module turns the data into a useable DataFrame by doing the following: 
* Applies the basic_body_clean, tokenization, removestop_words, and lemmatizes functions to the readme body text
and returns the output as gitMds['clean'].
* Applies the basic_code_clean, tokenizizatize, and removestop_words functions to the top_code and returns it as gitMds['top_code_cleaned]
* Splits gitMds['top_code_cleaned] into two columns gitMds['top_code_cleaned'] and gitMds['top_percentage_cleaned']
* Returns gitMDs as a data frame

The full code and it's explanation can be found at [prepare.py](https://github.com/NLP-MVPs/nlp-project/blob/main/prepare.py) within this repo.

# Exploratory Data Analysis (EDA)


## Visualizations


## Hypothesis Testing & Feature Selection

# Modeling

  
# Results & Conclusion

## Next Steps
