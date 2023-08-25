# NewsNabber

This project is developed in Python and focuses on get articles using a crawler.

## Prerequisites

Before you start with the installation, make sure you have the following:

- Python (**3.6 or above**) installed on your system.
- `pip` installed to manage dependencies.

## Installation

We recommend creating and activating a virtual environment before installing the dependencies to avoid conflicts with other projects. Follow these steps:

1. Open a terminal in the project directory.

2. Create a virtual environment (you can use `venv`):

   ```bash
   python -m venv .venv
   ```

1. Activate the virtual environment:
    - On windows:
    ```bash
    .venv\Scripts\activate
    ```

    - On macOS and Linux:
    ```bash
    source .venv/bin/activate
    ```
    
2. Now that you're in the virtual environment, install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

To run the application, use the src/handler.py file. Running this file will create two folders: data and pages.

```bash
python src/handler.py
```

- The pages folder will contain HTML files (pages processed).
- The data folder will contain JSON files (structured data from html pages).
