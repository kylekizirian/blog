# Asking questions about the git history

I've found parsing through a git repo's history to be an excellent way
to learn both git and the unix shell. Git's interface is designed to be
shell friendly and it's fun to figure out how to get answers out of your
git history.

Let's look at a couple of questions we might want to ask and how we can
compose shell commands to get answers.

We'll look at CPython's history because it's particularly interesting.
Unfortunately, it's also particularly huge.

## How many commits are in the entire history?

The all-important `git rev-list` lists all commit hashes reachable from
the given commit on their own line. `wc -l` counts the number of lines
in stdin so combining the two will print the number of commits in our
history.

```
git rev-list HEAD | wc -l
```

## How many people have committed to this repo?

`git show` takes a commit and can print a variety of information about
the commit. By default it will print the commit message, the diff from
the previous commit, and some metadata about the author.

To extract just the author's name, we can use `--no-patch
--format='%an'` which prints just the author's name. Looping over the
first 10 most recent commits from `git rev-list` we can get the last 10
authors to commit to CPython.

The output of `git show` also displays in a paged output akin to
`less`. To get the output sent to stdout we can supply `--no-pager`. 

```
git rev-list HEAD -n 10 | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done
```

Now we've got an output with just the commit author on each line. What
we want is the total number of commit authors which we can get from the
number of unique lines from the author output. Let's give this a test
with just the last 10 commit authors.

```
git rev-list head -n 10 | while read commit; do git --no-pager show --no-patch --        format='%an' $commit; done | sort | uniq | wc -l
```

Looks right. Try with the entire git history.

```
git rev-list head -n 1000 | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done | sort | uniq | wc -l
```

2. Who has the most commits

How to print just the author's name from a commit

Use `git show` to get the information about a specific commit
or reference. For example

```
git show HEAD
```

Use the `--no-patch` flag to just print commit information and
not the diff.

The `--format` flag used to print specific information about the
commit. The `%an` format prints the author's name.

```
git rev-list HEAD -n 1 | git show  --no-patch --format="%an"
```

Get the last 10 committers

```
git rev-list head -n 10 | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done
```

Get the last 100 committers and print out # of commits from each

```
git rev-list head -n 100 | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done | sort | uniq -c
```

Get the last 10 most frequent committers

```
git rev-list head | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done | sort | uniq -c | sort -rn -k 1 | head -10
```

Note: this takes a _long_ time, recommend running it in the background
and redirecting the result to a file like so

```
git rev-list head | while read commit; do git --no-pager show --no-patch --format='%an' $commit; done | sort | uniq -c | sort -rn -k 1 | head -10 > top_authors.txt &
```

Check if it's still running later with

```
jobs
```

3. % of commits by top few committers

Get # of commits with

```
git rev-list head | wc -l
```

Get # of commits from top authors from top_authors.txt

```
cat top_authors.txt | while read author; do cut -d ' ' -f 1 ; done
```

Use bc awk and bc to get % of commits

```
git rev-list head | wc -l | read -d '' num_commits ; cat top_authors.txt | while read author; do cut -d ' ' -f 1 | awk -v num_commits=$num_commits '{print $0 "*100/" num_commits}' | bc -l ; done
```

Find what % of total commits is taken up by top 10 commit authors

```
git rev-list head | wc -l | read -d '' num_commits ; cat top_authors.txt | while read author; do cut -d ' ' -f 1 | awk -v num_commits=$num_commits '{print $0 "*100/" num_commits}' | bc -l | paste -s -d+ - | bc -l; done
```

4. How many times has a specific file changed?

## Other resources

This post is heavily influenced by a number of Gary Bernhardt's videos.
[The Unix Chainsaw](https://mislav.net/2014/02/hidden-documentation/)
whic is excellent.
