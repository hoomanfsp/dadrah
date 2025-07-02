from dadrah_sc.crawler import extract_question_links, save_links_to_file
from dadrah_sc.parser import parse_all_links

def main():
    try:
        start = int(input("Start page number (about 21700 pages): "))
        end = int(input("End page number: "))

        links = extract_question_links(start, end)
        save_links_to_file(links)

        parse_all_links()

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
