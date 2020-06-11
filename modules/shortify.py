def shortify(text):
    if len(text) > 400:
        return f'{text[:400]}......'
    else:
        return text
