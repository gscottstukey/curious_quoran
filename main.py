from recommend import Recommender
from parser import TextParser
from image_scraper import get_image
import pickle
from selenium import webdriver



def main():
    '''
    INPUT: None
    OUTPUT: Recommendations sorted in order of relevance
    
    Uses the TextParser and Recommender classes to generate resource recommendations given a user's Quora data
    '''

    read = TextParser()
    read.assemble_df()
    pickle.dump(read.df, open("data/master_df.pkl", "wb"))
    quora_user = open('data/quora_data.pkl')
    quora = pickle.load(quora_user)
    filtered = read.preprocess_quora(quora)
    clean_quora = read.clean_up(filtered)
    pickle.dump(clean_quora, open("data/clean_quora.pkl", "wb"))

    # Make recommendations
    rec = Recommender()
    test = rec.vectorize()
    top_ten_ind = rec.recommend()
    recs = read.df.ix[top_ten_ind]
    recs = recs.reset_index()
    recs['img_link'] = map(get_image, recs['title'])
    recs['img_link'] = recs['img_link'].apply(lambda x: x[0])
    print "These are your recommendations: \n"
    print recs[['title', 'type', 'img_link']]

    # for link in recs['img_link']:
    #     driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")
    #     driver.get(link)

    return recs[['title', 'type', 'img_link']]

if __name__ =="__main__":
    main()	