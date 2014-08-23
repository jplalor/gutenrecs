John Lalor
ECT 584-FInal Project
8/23/2014

This README is for evaluation of my final project.

The zip file includes the following information:

-Lalor_Writeup.pdf: Project report
-The "gutenberg" folder includes source code for the recommender application, as well as utility functions used to clean the data and generate the TF-IDF matrix and recommendation lists.
-Readme.txt (this file)
-The final project exists as an online recommender at http://gutenrecs.heroku.com . Please use this link to test the app and see some of the recommendation results.
-requirements.txt: a list of Python requirements required to run the web app on your own server (Gunicorn is the recommended server for running the app)

Below is a list of the python files included and their function (each file includes comments to explain the code as well). These files are located in the "utils" directory:
-gutenberg-text2.py - create the partial term frequency matrices and output the TF-IDF matrix for 5000 of the Gutenberg texts.
-gutenberg-similarity.py - Calculates the cosine similarities for each book, and save the top 20 most similar books for each text. 

-NOTE: The term count matrix for all of the documents is available, but is quite large (3+ GB), if you would like to see this as well, let me know and I can figure out a way to send it along.