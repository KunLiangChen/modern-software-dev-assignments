# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 2: Add Unit Tests
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
1. In `week2/app/routers/notes.py`, add a GET endpoint at the root path (`/notes`) that returns a list of all notes from the database using `db.list_notes()`.
2. In `week2/frontend/index.html`:
   - Add an "Extract LLM" button that calls the existing `/action-items/extract-llm` endpoint.
   - Add a "List Notes" button that calls the new `/notes` endpoint and displays the results in the `#items` div.
   - Refactor the JavaScript to share logic between the extraction buttons and handle displaying notes.
``` 

Generated Code Snippets:
```
week2/app/routers/notes.py:
- Lines 73-87: Added `list_all_notes` GET endpoint.

week2/frontend/index.html:
- Lines 28-30: Added "Extract LLM" and "List Notes" buttons.
- Lines 42-101: Updated script to handle new buttons and render notes.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the week2 directory structure and contents. Create a professional README.md that includes:
- A clear project overview highlighting heuristic and LLM extraction modes.
- Tech stack details (FastAPI, SQLite, Ollama, etc.).
- Getting started guide with environment setup and Ollama configuration.
- Comprehensive API reference for action-items and notes endpoints.
- Testing instructions and a directory structure breakdown.
Maintain a professional and developer-friendly tone throughout.
``` 

Generated Code Snippets:
```
week2/README.md: Created new file with comprehensive project documentation.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 