from encoded_knowledge import *
from collections import Counter
from util import is_person, preprocess_awards, remove_stopwords
import wikipedia

class Wizard():

    # all the fun stuff happens in here

    def __init__(self, corpus):
        self.corpus = corpus
        self.cache_useful_corpora()


    # memory grows with log of original corpora size, should be ok
    # this method caches some often used subsets of corpus (we query these subsets
    # for each award that we are looking at)
    def cache_useful_corpora(self):

        self.corpus_contain_best = self.corpus.filter(
        lambda x: x.contains_word_partial('best'))
        self.corpus_contain_best_nominee = self.corpus_contain_best.filter(
        lambda x: x.contains_word_partial('nomin'))
        self.corpus_contain_best_win = self.corpus_contain_best.filter(
        lambda x: x.contains_any(['win', 'won', 'wins']))
        self.corpus_contain_best_present = self.corpus_contain_best.filter(
        lambda x: x.contains_word_partial('present'))
        self.corpus_contain_congrat_not_win = self.corpus_contain_best.filter(
        lambda x: x.contains_word_partial('congrat')).filter(
        lambda x: x.not_contains_partial('win'))
        self.corpus_contain_robbed = self.corpus.filter(
        lambda x: x.contains_word_partial('robbed'))

        # for tweet in self.corpus_contain_robbed:
        # 	print(tweet)
        # print(len(self.corpus_contain_robbed))
        # print(len(self.corpus_contain_best))



    # this just takes all tweets that contain the substring "host"
    # it then takes all of the capitalized 2grams that we filtered before
    # in each tweet. it returns the capitalized 2gram that occurs most often
    # in the corpus given these contraints
    def get_host(self):

        candidates = []

        for tweet in self.corpus:
            if tweet.contains_word_partial("host"):
                candidates += map(lambda x: ' '.join(x), tweet.uppercased_2grams)

        cand_counter = Counter(candidates)
        # print(cand_counter.most_common(10))

        # get the highest counted object, and extract the string out of it
        return cand_counter.most_common(1)[0][0]


    def get_award_names(self):

        # candidates = []

        # for tweet in self.corpus:
        # 	if tweet.contains_word_partial("present"):
        # 		print(tweet)

        # let's hardcode these for now. we can revisit later if we have time

        ggpage = wikipedia.page("Golden Globe Award")
        award_list = ggpage.section("Motion picture awards")+ "\n"+ ggpage.section("Television awards")
        award_list = list(preprocess_awards(award_list))
        print(award_list)
        return award_list


    def get_all_award_info(self, award_list):

        # for award_tokens in award_list:

        # right now just test on the first award
      	award_info = self.get_info_for_award(award_list[3])


    def get_info_for_award(self, award_tokens):

        print(award_tokens, "\n\n")

        self.__get_presenters(award_tokens)
        self.__get_nominees(award_tokens)
        self.__get_winners(award_tokens)

        print("\n\n\n")

    def __get_presenters(self, award_tokens):

        # corpus = self.corpus_contain_best.filter_re_search('\w+\W\w+\W(won|wins)')
        corpus = self.corpus_contain_best_present.filter(lambda x: x.contains_all(award_tokens))

        print("presenter")

        candidates = []

        for tweet in corpus:
            print(tweet)
            # tweet.text = remove_stopwords(tweet.text, award_tokens)
            # tweet.split_text = tweet.text.split()
            candidate = list(filter(is_person,list(map(lambda x: ' '.join(x), tweet.uppercased_2grams))))
            candidates += candidate

        cand_counter = Counter(candidates)
        print(cand_counter.most_common(10))


    def __get_nominees(self, award_tokens):

        corpus = self.corpus_contain_best_nominee.filter(lambda x: x.contains_all(award_tokens))

        print("nominee")
        for tweet in corpus:
            print(tweet)


    def __get_winners(self, award_tokens):

        corpus = self.corpus_contain_best_win.filter(lambda x: x.contains_all(award_tokens))

        winner_is_movie = False if any(token in ['actress','actor'] for token in award_tokens) else True

        print("winner")

        candidates = []

        for tweet in corpus:
            print(tweet)
            candidate = tweet.re_findall(r'(\b[A-Z][\w,]*(?:\s+\b[A-Z][\w,]*)+)\s+(?:win|won)')
            if len(candidate) > 0 and winner_is_movie != is_person(candidate[0]):
                candidates += candidate

        cand_counter = Counter(candidates)
        print(cand_counter.most_common(10))
