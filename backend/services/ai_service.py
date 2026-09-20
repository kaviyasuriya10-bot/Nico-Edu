from config import settings
class AIUnavailable(Exception): pass
def respond(prompt:str):
    if not settings.ai_provider or not settings.ai_api_key: raise AIUnavailable('AI is not configured. Add AI_PROVIDER, AI_API_KEY and AI_MODEL to backend/.env, then restart the server.')
    if settings.ai_provider == 'openai':
        from openai import OpenAI
        client=OpenAI(api_key=settings.ai_api_key)
        r=client.chat.completions.create(model=settings.ai_model or 'gpt-4o-mini',messages=[{'role':'system','content':'You are NicoEdu, a clear, supportive educational tutor.'},{'role':'user','content':prompt}])
        return r.choices[0].message.content
    raise AIUnavailable(f'AI provider {settings.ai_provider!r} is not supported yet.')
