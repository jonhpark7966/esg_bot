from dotenv import load_dotenv
import os
import pandas as pd

from esg_bot.utils import encode_image, image_summarize, extract_images_from_pdf, text_to_embeddings

# Load .env file
load_dotenv()


def process_sr_report(sr_report_path, sr_report_image_path, sr_report_corpus_vector_path, model="o1"):
    # Call the function
    extract_images_from_pdf(sr_report_path, sr_report_image_path)

    prompt = ""
    with open("./data/prompts/page_to_summary.txt", "rb") as prompt_file:
        # read file to string
        prompt = prompt_file.read().decode("utf-8")

    columns = ["page_number", "text", "vector"]

    # make df
    df = pd.DataFrame(columns=columns)

    # get file list in sr_report_image_path
    files = os.listdir(sr_report_image_path)
    for file in files:
        try:
            # if file is jpg file
            if not file.endswith(".jpg"):
                continue
            # get text from image
            text = image_summarize(encode_image(sr_report_image_path + "/" + file), prompt, model=model)
            # get vector from text
            vector = text_to_embeddings(text)
            # get page number from file name
            page_num = int(file.split("_")[1].split(".")[0])

            # append to df
            new_row = pd.DataFrame([[page_num, text, vector]], columns=columns)
            df = pd.concat([df, new_row], ignore_index=True)

            print("file" + file + "processed")

        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # save df to csv
    os.makedirs(sr_report_corpus_vector_path, exist_ok=True)
    df.to_csv(sr_report_corpus_vector_path + "corpus_vector_sr.csv", index=False)



if __name__ == "__main__":
    SR_REPORT_PATH = "../data/reports/hmc-sr-kor-2024.pdf"
    SR_REPORT_IMAGE_PATH = "./pages"
    SR_REPORT_CORPUS_VECTOR_PATH = "./"
    MODEL = "o1"

    # Load .env file
    load_dotenv()

    process_sr_report(SR_REPORT_PATH, SR_REPORT_IMAGE_PATH, SR_REPORT_CORPUS_VECTOR_PATH, MODEL)