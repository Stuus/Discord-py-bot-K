import glob
for f in glob.glob('E:/Project/Discord-py-bot-K/Cogs/*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('C.libiue', 'C.lightblue')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
