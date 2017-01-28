import bibsonomy

def bibsonomy_post_to_bibtex(post):
    """Convert a bibsonomy post to a bibtex string"""

    bibtex_attr_names = [attr for attr in dir(post.resource) if not attr.startswith("_")]
    if 'bibtex_key' not in bibtex_attr_names:
        raise ValueError("bibtex key not found")

    bibtex_entry = {attr_name : post.resource.__dict__[attr_name] for
                    attr_name in bibtex_attr_names}
    bibtex_entry_str = "@{0}{{{1}".format(bibtex_entry['entry_type'],
                                          bibtex_entry['bibtex_key'])
    for attr_name, attr in bibtex_entry.items():
        if attr_name in ['bibtex_key', 'entry_type', 'intra_hash', 'inter_hash']:
            continue
        bibtex_entry_str = '{0},\n{1} = {{{2}}}'.format(bibtex_entry_str,
                                                    attr_name, attr)

    bibtex_entry_str = "{0}\n}}\n\n".format(bibtex_entry_str)
    return bibtex_entry_str


def retrieve_bibsonomy_posts(user, token):
    source = bibsonomy.RestSource(user, token)
    bib = bibsonomy.BibSonomy(source)
    posts = bib.getPostsForUser("publications", user, None)
    return posts

def posts_to_bibtex_strings(posts):
    bibtex_strings = [bibsonomy_post_to_bibtex(post) for post in posts]
    return bibtex_strings

def write_bib(bibtex_strings, bib_target):
    with open(bib_target, 'w') as wf:
        for bibtex_str in bibtex_strings:
            wf.write(bibtex_str)
