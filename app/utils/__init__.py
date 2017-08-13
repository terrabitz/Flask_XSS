def snake_to_title(string):
    return ' '.join([word.capitalize() for word in string.split('_')])