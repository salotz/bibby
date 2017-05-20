#!/usr/bin/env python

import click

import bibby.bibby as bibby

@click.command()
@click.option('-v', 'verbosity', default=1, help='verbosity of output')
@click.argument('user', nargs=1, type=str)
@click.argument('token', nargs=1, type=str)
@click.argument('bib', nargs=1, type=click.Path(exists=True))
def fetch(verbosity, user, token, bib):
    # get the posts and report
    posts = bibby.retrieve_bibsonomy_posts(user, token)

    if verbosity > 0:
        print("Retrieved {} reference posts".format(len(posts)))

    # convert to bibtex file strings
    bibstrings = bibby.posts_to_bibtex_strings(posts)

    # write them to the target
    bibby.write_bib(bibstrings, bib)

    if verbosity > 0:
        print("Saved to {}".format(bib))

@click.group()
def cli():
    pass

cli.add_command(fetch)

if __name__ == "__main__":

    cli()



