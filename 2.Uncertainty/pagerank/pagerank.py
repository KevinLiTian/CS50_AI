import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus: dict({"1.html: set({2.html, 3.html})", 2.html: set({3.html})})
    probabilities = {}

    # If no link to other pages, choose at random, all pages have same probability
    if len(corpus[page]) == 0: 
        for webpage in corpus:
            probabilities[webpage] = 1/len(corpus)

        return probabilities

    # Otherwise the pages that are link to have the probability resulting from the sum of
    # selecting through links and selecting at random from all pages.
    prob_at_random = (1-damping_factor)/len(corpus)
    for webpage in corpus[page]:
        probabilities[webpage] = damping_factor/len(corpus[page]) + prob_at_random

    # The page that are not link to have the probability of selecting at random from all pages
    for webpage in corpus:
        if webpage not in corpus[page]:
            probabilities[webpage] = prob_at_random

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Keep track of how many times each page has been visited
    # Initialize all pages to 0
    visited = {}
    for webpage in corpus:
        visited[webpage] = 0

    # First choose at random from all pages
    probabilities = [1/len(corpus)] * len(corpus)
    first_choice = random.choices(population=list(corpus.keys()), weights=probabilities, k=1)[0]

    # Repeat the process for SAMPLES times, similar to the Markov chain
    choice = first_choice
    for sample in range(n):
        prob = transition_model(corpus, choice, damping_factor)
        choice = random.choices(population=list(prob.keys()), weights=list(prob.values()), k=1)[0]
        visited[choice] += 1

    PageRank = {}
    for webpage in visited:
        PageRank[webpage] = visited[webpage] / n

    return PageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
