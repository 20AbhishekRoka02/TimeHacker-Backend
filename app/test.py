import requests as req

res = req.get("postgres://default:zQP9da1wetiY@ep-hidden-sun-a4txcv4h.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
print(res)