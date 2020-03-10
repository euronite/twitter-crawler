# twitter-crawler
Coursework for Uni Y3, Web Science

To setup and run the program, dependencies are located in a requirements.txt file in the root directory. Run pip install -r requirements.txt to install. 
The API Keys and database URL can be inserted in the config.py file directly, and the json file reader can be removed, or as a api.json file. 
To start the whole program, run main.py after adjusting the parameters in the file. An important one is the true_k variable in grouping.py in the cluster_text() function. The program will crash if true_k is too large for the amount of tweets collected. The default is 70 for the couple of hours the program was run.
