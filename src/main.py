import argparse

from pdf_generator import pdf_generator

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str,
                    help="name of the txt file to convert, sitting inside of source")
parser.add_argument("--target", type=str,
                    help="name of the exported pdf file; is placed in target")
args = parser.parse_args()

if __name__ == '__main__':
    source_name = args.source
    target_name = args.target
    input_path = '../source/' + source_name
    output_path = '../target/' + target_name
    pdf_generator(input_path, output_path)
