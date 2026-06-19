import webbrowser

class WebSearch:
    def web_search(query):
        webbrowser.open(f"https://www.bing.com/search?q={query}")

    def open_browser():
        webbrowser.open(" ")

    def open_youtube():
        webbrowser.open("https://www.youtube.com")

    def search_youtube(query):
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")