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
  * an [MVP notebook](https://github.com/NLP-MVPs/nlp-project/blob/main/MVP.ipynb) that details every step of this project.
  * a 5-minute presentation about the project, including slides.
  * a data dictionary for data used in this project.
  * this readme.

# Wrangle
The following processes are used to wrangle the data into a useable form by first acquiring the data, then preparing the data, and finally pre-processing the data by spiting the data into train, validate, test sets and creating a few pandas series to conduct EDA on.

## Acquire
To acquire the data, the team first needed to decide on a method for gathering our sample data. We originally choose to manually find repos belonging to various news organizations and then scrape their repos for 5 coding languages: python, JavaScript, HTML, PHP, and Ruby. However, this proved to be too small of a sample size to work with. We then changed our approach to focusing in on repositories that were determined to be either JavaScript or Python by GitHub. 

To gather our data, we conducted two separate scraping operations. First, from the [most starred repos](https://github.com/search?q=stars%3A%3E0&s=stars&type=Repositories) for both [JavaScript](https://github.com/search?l=JavaScript&q=stars%3A%3E0&s=stars&type=Repositories) and [Python](https://github.com/search?l=Python&q=stars%3A%3E0&s=stars&type=Repositories), we scrapped the repo links of the first 20 pages of results. Our second scrape operations involved taking those links and then scraping <markdown-body entry-content container-lg> for the readme contents and <d-inline-flex flex-items-center flex-nowrap link-gray no-underline text-small mr-3> for the primary code used and the percentage of the repo it represents. If a repo did not contain a useable readme file, it was skipped.

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
After the data is prepared, we drop any columns we will not use in EDA, and then split the data into train, validate, and test sets within the [MVP notebook](https://github.com/NLP-MVPs/nlp-project/blob/main/MVP.ipynb). Lastly, we create a pandas series that contains all words each for python, JavaScript, and both to use in our EDA. The method we use to carry out this task is below.

```Python
# create series objects for each top_code_clean that is a string of words joined on spaces in order to make it 1 continious string 
# for python
python_words = ' '.join(train[train.language=='python'].readme)
# for javascript
javascript_words = ' '.join(train[train.language == 'javascript'].readme)
# both python and java script
all_words = ' '.join(train.readme)
```

# Exploratory Data Analysis (EDA)
After wrangling the data we conducted EDA on our train data set in order to glean insights from our data. We accomplished this by creating several visualizations that focused on which words are primarily used within our data, using those words to create additional features for our analysis, and then conducting hypothesis testing on the features we created.

## Visualizations
We created a few visualizations to help us identify possible features to use in our model. The most useful visualization we created was a proportional chat that showed the percentage break down of each word's usage by either JavaScript or Python. Doing this allowed us to identify a several words that were used more by each language than the other. We were also able to identify two words that were only used by one language in our test set - react for JavaScript and apikey for Python. From this visualization we created four features: has_top_5_js_words, has_top_5_py_words, has_react, and has_apikey. 

## Hypothesis Testing & Feature Selection
After creating our new features we needed to test them to see if they were actually statistically significant feature in our model. We did this by conducting [Chi Squared](https://statisticsbyjim.com/hypothesis-testing/chi-square-test-independence-example/) test as all the features were categorical. Our hypothesis and null hypothesis for each was:

* ![formula](https://render.githubusercontent.com/render/math?math=$H0$) - There is not a relationship between <new_feature> and language
* ![formula](https://render.githubusercontent.com/render/math?math=$Ha$) - There is relationship between <new_feature> and language

After running each of the 4 new features through a Chi Squared test, we discovered that only has_react had a statistically significant relationship with language.

# Modeling
  
# Results & Conclusion

## Next Steps
