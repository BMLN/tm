# Extraction of Industry Skills in the form of Topic Modeling through LDA from online Job Postings

offering an easy adjustable data collection and extraction interface (((with scrapy, spacy, ...)))



<br>
<br>
<br>

### Data Collection
#### -> problem definition: Company names have to be translated to job postings 

1. sources for Job Posting have to be selected

   the selection influences:
    - the demanded effort for an automation [2]
    - possible biases and the size of the resulting dataset 
    
    &rarr; Following the process of [1] and [2] the selection has therefore resulted in indeed.com, stepstone.de and get-in-it.de (and maybe should also include linked-in?(bitte feedback!)) to aim for a large dataset with a balanced distribution of sources
    
2. the search capabilities of the sources have to be analyzed

   the structure of the webpage and the resulting search results will:
    - determine how a scraper can be implemented to access jobpostings

   &rarr; our analysis has resulted in the observation that while some modifiers are available, atleast the companyname has to be translated to sourcespecific ids (noch ergänzungen) 

   
3. the resulting jobpostings have to be analyzed and attribues have to be selected

   the selection and structure will once again influence:
    - the demanded effort for an automation
    - the capabilites to fetch specific attributes directly

   &rarr; where general information like the source itself, titles, locations, (..., which ones?) can be singled out through html items, some sources don't offer those capabilities for more specific attributes like tasks and qualifications. It would be therefore be more suitable to limit the extraction just to the complete job posting element from the html source. This on the on hand has the advantage that a general purpose interface could be applied, but furthermore also reduces the computation the scraper has to do. Less computation from the scraping component means faster runthrough as well as easier changes to the processing pipeline as it is split into smaller and better interchangeable pieces.


#### -> Implementation: (tbd?)

with the resources available, especially python has led itself as the desired language for web scraping.
Additionally, the use of the scrapy framework brings in many desireable features and benefits to the process            (add sources)

1. We defined scraping interfaces and seperated each step in the data acquisition into its own problem, which consumes information provided (by its precessor)

   for each source there will be the following scrapers:
      - one gathering information about source specific mappings like company names and their respective ids (not implemented yet, handcoded/extracted atm)
      - one gathering the available urls that lead to job postings of each source
      - one extracting the as valuable determined information from each job posting
 
2. with the interfaces defined and an implementation as an abstract class:
   - some qualities are already implemented on the top level
   - leading to each new source/scraping only demanding the source specific knowledge and implementation of the webpage and content mappings (e.g. what element will provide the location of jobposting )


X. Processing is still inside of scraper (//text() (which isnt that great)), subject to change for a good architecture (should be then moved as an extra between DC and DE)


### Data Extraction
#### -> problem definition: job postings have to be translated to topics (a group of terms)

following [1] and [2] the extraction of IS is done through topic modeling with LDA

1. as of any analysis on text basis, the texts have to be prepared before it might be applied

   [2] describes the procedure as the following steps: 
      1. text normalization
      2. lemmatization, 
      (3.) (n-grams, meaning NER? most likely)
      4. filtering of words with not a lot of meaning (stopwords, non relevant POS)

2. LDA has to be applied to the resulting textdata

3. a set configuration for LDA has to be determined through (quantitive?) analysis


#### Implementation

1.1. basic filtering of leftover symbols 
1.2. & 3. & 4 applying the Spacy pipeline

2. the utilized LDA package applies LDA after building a dictionary and bag of word representations for each document

3. following [2], the determination for the best number of topics is selected after multiple runthroughs with different configurations in the range of x-300






#### Visualizing the results

tbd





### Sources:

[1]: ALIGNING IS CURRICULUM WITH INDUSTRY SKILL EXPECTATIONS: A TEXT MINING APPROACH

[2]: BRIDGING THE GAP BETWEEN INDUSTRY SKILL