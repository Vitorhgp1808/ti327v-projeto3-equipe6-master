import os
import random
import re
import sys


DAMPING = 0.85
SAMPLES = 10000


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are a list of all other pages in the corpus that are linked to by the page.
    """
    """
        Analise um diretório de páginas HTML e verifique links para outras páginas.
    Retorne um dicionário onde cada chave é uma página e os valores são uma lista de todas as outras páginas do corpus às quais a página está vinculada.
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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next, given a current page.
    With probability `damping_factor`, choose a link at random linked to by `page`. With probability `1 - damping_factor`, choose a link at random chosen from all pages in the corpus.

    Retorna uma distribuição de probabilidade sobre qual página visitar em seguida, dada uma página atual.
    Com probabilidade `damping_factor`, escolha um link aleatoriamente vinculado por `page`. Com probabilidade `1 - damping_factor`, escolha um link aleatoriamente escolhido de todas as páginas do corpus.
    """
    distribution = dict()
    linked_pages = corpus[page]
    number_linked_pages = len(linked_pages)
    number_corpus= len(corpus)


    # Se a página não tem links, escolher uniformemente entre todas as páginas
    if number_linked_pages == 0:
        for p in corpus:
            distribution[p] = 1 / number_corpus
        return distribution

    # Caso contrário, aplicar o modelo de transição com amortecimento
    for p in corpus:
        distribution[p] = (1 - damping_factor) / number_corpus
        if p in linked_pages:
            distribution[p] += damping_factor / number_corpus
            
    return distribution
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are their estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    """
    """"
    Retorne valores de PageRank para cada página amostrando `n` páginas de acordo com o modelo de transição, começando com uma página aleatoriamente.
    Retorna um dicionário onde as chaves são nomes de páginas e os valores são o valor estimado do PageRank (um valor entre 0 e 1). Todos os valores do PageRank devem somar 1.
    """
    pagerank = dict()
    current_page = random.choice(list(corpus.keys()))

    for page in corpus:
        pagerank[page] = 0

    # Realizar n amostragens
    for _ in range(n):
        pagerank[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(model.keys()), weights=model.values(), k=1)[0]
        
    # Normalizar para garantir que a soma dos PageRanks seja 1
    total_samples = sum(pagerank.values())
    pagerank = {page: rank / total_samples for page, rank in pagerank.items()}
    return pagerank
    
 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating PageRank values until convergence.
    Return a dictionary where keys are page names, and values are their estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    
    Retorna valores de PageRank para cada página atualizando iterativamente os valores de PageRank até a convergência.
    Retorna um dicionário onde as chaves são nomes de páginas e os valores são seus valores estimados de PageRank (um valor entre 0 e 1). Todos os valores de PageRank devem somar 1.
    """


    raise NotImplementedError


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1]) #Se o número de argumentos for igual a 2, o programa continua executando. A próxima linha corpus = crawl(sys.argv[1]) chama a função crawl passando o segundo argumento fornecido pelo usuário (o nome do arquivo corpus). A função crawl é responsável por processar o arquivo corpus e retornar uma estrutura de dados que representa o conteúdo do arquivo.
    #print(corpus)
    #for page in corpus:
     #   print(f"{page} : {corpus[page]}")
    try:
        print(f"PageRank Results from Sampling (n = {SAMPLES})")
        ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
        print(ranks)
        """
        for page in sorted(ranks):
            print(f"  {page}: {ranks[page]:.4f}")
           
        print(f"PageRank Results from Iteration")
        ranks = iterate_pagerank(corpus, DAMPING)
        for page in sorted(ranks):
            print(f"  {page}: {ranks[page]:.4f}")  
        """

    except NotImplementedError:
        sys.exit("NotImplementedError")