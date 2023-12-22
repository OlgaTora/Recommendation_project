import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
# Стоп-слова
import nltk
from nltk.corpus import stopwords

today = datetime.today()


class RecModel:

    def __init__(self, df, column_input, column_output, level_2seacrh):
        nltk.download('stopwords')
        stop_words = stopwords.words("russian")
        self.tfidf = TfidfVectorizer(stop_words=list(stop_words))
        self.df = df
        self.column_input = df[column_input]
        self.column_output = df[column_output]
        self.level = level_2seacrh

    def get_mapping(self):
        self.column_input = self.column_input.fillna('')
        mapping = pd.Series(self.df.index, index=self.column_output)
        return mapping

    def get_matrix(self):
        overview_matrix = self.tfidf.fit_transform(self.column_input)
        similarity_matrix = linear_kernel(overview_matrix, overview_matrix)
        return similarity_matrix

    def recommend_plan(self):
        mapping = self.get_mapping()
        plan_index = mapping[self.level]
        similarity_matrix = self.get_matrix()
        similarity_score = list(enumerate(similarity_matrix[plan_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[0], reverse=True)
        similarity_score = similarity_score[1:10]
        plan_indices = [i[0] for i in similarity_score]
        # return (df['numgroup'].iloc[plan_indices])
