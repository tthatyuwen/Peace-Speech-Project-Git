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


#### BigScience Group (Yibo Chen & Pinyi Yang):

  ##### Yibo Chen:  
  
  ##### Work Summary
  
  1. Find out datacards(English Part) start with "pseudocrawl", *eg.pseudocrawl-filtered_667_www_bhaskar_com*,[detailed work](https://github.com/ChenYb9807/ENGI8000/blob/main/Pseudocrawl%20data%20in%20BigScience.py)
  2. Try to use python library [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) to scrape news text from 16 countries. Not a good idea. [Demo](https://github.com/ChenYb9807/ENGI8000/blob/main/Scraping%20with%20Newspaper3k.py). The library is not that powerful.
  3. Collect great source for newspaper archive, [India](https://timesofindia.indiatimes.com/archive.cms),[~~Afghanistan~~](https://www.eastview.com/resources/gpa/afghan-central-press/),[Australia,Canada&UK](https://lil.nlp.cornell.edu/newsroom/explore/index.html),[Iran](https://www.tehrantimes.com/archive),[Nigeria](https://archive-it.org/collections/11796),[Sri Lanka](https://www.sundaytimes.lk/210110/archive/),[Finland](https://www.dailyfinland.fi/archive).This can be helpful for better web scraping result.
  4. BigScience dataset contains many news irrelavant corpus, wiki, and many text in forum website. The most valuable part for our study might be those newspaper in Singapore. *Dataset uid: pseudocrawl-filtered_497_www_straitstimes_com* It's big enough and relevant to our study.
  
   ##### Future work
   
   Successfully crawl data from India by Saturday and communicate with other members doing scraping work, make sure we have access to at least 6 countries newspapers by Tuesday.
   
   ##### Progress by Friday(10/7):
   1. Successfully scraped the news on India,Iran,Finland
   2. Found new source for [Ireland](https://www.sundayworld.com/archive/cnt),[Nigeria](https://www.thenigerianvoice.com/archive/),[Uganda](https://www.independent.co.ug/all-news/),[Norway](https://www.newsinenglish.no/2022/10/07/),[Zimbabwe](https://bulawayo24.com/index-id-archive.html). However, news source from Zimbabwe is not that good.
      
