# Book Ninja 📚🥷

A polished terminal-based book data explorer built with Python 3 and the Open Library API. Search for books on almost any topic, browse detailed results, investigate publication trends, analyse title lengths and popular words, compare different subjects, and export your discoveries as CSV files. With colorful menus, clean statistics, and visual charts, Book Ninja turns real book data into an interactive investigation. 🔍📊✨

## Features

- 📚 Search books by topic using the Open Library API
- 🔎 Browse up to 500 results per investigation
- 📖 View book titles, authors, publication years, and edition counts
- 📑 Browse results in pages of 10 books
- 📊 View a summary of your search results
- 📅 Explore publication dates and trends by decade
- 📏 Analyse book title lengths
- 📝 Compare title lengths before and after 2000
- 🔤 Discover the most common words in book titles
- 🏆 Rank books by their number of editions
- ⚖️ Compare two topics side by side
- 📈 Display statistics using terminal bar charts
- 💾 Export book data to a CSV file
- 🎨 Colorful ANSI terminal interface
- 🧭 Simple interactive menu navigation
- 🛡️ Input validation and API error handling
- 🔑 No API key required

## Requirements

- Python 3.x
- requests
- Internet connection

## Installation

```bash
git clone https://github.com/Python-Swift15/Book-Ninja.git
cd Book-Ninja
python3 -m pip install requests
```

## Usage

```bash
python3 PY3bookninja.py
```

## How to Use

1. Launch Book Ninja in your terminal. 🚀
2. Select **Start a new investigation** or **Compare two topics**.
3. Enter a topic you want to explore, such as dragons, robots, or space. 🔍
4. Choose how many books to load.
5. Browse matching books and open individual results. 📚
6. Explore publication timelines, title lengths, and frequently used words. 📊
7. View the edition leaderboard to compare different books. 🏆
8. Export the loaded dataset to CSV if you want to use it elsewhere. 💾
9. Return to the menu to begin another investigation. 🔄

## Investigation Tools

- 📖 **Book Browser** — Explore titles, authors, first publication years, and edition counts
- 📅 **Publication Timeline** — Discover the oldest and newest books and visualise books by decade
- 📏 **Title Length Analysis** — Compare average title lengths and explore differences across publication periods
- 🔤 **Word Lab** — Find frequently repeated words in book titles
- 🏆 **Edition Leaderboard** — View the 10 books with the highest edition counts in your loaded results
- ⚖️ **Topic Comparison** — Compare two search topics using average publication years, title lengths, and editions
- 💾 **CSV Export** — Save your dataset for use in spreadsheets and other programs

## Data Analysis

Book Ninja retrieves information from Open Library and works with a selected sample of the search results.

Each book may include:

- 📚 Title
- ✍️ Author or authors
- 📅 First publication year
- 📖 Number of editions

Results may contain missing information, and topic matches are not always exact. Statistics describe the loaded results rather than every book ever published.

## Technical Details

- Built with Python 3
- Uses the `requests` library to access the Open Library Search API
- Processes JSON responses into structured Python dictionaries
- Uses `collections.Counter` to count publication decades and title words
- Uses `statistics.mean` to calculate averages
- Uses regular expressions to clean search topics and analyse text
- Uses ANSI escape sequences for bold text and terminal colors
- Includes reusable menu, prompt, and display functions
- Supports paginated book browsing and detailed book views
- Exports datasets using Python's built-in `csv` module
- Handles invalid inputs, network errors, and missing book data
- Requires no Open Library API key

## Future Enhancements

- ⭐ Save favourite books
- 📊 More detailed data visualisations
- 🏷️ Filter and sort search results
- 🔍 Advanced search options
- 📚 Search by author or publication year
- 💾 Save and reload previous investigations
- 📈 More comparison statistics
- 🖥️ Optional graphical interface
- 📤 Additional export formats
- 🌙 Customizable terminal themes

## License

Open source - Feel free to take inspiration!
