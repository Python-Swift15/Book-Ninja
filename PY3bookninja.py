#!/usr/bin/env python3
"""
BOOK NINJA — Open Library Data Explorer
Upgraded from the Code Ninja Data Investigation worksheet.

Requires:
    pip install requests

Run:
    python3 book_ninja.py
"""

import csv
import os
import re
import sys
import time
from collections import Counter, defaultdict
from statistics import mean

try:
    import requests
except ImportError:
    print("\nBOOK NINJA needs the 'requests' package.")
    print("Install it with:  python3 -m pip install requests\n")
    raise SystemExit(1)


# ─────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

WIDTH = 68
API_URL = "https://openlibrary.org/search.json"

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "book", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "the", "to", "with", "your", "my",
    "this", "that", "into", "its", "vol", "volume", "edition"
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line(char="─"):
    print(DIM + char * WIDTH + RESET)


def title(text, subtitle=None):
    clear()
    print(CYAN + BOLD + "╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + text.center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝" + RESET)
    if subtitle:
        print(DIM + subtitle.center(WIDTH) + RESET)
    print()


def heading(text):
    print("\n" + BOLD + WHITE + text + RESET)
    line()


def pause():
    input(DIM + "\nPress Enter to continue..." + RESET)


def prompt(text, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(CYAN + BOLD + f"{text}{suffix}: " + RESET).strip()
    return value if value else default


def choose(options, text="Choose an option"):
    print()
    for i, option in enumerate(options, 1):
        print(f"  {CYAN}{BOLD}{i:>2}{RESET}  {option}")
    while True:
        answer = input(CYAN + BOLD + f"\n{text}: " + RESET).strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer)
        print(RED + "Please enter one of the numbers above." + RESET)


def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def shorten(text, length=48):
    text = str(text or "Unknown")
    return text if len(text) <= length else text[:length - 1] + "…"


# ─────────────────────────────────────────────────────────────
# API + DATA
# ─────────────────────────────────────────────────────────────

def fetch_books(topic, limit=100):
    params = {
        "q": topic,
        "limit": limit,
        "fields": "key,title,author_name,first_publish_year,edition_count"
    }

    print(f"\n{BLUE}Searching Open Library for {BOLD}{topic}{RESET}{BLUE}...{RESET}")

    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        print(RED + BOLD + "\nCould not reach Open Library." + RESET)
        print(DIM + str(error) + RESET)
        return None, []
    except ValueError:
        print(RED + "Open Library returned data that could not be read." + RESET)
        return None, []

    books = []
    for item in data.get("docs", []):
        authors = item.get("author_name") or []
        books.append({
            "title": item.get("title") or "Unknown title",
            "authors": ", ".join(authors) if authors else "Unknown author",
            "first_publish_year": item.get("first_publish_year"),
            "edition_count": item.get("edition_count", 0)
        })

    return data, books


def save_csv(books, topic):
    safe_topic = re.sub(r"[^A-Za-z0-9_-]+", "_", topic.strip()).strip("_") or "books"
    filename = f"{safe_topic.lower()}_books.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        fields = ["title", "authors", "first_publish_year", "edition_count"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(books)

    return os.path.abspath(filename)


# ─────────────────────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────────────────────

def show_summary(topic, data, books):
    title("BOOK NINJA", "Open Library • Data Explorer")
    print(f"{BOLD}SEARCH{RESET}     {MAGENTA}{topic}{RESET}")
    print(f"{BOLD}MATCHES{RESET}    {GREEN}{data.get('numFound', 0):,}{RESET}")
    print(f"{BOLD}LOADED{RESET}     {GREEN}{len(books):,}{RESET} books")

    years = [safe_int(b["first_publish_year"]) for b in books]
    years = [y for y in years if y is not None]

    if years:
        print(f"{BOLD}YEAR RANGE{RESET}  {min(years)} → {max(years)}")

    editions = [safe_int(b["edition_count"]) or 0 for b in books]
    if editions:
        print(f"{BOLD}EDITIONS{RESET}    {sum(editions):,} across loaded results")

    heading("QUICK PREVIEW")
    for i, book in enumerate(books[:5], 1):
        year = book["first_publish_year"] or "?"
        print(f"{DIM}{i:>2}.{RESET} {BOLD}{shorten(book['title'], 43)}{RESET}  {DIM}({year}){RESET}")


