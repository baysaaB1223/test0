def asuult1(user_query):
    return user_query


keywords = ["утас", "contact", "холбоо барих"]

def asuult2(user_query):
    if any(k in user_query.lower() for k in keywords):
        return "Манай холбооо барих утасны дугаар: 99887766"
    else:
        return asuult1(user_query)