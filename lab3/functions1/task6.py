def reverse_words(sentence):
    words = sentence.split()
    return ' '.join(reversed(words))

sentence = input()
print(reverse_words(sentence))
