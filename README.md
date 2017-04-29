Group Names: Grant Lindberg, Vannesa Farmer, Tyler Petty
E-mails: grant.lindberg@wsu.edu, vannesa.farmer@wsu.edu, tyler.petty@wsu.edu
Professor: Scott Wallace
Assignment: Project 2: Document Classification
Date: April 28, 2017


Description: In this project, we attempt to find ways to classify documents by parsing their input and using patterns to group them. We explore six different initial
strategies in order to test and evaluate our classification process. By comparing these strategies, their weak points and strong points will surface, allowing us to
determine the best scenarios for each strategy. Our writeup will lay out the details for interested recipients.


How to build/run:

Type "python3 main.py 'training_dir_1' 'training_dir_2' 'training_dir_3' 'testing_dir' <yes>" (Note: The single quotes are optional)
Where each 'training_dir' represents a relative path to a directory used for training the algorithms, the 'testing_dir' represents a relative path to the directory used for testing the algorithms, and the 'yes' flag, being optional, will save and load the weights and biases for the perceptrons

You may not enter in fewer than four arguments i.e. the program must have three training directories and one testing directory
If you mess up on the command line input, the program will display a help message


Output:

The results will be outputted to a file called 'file_results.txt', each line containing a classification in the format 'I, 'OR_COOS.txt', DR' where 'I' represents the strategy, 'OR_COOS' represents the file name in question, and 'DR' represents the classification
