from google.cloud import language


def analyze_sentiment(text):
    if text:
        client = language.LanguageServiceClient()
        document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        return score if score else 0
    return 0
