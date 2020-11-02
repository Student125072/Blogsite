def shortify(text):
    if len(text) > 200:
        return f'{text[:200]}......'
    else:
        return text