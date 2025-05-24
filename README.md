# test task okx_parser
# task:
**This script should be able to:**

1. Specify a date range: Take START_DATE and END_DATE as inputs to define which news to fetch.
2. Define output location: Accept a FOLDER parameter to designate where the downloaded data will be stored. 
3. Capture full content: Scrape both the title and body of each news article. 
4. Avoid APIs: Strictly do not use any official OKX APIs; direct web scraping is required. 
5. Organize output: Store the extracted news within the specified FOLDER, using a file structure of your choice.

**Key Considerations:**

1. Maintainability: Design the project structure with future development and collaboration in mind. How can it be easily versioned, installed, and used by other developers?
2. Library usage: Any reasonable Python libraries are permissible. 
3. Deployment readiness: Anticipate potential issues when deploying this solution on a remote server and consider proactive measures to mitigate them.

## possible solutions:

### Solution 1. parse all existing news and save it in local storage:
    1) start script with required period and folder
    2) check required period in the local storage
        period hits:
           1) save response in required folder without parsing
        period mis:
           1) update the local storage: parse all news until we get matching existing record in our storage and parsed news record

### Solution 2. parse every time or running script
    1) get total pages qty
    2) find according dates for first and last page
    3) make binary search for seeking period with news parsing

## Chosen decision
Chose to implement the second solution cause it is faster to implement and doesn't require database.

If there is a need to make news parsing for different clients and not doing many request :
1. implement Solution 1. parse all existing news and save it in local storage.
2. update it to microservice with api by implementing new presenter

PS.
If we have a need to add different sources, we can extract abstract interface from each actor we use now.


## implemented features
- parsing news from okx.com for selected period START_DATE and END_DATE
- saving file to selected directory

## Install uv
```bash
$ python3 -m pip install uv
$ uv python install 3.13
```

## install depends
```bash
$ uv venv --python 3.13
$ . ./bin/activate
$ uv pip install
```

## run tests

```bash
$ python -m pytest -vvs
```

## run 
```bash
uv run -- entrypoint.py --start-date 2025-04-20 --end-date 2025-04-21 --folder tmp
```
