from dadrah_sc.crawler import extract_question_links, save_links_to_file
from dadrah_sc.parser import parse_all_links

def main():
    try:
        start = 1
        end = 1

        links = extract_question_links(start, end)
        save_links_to_file(links)

        parse_all_links()

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
