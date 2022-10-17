# Peace Speech Project

You have reached the Github repo for the Peace Speech Project for Fall 2022 Capstone

## 9/27-10/4

#### Social Media Group (Yuwen Zhang, Ziheng Ru):

  1. Looked into the usage of social media platforms in the 20 countries listed previously; among them, both Reddit and Facebook API do not provide users’ geospatial information
  2. Applied Twitter Developer API for Academic Research Access:
     https://developer.twitter.com/en/products/twitter-api/academic-research/application-info
     * Maximum 10 M Tweets per month
     * Can fetch user info including: user id/location/followers/tweets/description etc
     * Can fetch tweet info including: tweet content/time/retweets/replies/likes/quote/tag location
  3. Fetched around 2 M tweets from 2017-present, maximum 100k tweets per country
     * Approach: Get tag location of each tweet, if it exists. Select tweets with tag location that’s in the 20 countries list
     * The complete dataset
       https://drive.google.com/file/d/1WfjUgL7eqGj8CP_7rqKTeyQM1NzupRyj/view?usp=sharing


#### News Group ( Yibo Chen & Pinyi Yang & Xinfu Su & Hongou Liu): 
  
  ##### Work Summary
        1. Collect and Process 5 indexes to build model for identifying high/low peace countries(Pinyi Yang)
        2. Preprocess news data, find stop words, use xgboost(Xinfu Su), NN(Yibo Chen), bert(Hongou Liu) to model high/low peaceful countries, accuracy range from 0.9-0.98
        3. Find keywords that indicate peacefulness(Present in meeting)
  
   ##### Future work
        1. Find Reason for such high accuracy, improve methods to find keywords.

##### Data Source:

 [India](https://timesofindia.indiatimes.com/archive.cms),[~~Afghanistan~~](https://www.eastview.com/resources/gpa/afghan-central-press/),[Australia,Canada&UK](https://lil.nlp.cornell.edu/newsroom/explore/index.html),[Iran](https://www.tehrantimes.com/archive),[Nigeria](https://archive-it.org/collections/11796),[Sri Lanka](https://www.sundaytimes.lk/210110/archive/),[Finland](https://www.dailyfinland.fi/archive),[UK](https://www.independent.co.uk/archive),[Canada](https://www.thestar.com/archive.html),[Ireland](https://www.sundayworld.com/archive/cnt),[Nigeria](https://www.thenigerianvoice.com/archive/),[Uganda](https://www.independent.co.ug/all-news/),[Norway](https://www.newsinenglish.no/2022/10/07/),[Zimbabwe](https://bulawayo24.com/index-id-archive.html)
