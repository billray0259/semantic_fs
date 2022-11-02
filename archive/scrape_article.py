import bs4
import requests

while True:
    url = input("article url: ")
    res = requests.get(url)
    res.raise_for_status()

    # Parse the page
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get the title
    title = soup.select('title')[0].getText()
    print(title)

    # concatenate all the paragraphs
    article = "\n".join([p.getText().strip() for p in soup.select('p')])

    # Print the article
    print(article)

    # Save the article <title>.txt
    name = title.replace(' ', '_') + '.txt'
    with open(f"data_directory/texts/{name}", 'w') as f:
        f.write(article)