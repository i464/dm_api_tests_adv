from json import loads

def get_activation_token_by_login(login, messages_response):
    for item in messages_response.json().get("items", []):
        body = loads(item["Content"]["Body"])
        if body.get("Login") == login:
            url = body.get("ConfirmationLinkUrl") or body.get("ConfirmationLinkUri")
            if url:
                return url.rsplit("/", 1)[-1]
    return None

def get_confirmation_token_by_email(to_email, messages_response):
    for item in messages_response.json().get("items", []):
        to_list = item["Content"]["Headers"].get("To", [])
        if to_list and to_list[0] == to_email:
            body = loads(item["Content"]["Body"])
            url = body.get("ConfirmationLinkUrl") or body.get("ConfirmationLinkUri")
            if url:
                return url.rsplit("/", 1)[-1]
    return None
