#%%
!pip install pyjokes
#%%
# pip install pyjokes
import pyjokes
import requests

webhook_url = "https://hooks.slack.com/services/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"

joke = pyjokes.get_joke()

#joke = 'I like telling jokes'
data = {'text': joke}
requests.post(url=webhook_url, json = data)