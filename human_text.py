"""Language boundaries for user-authored text, never credentials or generated questions."""
from text_filter import acceptable

MESSAGE='Please reword this without offensive language.'
TEXT_KEYS=frozenset('alias name username device title description purpose label behaviours note text reflection explanation nextWin companionName message content supporter sponsor saved backup review_note accessNote backupNote explain email change reason plan cancellation writing value'.split())
SKIP=frozenset('password passphrase username code recovery token id key questions options prompt hint example baseline'.split())

def text_fields(value,key=''):
    if key in SKIP:return
    if isinstance(value,dict):
        for field,item in value.items():
            yield from text_fields(item,'answer' if key=='answers' else field)
    elif isinstance(value,list):
        for item in value:yield from text_fields(item,key)
    elif isinstance(value,str) and (key in TEXT_KEYS or key=='answer'):
        yield value

def valid_payload(value):
    return all(acceptable(text) for text in text_fields(value))

def display_safe(value,key=''):
    """Redact legacy display text without changing the stored evidence or credentials."""
    if key=='questions' and isinstance(value,list):
        return [{**item,'answer':display_safe(item['answer'],'answer')} if isinstance(item,dict) and 'answer' in item else item for item in value]
    if key in SKIP:return value
    if isinstance(value,dict):return {field:display_safe(item,'answer' if key=='answers' else field) for field,item in value.items()}
    if isinstance(value,list):return [display_safe(item,key) for item in value]
    if isinstance(value,str) and (key in TEXT_KEYS or key=='answer') and not acceptable(value):return 'Text needs revision.'
    return value
