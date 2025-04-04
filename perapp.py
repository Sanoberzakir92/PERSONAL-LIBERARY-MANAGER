import streamlit as st
import json

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a JSON file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save the library to a JSON file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read):
    """Add a book to the library."""
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    library.append(book)
    save_library(library)
    st.success("Book added successfully!")

def remove_book(library, title):
    """Remove a book from the library by title."""
    updated_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(updated_library) < len(library):
        save_library(updated_library)
        st.success("Book removed successfully!")
    else:
        st.error("Book not found!")
    return updated_library

def search_books(library, query, by="title"):
    """Search for books by title or author."""
    return [book for book in library if query.lower() in book[by].lower()]

def display_statistics(library):
    """Display statistics about the library."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"**Total books:** {total_books}")
    st.write(f"**Percentage read:** {read_percentage:.2f}%")

# Load library data
library = load_library()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"])

if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(library, title, author, year, genre, read)

elif menu == "Remove Book":
    st.header("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        library = remove_book(library, title)

elif menu == "Search Books":
    st.header("🔍 Search for a Book")
    search_query = st.text_input("Enter title or author")
    search_by = st.radio("Search by", ("title", "author"))
    if st.button("Search"):
        results = search_books(library, search_query, search_by)
        if results:
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.error("No matching books found.")

elif menu == "View All Books":
    st.header("📖 Your Library")
    if library:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.warning("No books in your library.")

elif menu == "Statistics":
    st.header("📊 Library Statistics")
    display_statistics(library)
