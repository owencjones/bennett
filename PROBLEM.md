# Bennett Institute coding problem

## The problem

Write a command line tool which uses the OpenPrescribing API to retrieve information about
prescribing of particular drugs and calculate how this varies around the country. There is a
detailed specification of the tool below.

There are three parts to the problem which build on each other, but there is no need for you to
leave your solution to early parts intact as you build later ones.

We've deliberately based this problem around some fairly slim documentation for a system you're not
familiar with because we think that finding your way through uncharted waters is an important skill
for developers. But if you really get stuck, please ask us for help.

We expect most candidates to spend around two to four hours on their solution, but that's not a
hard limit.

Please be prepared to talk about the trade-offs and other design decisions that you made in your
solution in any follow-up interview.

We're not trying to assess your skills in telepathy or your adherence to some arbitrary set of
secret criteria that we're not telling you about. If anything about the problem is unclear, or you
need a requirements decision, _please ask_. And there are no deliberate omissions or bugs: if you
find any, please let us know!


## Communication

If you've not used GitHub before, then you may find the following helpful:

* "[Creating an account on GitHub](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)"
* "[Uploading a project to GitHub](https://docs.github.com/en/get-started/start-your-journey/uploading-a-project-to-github)"
* "[Inviting collaborators to a personal repository](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository)"

## Assessment criteria

We'll assess your solution following these criteria, in order of priority.

1. Adherence to the requirements and specification below.
2. Simplicity and approachability of the code and documentation for other developers.
3. Completion of all parts of the problem.

We strongly advise you to focus on those criteria rather than inventing new requirements or
elaborating your solution in order to impress us.


## Requirements

* The tool can be written in Python or JavaScript. (The examples below use Python; the JavaScript
  version should be invoked like `node optool.js`.)
* The tool should have exactly the interface and output described below in the specification.
* The tool should handle all the functionality and concerns described below in the specification.
* You may use any third-party packages that you think are useful.
* You should include automated tests which _at least_ cover the parts of the code that you
  think most need testing. (You may choose to include other tests, but we recognise that for a toy project
  like this it's hard to apply the same criteria and approaches to testing as you would for
  production code.)
* You should include error handling for some cases that you think are important, but need not handle
  every possible error. You should make the behaviour in these cases sympathetic towards the user of
  the tool, who may not be a software developer.
* You need not deal with all the other concerns that production-ready code requires (for example
  logging and configuration). (But we're likely to ask you about these things in any follow-up
  interview.)
* Please don't use ChatGPT or another LLM to write the code for you. We understand that LLMs can be
  a useful tool in software development, but it's important for us to get an idea of your own
  coding skills.
* Do not include your name in your solution, so that we can review submissions anonymously.
* Include a README file which includes:
  * instructions for installing and running the tool, including providing dependencies;
  * a brief description of how the code is structured;
  * an explanation of any significant design decisions that you've made.


## Specification

OpenPrescribing.net is a website run by the Bennett Institute which uses publicly available data
about prescribing by GPs in England to provide useful tools to clinicians, researchers
and policy-makers.

The examples below all use a single code: `1304000H0AAAAAA`.
Here are some more example codes that you might like to use in your manual testing:
`0212000AAAAAIAI`, `0407010ADBCAAAB`, `0301020I0BBAFAF`, `040702040BEABAC`.


### Part 1

The OpenPrescribing site identifies drugs by their "BNF codes". BNF codes have a defined structure
so, for example, part of the code for a drug identifies the chemical substance and part identifies
how the drug is presented.

This blog post gives a short overview of what different parts of a BNF code mean:
https://www.bennett.ox.ac.uk/blog/2017/04/prescribing-data-bnf-codes/.

Your tool should take the full 15 character BNF code for a drug, identify the code for that drug's
chemical substance, look up the name of the chemical using the `bnf_code` endpoint of the
OpenPrescribing API and print it out.

The API is documented here: https://openprescribing.net/api/.

Here is an example of the output that your tool should produce:
```
$ python optool.py 1304000H0AAAAAA

Clobetasone butyrate
```


### Part 2

The OpenPrescribing API allows you to see how much of this chemical has been prescribed in NHS
England over the last five years, using the `spending_by_org` endpoint.

When requesting spending data you can specify the type of NHS organisation you want the spending
broken down by. For instance, you can get data at the level of individual GP practices or at the
level of regional teams which cover large areas of the country. We are interested in data at the
level of Integrated Care Boards (ICBs).

Extend your tool to fetch spending data on the chemical you found in Part 1 for all ICBs. Then, for
each month in the results, find the ICB which has prescribed this chemical most frequently (as
measured by the `items` field) and print it out. If there is a tie then choose the first ICB returned
by the API.

Here is some example output (note only a subset of the full results is shown, omitted parts marked
with `...`):
```
$ python optool.py 1304000H0AAAAAA

Clobetasone butyrate

...
2024-01-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-02-01 NHS NORTH EAST AND NORTH CUMBRIA INTEGRATED CARE BOARD
2024-03-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-04-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-05-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-06-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-07-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-08-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-09-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-10-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-11-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
2024-12-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD
...
```


### Part 3

Comparing the number of items for each ICB directly in this way does not take into account the fact
that each ICB may be responsible for different numbers of patients. We would like to take account
of this difference when calculating the rankings by weighting the number of items by the ICBs
"total list size" (which means the total number of patients registered at all GP practices in
the ICB).

You can use the `org_details` endpoint to retrieve the `total_list_size` value for all ICBs. This
can then be used to calculate the ICB with the highest number of items _per patient_ in each month.
Note that the `total_list_size` changes from month to month and your solution should account for
this.

Update your tool to optionally weight its results by population size.

Here is some example output (note only a subset of the full results is shown, omitted parts marked
with `...`):
```
$ python optool.py --weighted 1304000H0AAAAAA

Clobetasone butyrate

...
2024-01-01 NHS DEVON INTEGRATED CARE BOARD
2024-02-01 NHS DEVON INTEGRATED CARE BOARD
2024-03-01 NHS DEVON INTEGRATED CARE BOARD
2024-04-01 NHS CORNWALL AND THE ISLES OF SCILLY INTEGRATED CARE BOARD
2024-05-01 NHS NORFOLK AND WAVENEY INTEGRATED CARE BOARD
2024-06-01 NHS CORNWALL AND THE ISLES OF SCILLY INTEGRATED CARE BOARD
2024-07-01 NHS DEVON INTEGRATED CARE BOARD
2024-08-01 NHS BIRMINGHAM AND SOLIHULL INTEGRATED CARE BOARD
2024-09-01 NHS DEVON INTEGRATED CARE BOARD
2024-10-01 NHS DEVON INTEGRATED CARE BOARD
2024-11-01 NHS DEVON INTEGRATED CARE BOARD
2024-12-01 NHS DEVON INTEGRATED CARE BOARD
...
```
