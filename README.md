# w207_final_project_Cluster-F  

1) Download csv's from kaggle and put into folder ../input  
2) Run Data_EDA_Loading_and_Features.ipynb  
	- Note this only includes a sample of some of the documentation we got
	- Page_views.csv is 100GB and >2 billion rows, so we used page_views_sample instead
3) Then you can run Machine_Learning.ipynb which will use the training and dev data set up by the Data_EDA_Features.ipynb.
	- The GridSearches and Random Forest models are SLOW

3) The full version of the data loading code is in Archive/Final_Code_FULL.py  
	- This script can be run on an AMI instance that should be large size and connected to a volume that is at least 300 GB. It will still take a while to run and should be run in the background through `nohup python Final_Code_FULL.py &` to make sure sleep doesn't kill the process










