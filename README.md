# Job Application Manager

A desktop application built with Python and Tkinter to help you track and manage your job applications.

![App Preview](placeholder_app_preview.png)
_(Replace `preview.png` with an actual screenshot of your application)_

## Features

- **Add Applications**: Easily add new job applications with details like date, company name, job title, job description, and status.
- **View Applications**: Displays all applications in a sortable and filterable table.
- **Edit Applications**: Modify the details of existing applications.
- **Remove Applications**: Delete applications you no longer need to track.
- **Search/Filter**: Quickly find applications by company, job title, description, or status.
- **Sort**: Sort applications by date (newest/oldest), company name, job title, or status.
- **View Job Description**: Click to view the full job description in a separate pop-up window.
- **Persistent Storage**: Application data is saved locally in a `applications.json` file.
- **Dark Theme**: User-friendly dark interface.

## Prerequisites

- Python 3.x
- Tkinter (usually included with Python installations. If not, you may need to install it separately, e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu or `brew install python-tk` on macOS).

## Setup and Running

1.  **Clone the repository (or download the files):**

    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

    Or simply download the Python script (`main.py`) and the `applications.json` (if you have one already or it will be created).

2.  **Navigate to the project directory:**

    ```bash
    cd path/to/your/app
    ```

3.  **(Optional but Recommended) Create and activate a virtual environment:**

    - **Create:**
      ```bash
      python -m venv venv
      ```
    - **Activate:**
      - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
      - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Run the application:**
    ```bash
    python your_script_name.py
    ```
    (Replace `main.py` with the actual name of your Python file).

## Building with PyInstaller

To package the application into a single executable file, you can use PyInstaller.

1.  **Install PyInstaller:**
    If you haven't already, install PyInstaller (preferably within your activated virtual environment):

    ```bash
    pip install pyinstaller
    ```

2.  **Build the executable:**
    Navigate to your project directory in the terminal and run the following command:

    ```bash
    pyinstaller --onefile --windowed --name JobAppManager your_script_name.py
    ```

    - `--onefile`: Creates a single executable file.
    - `--windowed` (or `-w`): Prevents the command-line console from appearing when the GUI application runs.
    - `--name JobAppManager`: Sets the name of your executable.
    - `your_script_name.py`: Replace with the actual name of your Python script.

    After the build process is complete, you will find the executable in a `dist` folder within your project directory.

    **Note on data file (`applications.json`):**
    PyInstaller by default does not bundle data files like `applications.json`. The application will look for (or create) `applications.json` in the same directory where the executable is run. If you want to bundle default data or ensure the file is created alongside the executable in a specific way, you might need to adjust the script's data file handling or use PyInstaller's `--add-data` option.
    For this application, it's designed to create `applications.json` if it doesn't exist, so running the executable in a new directory will simply start with an empty list of applications.

## File Structure (Example)

```text
.
├── your_script_name.py     # Main application script
├── applications.json       # Data file (created/used by the app)
├── placeholder_app_preview.png # Screenshot of the app
├── requirements.txt        # Python dependencies (empty for this app)
└── README.md               # This file
```
