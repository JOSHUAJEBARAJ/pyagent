import loop 



message=None
while True:
    prompt=input(">")
    message=loop.run(prompt,message)