import os
import random
import re
import sys
import math

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
    t_dict = {}
    total = 0

    if corpus[page]:
        for i in corpus:
            t_dict[i] = (1-damping_factor) / len(corpus)
            if i in corpus[page]:
                t_dict[i] += damping_factor / len(corpus[page])
    else:
        # If page has no outgoing links then choose randomly among all pages
        for i in corpus:
            t_dict[i] = 1 / len(corpus)

    # Run a check to make sure the total probability is equal to 1 before returning the result
    for i in t_dict:
        total += t_dict[i]
    if round(total, 2) != 1.0:
        raise Exception('Transition probability total is not 1, fatal error')

    return t_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    s_dict = {}
    sample = None
    total = 0

    for i in corpus:
        # create and set all items in sample dictionary to have a probability of 0
        s_dict[i] = 0

    for i in range(n):
        if sample is None:
            # choose a random page during the start of the sampling process
            sample = random.choice(list(corpus.items()))[0]
        else:
            # continue to find new samples by pushing the previous sample into the transition model
            var = transition_model(corpus, sample, damping_factor)
            page, weight = zip(*var.items())
            sample = random.choices(page, weights=weight)[0]

        # Once a sample is found, increment its value in the dictionary
        s_dict[sample] += 1

    for i in s_dict:
        # Normalize the sample values to meet a probability distribution standard
        s_dict[i] /= n

    # Run a check to make sure the total probability is equal to 1 before returning the result
    for i in s_dict:
        total += s_dict[i]
    if round(total, 2) != 1.0:
        raise Exception('Sampling probability total is not 1, fatal error')

    return s_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    i_dict = {}
    compare_dict = {}
    prob = 0

    # set all keys to have a value of 1/N
    for page in corpus:
        i_dict[page] = 1/len(corpus)

    # initialize iteration flag
    repeat = True

    while repeat:
        for page in i_dict:
            total = 0

            for pages in corpus:
                if page in corpus[pages]:
                    # if a page from i_dict is a found as a value in corpus, then we do the following
                    total += i_dict[pages] / len(corpus[pages])
                if not corpus[pages]:
                    # if a particular key in corpus produces no value, then we do the following
                    total += 1 / len(corpus)

            # Store the new iteration value so it can be compared
            compare_dict[page] = (1 - damping_factor) / len(corpus) + damping_factor * total

        # reset the flag so the loop stops temporarily until the check is finalized
        repeat = False

        for page in i_dict:
            # perform the check, if the difference is greater than 0.001 the loop restarts
            if not math.isclose(compare_dict[page], i_dict[page], abs_tol=0.001):
                repeat = True
            # assign the new value to the iteration dictionary
            i_dict[page] = compare_dict[page]

    # Run a check to make sure the total probability is equal to 1 before returning the result
    for i in i_dict:
        prob += i_dict[i]
    if round(prob, 2) != 1.0:
        raise Exception('Iteration probability total is not 1, fatal error')

    return i_dict


if __name__ == "__main__":
    main()
