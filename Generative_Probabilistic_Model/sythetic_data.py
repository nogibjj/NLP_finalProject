# this code is to generate sythetic email data
import sys
import os
import pandas as pd
import random

# import packages from Generative_Probabilistic_Model
sys.path.append(os.path.abspath(os.path.join("..")))
from Generative_Probabilistic_Model.ProcessEmail import process_email_body_simple

# Load the data
df = pd.read_csv("/workspaces/NLP_finalProject/data/completeSpamAssassin.csv")

# Splitting the dataframe into two based on the label
spam_df = df[df["Label"] == 1]
non_spam_df = df[df["Label"] == 0]

# Applying the simplified processing function to each group
spam_emails = spam_df["Body"].apply(process_email_body_simple)
non_spam_emails = non_spam_df["Body"].apply(process_email_body_simple)

# Compile the processed emails into separate lists for spam and non-spam
spam_list = [line for email in spam_emails for line in email]
non_spam_list = [line for email in non_spam_emails for line in email]

# Display the first few elements of the compiled simple list to verify the structure
sample_spam = spam_list[:800]  # 300
sample_nonspam = non_spam_list[:1000]  # 500
# print(sample_spam[0])
# print(sample_spam)
vocabulary = sorted(
    set(token for sentence in sample_spam + sample_nonspam for token in sentence)
) + [None]


# define a function that create dictionaries for spam and non-spam that records the frequency of each word
def create_dict(vocabulary, emails):
    dict = {}
    for word in vocabulary:
        dict[word] = 1
    for lines in emails:
        for word in lines:
            dict[word] += 1
    return dict


def select_next(vocab_freq):
    # print("stochastic running")
    weight = [val for val in vocab_freq.values()]
    ls = [e for e in vocab_freq.keys()]
    return random.choices(ls, weight, k=1).pop()


def generate_sythetic(original_data, vocabulary):
    nlines = len(original_data)
    vocab_freq = create_dict(vocabulary, original_data)
    sythetic_data = []
    for _ in range(nlines):
        line = []
        while len(line) < 15:
            next_word = select_next(vocab_freq)
            line.append(next_word)
        sythetic_data.append(line)
    return sythetic_data


if __name__ == "__main__":
    spam_sythetic = generate_sythetic(sample_spam, vocabulary)
    nonspam_sythetic = generate_sythetic(sample_nonspam, vocabulary)
    print(nonspam_sythetic)
