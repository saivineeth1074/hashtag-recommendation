# Hashtag recommendation for hyperlinked tweets
### Need for this project
- Many hashtag recommendations doesn't take the content of the hyperlinks in the tweets into account while recommending hashtags. 
- This project aims to take into account the content of the hyperlinks in the tweets for a better hashtag recommendation system.

### Research paper used for implementation
> Hashtag recommendation for hyperlinked Tweets - Surendra Sedhai, Aixin Sun (Proceedings of the 37th international ACM SIGIR conference on Research & development in information retrieval (Pages 831-834)

### Implementation
- The scraped dataset (containing posts with hashtags) is available at this [**link**](https://drive.google.com/open?id=0BynZHoodZ0lqVTBmZ1FGa015OUk).
- The data was scraped for some domains (politics/tech/..) using which the models could be trained.
- Various methods are used to recommend hashtags for a given test tweet or post. These recommendations are then sent to a learning to rank algorithm which ranks these hashtags according to their relevance to the given tweet and finally recommends the **top-K** hashtags.

### Code files description
- All the codes were written in **python 3.5.2**.
- *app.py* -  Main code which returns the top-K recommended hashtags when the test data is given as input (end-to-end).
- *crawler.py* - Code to scrape data from a given domain on the moneycontrol website.
- *structuredData.py* - Code to create a structured data from the scraped data (which are stored in separate files).
- *getEntities.py* - Code to get all the entities for all the posts using dendalion API.
- *similarDesc.py* - code implementing cosine similarity using the description of the post.
- *similarContent.py* - code implementing cosine similarity using the content of the post.
- *domainLink.py* - Code to recommend hashtags based on the domain of the test data.
- *RWR.py* - code implementing random walk with restart method.
- *LTModel.py* - Code to implement the language translation model.
- *rankSVM.py* - code implementing the learning to rank method.

### Steps to run the code
- Before running the code, the required modules can be installed using the command `sudo pip3 install -r requirements.txt`.
- The file *app.py* can be run using the command `python3 app.py` for a given test post which then gives out the recommended hashtags for the given post.