from roles import USER_ROLES

def get_prompt(role, question):
    base_prompt = USER_ROLES.get(role, "")
    return f"{base_prompt}\n\nQuestion: {question}"
