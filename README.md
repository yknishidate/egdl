# EGDL

**Unofficial** API for Eurographics digital library

## Features

- Get the most recent articles
- Search for articles

## Sample

Get the most recent articles

```python
import egdl

page_links = egdl.get_recently_added_links()
for page_link in page_links:
    print("Link:", page_link)
    article = page_link.get_article()
    print("Title:", article.title)
    print("Abstract:", article.abstract)
    print("Authors:", article.authors)
```

Search for articles

```python
import egdl

page_links = egdl.search("deep learning")
for page_link in page_links:
    print("Link:", page_link)
    article = page_link.get_article()
    print("Title:", article.title)
    print("Abstract:", article.abstract)
    print("Authors:", article.authors)
```