def browse_books(books):
    title("BROWSE BOOKS", f"{len(books)} loaded results")
    page_size = 10
    page = 0
    max_page = max(0, (len(books) - 1) // page_size)

    while True:
        clear()
        print(CYAN + BOLD + f"BOOKS  •  PAGE {page + 1}/{max_page + 1}" + RESET)
        line()

        start = page * page_size
        current = books[start:start + page_size]

        for index, book in enumerate(current, start + 1):
            year = book["first_publish_year"] or "?"
            print(f"\n{CYAN}{BOLD}{index:>3}{RESET}  {BOLD}{shorten(book['title'], 52)}{RESET}")
            print(f"     {DIM}{shorten(book['authors'], 43)} • {year} • {book['edition_count']} editions{RESET}")

        print()
        line()
        print(DIM + "N = next   P = previous   number = details   Q = back" + RESET)
        action = input(CYAN + BOLD + "> " + RESET).strip().lower()

        if action == "q":
            return
        if action == "n" and page < max_page:
            page += 1
        elif action == "p" and page > 0:
            page -= 1
        elif action.isdigit():
            number = int(action)
            if 1 <= number <= len(books):
                show_book(books[number - 1], number)


def show_book(book, number):
    title(f"BOOK #{number}")
    print(BOLD + shorten(book["title"], 65) + RESET)
    print()
    print(f"{BOLD}Author(s):{RESET}       {book['authors']}")
    print(f"{BOLD}First published:{RESET} {book['first_publish_year'] or 'Unknown'}")
    print(f"{BOLD}Editions:{RESET}        {book['edition_count']}")
    pause()


# ─────────────────────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────────────────────

def publication_analysis(books):
    title("PUBLICATION TIMELINE", "When were these books first published?")
    years = [safe_int(b["first_publish_year"]) for b in books]
    years = [y for y in years if y is not None]

    if not years:
        print(YELLOW + "No publication-year data was found." + RESET)
        pause()
        return

    decades = Counter((year // 10) * 10 for year in years)
    most_common = decades.most_common(1)[0]

    print(f"{BOLD}Oldest:{RESET} {min(years)}")
    print(f"{BOLD}Newest:{RESET} {max(years)}")
    print(f"{BOLD}Most common decade:{RESET} {GREEN}{most_common[0]}s{RESET} ({most_common[1]} books)")
    heading("BOOKS BY DECADE")

    maximum = max(decades.values())
    for decade in sorted(decades):
        count = decades[decade]
        bars = "█" * max(1, round((count / maximum) * 28))
        print(f"{decade}s  {CYAN}{bars}{RESET} {count}")

    pause()


def title_length_analysis(books):
    title("TITLE LENGTH", "Are newer books given longer titles?")
    pairs = []

    for book in books:
        year = safe_int(book["first_publish_year"])
        if year is not None:
            words = len(re.findall(r"\b[\w'-]+\b", book["title"]))
            pairs.append((year, words, book["title"]))

    if not pairs:
        print(YELLOW + "Not enough year data to analyse." + RESET)
        pause()
        return

    old = [words for year, words, _ in pairs if year < 2000]
    new = [words for year, words, _ in pairs if year >= 2000]

    all_lengths = [words for _, words, _ in pairs]
    longest = max(pairs, key=lambda x: x[1])

    print(f"{BOLD}Average title:{RESET} {mean(all_lengths):.1f} words")
    if old:
        print(f"{BOLD}Before 2000:{RESET}  {mean(old):.1f} words")
    if new:
        print(f"{BOLD}2000 onward:{RESET} {mean(new):.1f} words")

    print(f"\n{BOLD}Longest loaded title:{RESET}")
    print(f"{MAGENTA}{longest[2]}{RESET}")
    print(DIM + f"{longest[1]} words • first published {longest[0]}" + RESET)

    if old and new:
        difference = mean(new) - mean(old)
        if abs(difference) < 0.5:
            verdict = "Titles are roughly the same length."
        elif difference > 0:
            verdict = "In this sample, newer titles are longer."
        else:
            verdict = "In this sample, older titles are longer."
        heading("QUICK VERDICT")
        print(verdict)
        print(DIM + "This only describes the loaded sample — it does not prove a general trend." + RESET)

    pause()


def word_analysis(books, topic):
    title("WORD LAB", "Which words appear most often in the titles?")
    topic_words = set(re.findall(r"[a-z0-9']+", topic.lower()))
    words = []

    for book in books:
        found = re.findall(r"[a-z0-9']+", book["title"].lower())
        words.extend(
            word for word in found
            if len(word) > 2 and word not in STOP_WORDS and word not in topic_words
        )

    counts = Counter(words)

    if not counts:
        print(YELLOW + "Not enough title words to analyse." + RESET)
        pause()
        return

    maximum = counts.most_common(1)[0][1]
    for rank, (word, count) in enumerate(counts.most_common(15), 1):
        bars = "█" * max(1, round((count / maximum) * 24))
        print(f"{rank:>2}. {BOLD}{word:<16}{RESET} {CYAN}{bars}{RESET} {count}")

    pause()


def edition_analysis(books):
    title("EDITION LEADERBOARD", "Which loaded books have the most editions?")
    ranked = sorted(books, key=lambda b: safe_int(b["edition_count"]) or 0, reverse=True)[:10]

    for i, book in enumerate(ranked, 1):
        print(f"\n{CYAN}{BOLD}{i:>2}.{RESET} {BOLD}{shorten(book['title'], 49)}{RESET}")
        print(f"    {GREEN}{book['edition_count']} editions{RESET} {DIM}• {shorten(book['authors'], 34)}{RESET}")

    print(DIM + "\nMore editions does not automatically mean a book is more popular." + RESET)
    pause()


def compare_topics():
    title("COMPARE TWO TOPICS", "Build two datasets and compare them")
    first = prompt("First topic", "dragons")
    second = prompt("Second topic", "robots")
    raw_limit = prompt("Books per topic", "100")

    try:
        limit = max(10, min(500, int(raw_limit)))
    except ValueError:
        limit = 100

    data_a, books_a = fetch_books(first, limit)
    data_b, books_b = fetch_books(second, limit)

    if not data_a or not data_b:
        pause()
        return

    def stats(books):
        years = [safe_int(b["first_publish_year"]) for b in books]
        years = [y for y in years if y is not None]
        lengths = [len(re.findall(r"\b[\w'-]+\b", b["title"])) for b in books]
        editions = [safe_int(b["edition_count"]) or 0 for b in books]
        return {
            "avg_year": mean(years) if years else None,
            "avg_title": mean(lengths) if lengths else 0,
            "avg_editions": mean(editions) if editions else 0
        }

    a = stats(books_a)
    b = stats(books_b)

    title("HEAD-TO-HEAD", f"{first.upper()}  VS  {second.upper()}")
    print(f"{'':20}{BOLD}{first[:18]:>18}{second[:18]:>18}{RESET}")
    line()
    print(f"{'API matches':20}{data_a.get('numFound', 0):>18,}{data_b.get('numFound', 0):>18,}")
    print(f"{'Avg. title words':20}{a['avg_title']:>18.1f}{b['avg_title']:>18.1f}")
    print(f"{'Avg. editions':20}{a['avg_editions']:>18.1f}{b['avg_editions']:>18.1f}")

    if a["avg_year"] and b["avg_year"]:
        print(f"{'Avg. first year':20}{a['avg_year']:>18.0f}{b['avg_year']:>18.0f}")

    heading("REMEMBER")
    print("Search results can be messy. A match does not guarantee that every")
    print("book is mainly about that topic, so treat comparisons as clues.")
    pause()


# ─────────────────────────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────────────────────────

def new_investigation():
    title("NEW INVESTIGATION", "Start with something you are curious about")
    topic = prompt("Search topic", "dragons")
    raw_limit = prompt("How many books should I load? 20–500", "100")

    try:
        limit = max(20, min(500, int(raw_limit)))
    except ValueError:
        limit = 100

    data, books = fetch_books(topic, limit)

    if data is None or not books:
        print(YELLOW + "\nNo usable books were returned. Try another search." + RESET)
        pause()
        return

    while True:
        show_summary(topic, data, books)
        option = choose([
            "Browse loaded books",
            "Publication timeline",
            "Title length analysis",
            "Most common title words",
            "Edition leaderboard",
            "Save clean dataset as CSV",
            "Search a different topic",
            "Back to home"
        ])

        if option == 1:
            browse_books(books)
        elif option == 2:
            publication_analysis(books)
        elif option == 3:
            title_length_analysis(books)
        elif option == 4:
            word_analysis(books, topic)
        elif option == 5:
            edition_analysis(books)
        elif option == 6:
            path = save_csv(books, topic)
            title("DATASET SAVED")
            print(GREEN + BOLD + "✓ CSV created successfully" + RESET)
            print("\n" + path)
            print(DIM + "\nFields: title, authors, first_publish_year, edition_count" + RESET)
            pause()
        elif option == 7:
            return new_investigation()
        else:
            return


def about():
    title("HOW IT WORKS")
    print(f"{BOLD}1.{RESET} You choose a topic.")
    print(f"{BOLD}2.{RESET} Python sends a request to the Open Library API.")
    print(f"{BOLD}3.{RESET} Open Library returns JSON data.")
    print(f"{BOLD}4.{RESET} Book Ninja cleans the useful fields.")
    print(f"{BOLD}5.{RESET} You can explore, analyse, compare, and export the data.")
    heading("DATA WARNING")
    print("Real data is messy. Missing authors or years are normal, and a search")
    print("match does not necessarily mean the entire book is about your topic.")
    pause()


def main():
    while True:
        title("BOOK NINJA", "A bold Python 3 Open Library data investigation")
        print(f"{BOLD}SEARCH • EXPLORE • ANALYSE • EXPORT{RESET}")
        print(DIM + "No API key required." + RESET)

        option = choose([
            "Start a new investigation",
            "Compare two topics",
            "How this project works",
            "Exit"
        ])

        if option == 1:
            new_investigation()
        elif option == 2:
            compare_topics()
        elif option == 3:
            about()
        else:
            clear()
            print(CYAN + BOLD + "\nBOOK NINJA" + RESET)
            print("Investigation complete. See you next time.\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + DIM + "Exited safely." + RESET)
        sys.exit(0)
