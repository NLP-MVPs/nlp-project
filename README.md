# Predict the Code - An NLP Project
## Table of Contents
- [Predict the Code - An NLP Project](#predict-the-code---an-nlp-project)
  - [Table of Contents](#table-of-contents)
- [Goal](#goal)
- [Wrangle](#wrangle)
  - [Acquire](#acquire)
  - [Prepare](#prepare)
  - [Pre-processing](#pre-processing)
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
The following processes are used to wrangle the data into a useable form by first acquiring the data, then preparing the data, and finally pre-processing the data by spiting the data into train, validate, test sets.

## Acquire
To acquire the data, the team first needed to decide on a method for gathering our sample data. We originally choose to manually find repos belonging to various news organizations and then scrape their repos for 5 coding languages: python, JavaScript, HTML, PHP, and Ruby. However, this proved to be too small of a sample size to work with. We then changed our approach to focusing in on repositories that were determined to be either JavaScript or Python by GitHub. 

To gather our data, we conducted two separate scraping operations. First, from the [most starred repos](https://github.com/search?q=stars%3A%3E0&s=stars&type=Repositories) for both [JavaScript](https://github.com/search?l=JavaScript&q=stars%3A%3E0&s=stars&type=Repositories) and [Python](https://github.com/search?l=Python&q=stars%3A%3E0&s=stars&type=Repositories), we scrapped the repo links of the first 20 pages of results. Our second scrape operations involved taking those links and then scraping 'markdown-body entry-content container-lg' for the readme contents and 'd-inline-flex flex-items-center flex-nowrap link-gray no-underline text-small mr-3' for the primary code used and the percentage of the repo it represents. If a repo did not contain a useable readme file, it was skipped.

Each iteration of scrapping process produced a dictionary object that was then appended to the a list. Each dictionary has the shape below.
```
{"body":text from the readme, "top_code":the first entry from the code block}
```
Once the list of dictionaries created, we create a [gitMDv2.json](gitMDsv2.json) file, reads the list of dictionaries into a DataFrame, and finally returns the DataFrame. The full code and its explanation can be found at [acquire.py](https://github.com/NLP-MVPs/nlp-project/blob/main/acquire.py) in this repo.

## Prepare
Once the data was acquire, the prepare.py module turns the data into a useable DataFrame by doing the following: 
* Applies the basic_body_clean, tokenization, removestop_words, and lemmatizes functions to the readme body text
and returns the output as gitMDs['clean'].
* Applies the basic_code_clean, tokenizizatize, and removestop_words functions to the top_code and returns it as gitMDs['top_code_cleaned]
* Splits gitMDs['top_code_cleaned] into two columns gitMDs['top_code_cleaned'] and gitMDs['top_percentage_cleaned']
* Splits gitMDs into train, validate, and test data sets that is stratified on languages and is seeded using 333
* Returns train, validate, and test sets

The full code and it's explanation can be found at [prepare.py](https://github.com/NLP-MVPs/nlp-project/blob/main/prepare.py) within this repo.

## Pre-processing
After the data is prepared, we drop any columns we will not use in EDA, and then split the data into train, validate, and test sets within the [MVP notebook](https://github.com/NLP-MVPs/nlp-project/blob/main/MVP.ipynb) before starting EDA. The method we use to split the data is below.

```Python
df.drop(columns = ['body', 'top_code', 'percentage'], inplace = True)

df.columns = ['readme', 'language']

train_validate, test = train_test_split(df[['language', 'readme']], 
                                        stratify=df.language, 
                                        test_size=.2, 
                                        random_state=333)

train, validate = train_test_split(train_validate, 
                                   stratify=train_validate.language, 
                                   test_size=.25,
                                   random_state=333)
```

# Exploratory Data Analysis (EDA)


## Visualizations


## Hypothesis Testing & Feature Selection

# Modeling

  
# Results & Conclusion

## Next Steps
