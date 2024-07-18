# #import spacy

# nlp = spacy.load("en_core_web_sm")

# # Synonym dictionary for demonstration purposes
# synonyms = {
#     "introduction": ["intro", "beginning", "start"],
#     "main topic": ["main subject", "central theme", "core idea"],
#     "conclusion": ["end", "summary", "wrap-up"]
# }

# def is_point_covered(transcript_tokens, point):
#     point_text_lower = point.lower()
#     if point_text_lower in transcript_tokens:
#         return True

#     for synonym in synonyms.get(point_text_lower, []):
#         if synonym in transcript_tokens:
#             return True

#     return False

# def process_transcript(transcript):
#     doc = nlp(transcript)
#     return [token.text.lower() for token in doc]