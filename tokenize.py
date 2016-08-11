# Given input text, return list with tokens
def input_file_lines(input_text, tokens):
	tokens = input_text.splitlines();
	return tokens

def input_file_words(input_text, tokens):
	tokens = input_text.split();
	return tokens