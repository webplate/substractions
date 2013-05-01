def flatten(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el

print [i for i in flatten([[[1, 2, 3], [4, 5]], 6])]

bugs = [['unexplained'], ['pt-gd', 'pt-gd=gd', '0-N=N'], ['blank', ['pt-gd', 'pt-gd=gd', '0-N=N']], ['unexplained']]

print [i for i in flatten(bugs)]
