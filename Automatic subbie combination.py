import os
import pysrt
import sys
import logging

def load_subtitles(file_path):
    try:
        return pysrt.open(file_path)
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {e}")
        sys.exit(1)

def find_matching_subtitle(en_sub, ko_subs):
    return next((ko_sub for ko_sub in ko_subs if ko_sub.start == en_sub.start and ko_sub.end == en_sub.end), None)

def combine_subtitles(en_subs, ko_subs):
    combined_subs = pysrt.SubRipFile()
    for en_sub in en_subs:
        ko_sub = find_matching_subtitle(en_sub, ko_subs)
        combined_text = en_sub.text + '\n' + ko_sub.text if ko_sub else en_sub.text
        combined_sub = pysrt.SubRipItem(
            index=en_sub.index,
            text=combined_text,
            start=en_sub.start,
            end=en_sub.end
        )
        combined_subs.append(combined_sub)
    return combined_subs

def main():
    logging.basicConfig(level=logging.INFO)

    en_file_path = input("Enter English subtitle file path: ")
    en_file_path = en_file_path.replace('\\ ', ' ').strip()
    ko_file_path = input("Enter Korean subtitle file path: ")
    ko_file_path = ko_file_path.replace('\\ ', ' ').strip()

    # Automatically generate the output file path
    base, ext = os.path.splitext(en_file_path)
    output_file_path = f"{base}_combined{ext}"

    en_subs = load_subtitles(en_file_path)
    ko_subs = load_subtitles(ko_file_path)

    combined_subs = combine_subtitles(en_subs, ko_subs)
    combined_subs.save(output_file_path)
    logging.info(f"Combined subtitles saved to {output_file_path}")

if __name__ == "__main__":
    main()
