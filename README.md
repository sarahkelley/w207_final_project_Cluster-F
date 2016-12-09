# w207_final_project_Cluster-F  

1) Download csv's from kaggle and put into folder ../input  
2) Run make_mini_datasets.py  
3) Run Data wrangling.ipynb  

Ideas: 
Have we tried [Dask DataFrame](http://dask.pydata.org/en/latest/dataframe.html) or [Pyspark + pandas] (https://spark.apache.org/docs/2.0.0/sql-programming-guide.html#generic-loadsave-functions) for getting the large files down? My office had a talk today that brought this up and I wanted to pass it on. I need to finish a 205 project tonight (Tuesday) but can look into it on Wednesday if we want.

# 12/08/16    
- Set up shared AMI with Spark 2.0  
- Install pandas, numpy, sklearn, etc. on AMI  
- Clean up data because TOO BIG  
- Join/merge all the datasets to get one central dataframe  

## MODELS:  
1. Basic model (Jay): which ad is most likely to be clicked?  
2. Regression (Sarah): platform + country binarized + others, .8 accuracy
3. Decision tree: Lisa/Nikki?
4. SVD: display_id x ad_id, likelihood as values

## TASKS:  
1. SPARK/AMI setup - Sarah - Friday night
2. SVD - Jay
3. Feature engineering - Nikki/Lisa
   - Campaign ID: % of ads clicked from campaign
   - Advertiser ID: % of ads clicked from advertiser
   - Platform
   - Document entity/category
4. Decision tree - Lisa?

## Saturday 930AM - checkin!








