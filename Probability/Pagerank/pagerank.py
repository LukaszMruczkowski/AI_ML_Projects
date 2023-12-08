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
    # Dictionary representing probability distribution
    model = dict()

    # Set to store values from corpus about certain page's links
    possible_pages = corpus.get(page)

    # Check if current page has any links
    if len(possible_pages) != 0:
        
        # Number of pages that current page has links to
        links_number = len(possible_pages)

        # Number of all links including current page
        pages_number = links_number + 1

        # Probability that random page will be chosen
        probability_for_random = 1 - damping_factor

        # Probability to choose among other pages than current
        probability_other = round((damping_factor / links_number) + (probability_for_random / pages_number), 3)

        # Probability to choose current page among random
        probability_current = round(probability_for_random / pages_number, 3)

        # List of every possible page including current
        model_keys = list(possible_pages)
        model_keys.append(page)

        # Adding probability to every page
        for p in model_keys:
                # Probability for current page
                if p == page:
                    model[p] = probability_current
                else:
                    model[p] = probability_other
    # Page doesn't have any links
    else:
        pages_number = len(corpus)

        # Probability to choose among all pages
        probability = round(1 / pages_number, 3)

        # List of every possible page
        model_keys = list(corpus.keys())

        # Adding probability to every page
        for p in model_keys:
                model[p] = probability

    return model






def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # List of all possible pages
    all_pages = list(corpus.keys())

    # PageRank dictionary
    page_rank = dict()
    for p in all_pages:
        page_rank[p] = 0

    # Keep track of last page chosen to call on it new transition
    last_page = ""

    for i in range(n):

        # First sample
        if i == 0:
            random_page = random.choice(all_pages)
            sample_model = transition_model(corpus, random_page, damping_factor)
        else:
            sample_model = transition_model(corpus, last_page, damping_factor)
            
        # Drawn page variable
        chosen_page = ""

        # Variable to store cumulation of probabilities in order to draw a page
        cumulative_probability = 0

        # Generate a random float between 0 and 1
        random_number = random.random()

        # Draw a page
        for page, probability in sample_model.items():
            cumulative_probability += probability
            if random_number < cumulative_probability:
                chosen_page = page
                last_page = chosen_page
                break
        
        # Add drawn page to counter
        for page in page_rank:
            if page == chosen_page:
                page_rank[page] += 1
                break
            
    # Turn counters of pages into percentage values
    for page in page_rank:
        page_rank[page] /= n

    return page_rank
        
            



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Number of all pages in corpus
    N = len(corpus.keys())
    
    # Page_rank distribution dictionary
    page_rank = dict()
    for page in corpus:
        page_rank[page] = 1 / N
    
    while True:
        # Counter to see if every rank don't change more than 0.001
        count = 0

        # Make new rank for every page
        for page in corpus:
            # Adaptation of page rank iteration formula
            new_rank = (1 - damping_factor) / N
            summary = 0
            for p in corpus:
                if len(corpus[p]) == 0:
                    num_links = len(corpus)
                    summary = summary + page_rank[p] / num_links
                if page in corpus[p]:
                    num_links = len(corpus[p])
                    summary = summary + page_rank[p] / num_links
            summary *= damping_factor
            new_rank += summary

            # Check if rank changed more than 0.001
            if abs(page_rank[page] - new_rank) < 0.001:
                count += 1
            # Insert new iteration formula page rank
            page_rank[page] = new_rank
            
        # If every page don't change rank more than 0.001 it's done
        if count == N:
            break
        
    return page_rank

if __name__ == "__main__":
    main()
