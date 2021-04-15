# find-annotations-usage-in-python

## What is annotation?
Annotaion is a metadata information for function/Class with the expected input type and expected output type

## Why annotation is used?

Annotation 
 - Enables static analyzers/IDEs show what types a function expects and returns  
 - Improves the interpretability of the code
 - Improves the documentation of the code
 - For more usecases, please refer to [annotation-usecases](https://www.python.org/dev/peps/pep-3107/#use-cases)


## How often are the built-in typing module annotations are being used in top python open-source repositories on Github?

To answer this question, 
- I had to get top 1000 repos with highest stars using github repos API
- Filter the repos using [typing](https://docs.python.org/3/library/typing.html) module using github search
- After filtering, got the count per each type in [Typing module](https://github.com/python/cpython/blob/3.8/Lib/typing.py) by downloading the repos and doing grep commands.
- Final Output is present in data/ folder


## How to run the script?

```console
foo@bar:~$ pip install -r requirements.txt 
```
The above command will install the necessary modules to run the script.

```console
foo@bar:~$ python main.py --token XXXXXXXX
```
Script will need a gitub token which can be created at [Token](https://github.com/settings/tokens)


