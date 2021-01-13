"""depends on NLTK"""

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from rake_nltk import Rake
import heapq
import string

class Sentence_rank:
    def sentence_rank(self,document):
        # Object of automatic summarization.
        auto_abstractor = AutoAbstractor()
        # Set tokenizer.
        auto_abstractor.tokenizable_doc = SimpleTokenizer()
        # Set delimiter for making a list of sentence.
        auto_abstractor.delimiter_list = [".","\n"]
        # Object of abstracting and filtering document.
        abstractable_doc = TopNRankAbstractor()
        # Summarize document.
        result_dict = auto_abstractor.summarize(document, abstractable_doc)


        score = [x[1] for x in result_dict["scoring_data"]]
        res = dict(zip(result_dict["summarize_result"], score))

        # 10 is the argument for the maximum lines count
        summary_sentences = heapq.nlargest(3, res, key=res.get)
        summary = ''.join(summary_sentences)
        return summary


class Extract_keyphrases:
    def extract_keyphrases(self,document):
        r = Rake(punctuations=string.punctuation)
        r.extract_keywords_from_text(document)
        phrases = r.get_ranked_phrases()

        parsed_phrases = []
        for prase in phrases:
            if len(prase.split()) >= 2:
                parsed_phrases.append(prase)
        
        return parsed_phrases

class Remove_punctuations:
    # This will be useful for removing extra characters while summarizing code changes
    def remove(self,document):
        lines_added = []
        for i in document:
            punctuation = string.punctuation
            punctuation = punctuation.replace("_","")
            translated = i[1].translate(str.maketrans('', '', punctuation))
            lines_added.append(translated)
            document = "\n".join(lines_added)
        return document

# dictonary = {'added': [(27, 'def transform_chosen_check(check):'), (28, '    """"""Transform the chosen check from the provided command-line arguments.""""""'), (29, '    # add ""check_"" to the name of the checker so that it looks like, for instance,'), (30, '    # ""check_CountCommits"" when ""CountCommits"" is chosen on command-line'), (31, '    transformed_check = constants.checkers.Check_Prefix + check'), (32, '    return transformed_check'), (33, ''), (34, '')], 'deleted': []}

# added = dictonary["added"]

# r = Remove_punctuations()
# document = r.remove(added)
# c = Sentence_rank()
# out = c.sentence_rank(document)

# print(out)

# c = Extract_keyphrases()
# final = c.extract_keyphrases(out)
# print("\nkeyphrases:\n")
# print(final)
# # print("\n")
# # s = Sentence_rank()
# # print(s.sentence_rank(document))


