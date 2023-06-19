# Youtube SEO Optimizer
Optimizes the SEO meta items for a Youtube video using ChatGPT

### Request:
```
curl --location --request POST 'http://127.0.0.1:5000/youtube-seo-optimize' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://youtu.be/Sr9iZd9fXpA"
}'
```
### Response
```
{
    "description": "Learn how to easily embed a custom ChatGPT chatbot into your website or live chat. With the sharing tab feature in Custom GPT, you can effortlessly manage and apply your chatbot according to your preferences. Follow the step-by-step guide to enable sharing, embedding, and live chat features for your chatbot.",
    "tags": [
        "custom GPT",
        "embed chatbot",
        "website chatbot",
        "live chatbot",
        "chatbot platform",
        "user-friendly interface"
    ],
    "title": "How To Embed A Custom ChatGPT Chatbot Into Your Website"
}
```
