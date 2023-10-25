import wikipedia
wikipedia.set_lang("ru")


def get_exception():
    while True:
        try:
            ran_article = wikipedia.random()
            sum_article = wikipedia.summary(ran_article)
            break
        except wikipedia.exceptions.DisambiguationError:
            continue
        except wikipedia.exceptions.PageError:
            continue
        except wikipedia.exceptions.RedirectError:
            continue
        except wikipedia.exceptions.HTTPTimeoutError:
            continue
    return sum_article, ran_article
