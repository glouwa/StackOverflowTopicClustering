/*
const minwordlen = 2

export function tag_tf(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid].tags
            .filter(t=> t !== 'constructor')
            .forEach(tag=> result[tag] = result[tag]+1 || 1)
    return result
}

export function anc_dist(merge) {
    let result = {}
    for (var qid in merge) 
        result[merge[qid].answer_count] = result[merge[qid].answer_count ]+1 || 1            
    return result
}

export function isa_dist(merge) {
    let result = {}
    for (var qid in merge) 
        result[merge[qid].is_answered] = result[merge[qid].is_answered]+1 || 1
    return result
}

export function sco_dist(merge) {
    let result = {}
    for (var qid in merge)         
        result[merge[qid].score] = result[merge[qid].score]+1 || 1    
    
    //sort---
    return result
}

export function titleterm_dist(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid].title            
            .forEach(sentence=> {
                const terms = sentence.split(' ')
                terms.forEach(t=> {
                    if(t.length > minwordlen && !stopwords.includes(t)) 
                        result[t] = result[t]+1 || 1
                })                
            })
    
    return result
}

export function bodyterm_dist(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid].body            
            .forEach(sentence=> {
                const terms = sentence.split(' ')
                terms.forEach(t=> {
                    if(t.length > minwordlen && !stopwords.includes(t)) 
                        result[t] = result[t]+1 || 1
                })                
            })
    
    return result
}


export const stopwords = `
project
create
something
getting
running

trying
problem
understand
please
working

How
using
question
Thanks
However,
following

i
me
my
myself
we
our
ours
ourselves
you
your
yours
yourself
yourselves
he
him
his
himself
she
her
hers
herself
it
its
itself
they
them
their
theirs
themselves
what
which
who
whom
this
that
these
those
am
is
are
was
were
be
been
being
have
has
had
having
do
does
did
doing
a
an
the
and
but
if
or
because
as
until
while
of
at
by
for
with
about
against
between
into
through
during
before
after
above
below
to
from
up
down
in
out
on
off
over
under
again
further
then
once
here
there
when
where
why
how
all
any
both
each
few
more
most
other
some
such
no
nor
not
only
own
same
so
than
too
very
s
t
can
will
just
don
should
now`.split('\n')


*/