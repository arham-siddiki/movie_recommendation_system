To run the app properly, follow the steps : 
1. open the python files in any python ide.
2. make sure the required csv file dataset is there in root folder.
3. download and install all the required packages(numpy, sklearn, nltk, streamlit, etc).
4. open data_process.py file.
5. if there is no 'movie_dict.pkl' file, uncomment line number 129 and run file "data_process" once.
6. if there is no 'similarity.pkl' file, uncomment line number 131 and run file "data_process" once.
7. now for the final step, go to terminal and give command :
	"streamlit run app.py"
8. a new page in browser will open.
9. choose any movie and press recommend.
