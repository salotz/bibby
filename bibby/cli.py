#!/usr/bin/env python
import sys

import click
from pybtex.database import parse_file, BibliographyData, Entry

import bibby.bibby as bibby

PYBTEX_FORMAT = 'bibtex'

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


@click.command()
@click.option('-O', 'output', default=None, type=click.Path(exists=False),
              help='File to save modified bibtex file in.')
@click.option('-v', 'verbosity', default=1, help='verbosity of output')
@click.argument('bib', nargs=1, type=click.Path(exists=True))
@click.argument('field', nargs=1, type=str)
def remove_field(bib, field, output, verbosity):
    bib_path = bib
    bib = parse_file(bib)
    mod_entries = {}
    for key, entry in bib.entries.items():

        # find it whether it is in fields or persons
        is_fields = None
        if field in entry.fields:
            is_fields = True
        elif field in entry.persons:
            is_fields = False
        else:
            if verbosity > 0:
                print("'{}' field not found in the '{}' entry, skipping".format(field, key))
            mod_entries[entry.key] = entry
            continue

        fields_dict = dict(entry.fields)
        persons_dict = dict(entry.persons)
        # remove the field from the dictionary
        if is_fields:
            removed_field = fields_dict.pop(field)
        else:
            removed_field = persons_dict.pop(field)

        # recreate the entry and add to the new dictionary of entries
        new_entry = Entry(entry.type, fields=fields_dict, persons=persons_dict)
        mod_entries[entry.key] = new_entry

    # make a new bib dataset
    new_bib = BibliographyData(entries=mod_entries,
                               preamble=bib.preamble, wanted_entries=bib.wanted_entries)
    if output is not None:
        # write to a file
        new_bib.to_file(output, bib_format=PYBTEX_FORMAT)
    else:
        # just send to stdout
        sys.stdout.write(new_bib.to_string(PYBTEX_FORMAT))

@click.command()
def abbreviate_field():
    pass

@click.group()
def cli():
    pass

cli.add_command(fetch)
cli.add_command(remove_field)
cli.add_command(abbreviate_field)

if __name__ == "__main__":

    cli()



