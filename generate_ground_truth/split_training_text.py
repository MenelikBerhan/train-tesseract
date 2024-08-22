#!/usr/bin/env python3
# source: https://github.com/astutejoe/tesseract_tutorial
# creates a text, image(tif) and box file for each line in a text file.
# output to be used as a ground truth for training tesseract

from datetime import datetime
import os
import pathlib
import random
import re
import subprocess

from glob import iglob

OVERWRITE_FILES: "bool" = True
training_text_file = "amh-layer.training_txt"

output_directory = "./amh-layer-ground-truth"

output_dir_path = pathlib.Path(output_directory)


def setup_output_dir(OVERWRITE_FILES, output_directory, output_dir_path):
    if not output_dir_path.is_dir():
        os.mkdir(output_directory)
    else:
        # move to backup folder
        if (
            list(iglob(output_dir_path.joinpath("*.txt").as_posix()))
            and not OVERWRITE_FILES
        ):
            t = datetime.now().strftime("%b-%d-%H_%M_%S")
            move_to = pathlib.Path(f"./bak-ground-truth-{t}")
            os.renames(output_directory, move_to)
            os.mkdir(output_directory)
            print(f'Moved old files to: "{move_to}"')
        else:
            # confirm overwrite
            overwrite = input(
                f'About To OVERWRITE files in"{output_dir_path}"\nYes(Y) | No(N): '
            )
            if not overwrite in ["Yes", "Y"]:
                exit(1)
            print(f'Overwriting files in "{output_dir_path}"')


setup_output_dir(OVERWRITE_FILES, output_directory, output_dir_path)

lines: "list[str]" = []

with open(training_text_file, "r") as input_file:
    for line in input_file:
        lines.append(line.strip())

rand = random.Random(0)
rand.shuffle(lines)

# list of fonts to use (must be found in --fonts_dir param of text2image)
# to install fonts: copy to `/usr/share/fonts` and `fc-cache -fv`
# to list all available fonts: `fc-list : family style | sort`
fonts = [
    # from okfonts of lstmdata/amh (except droid sans)
    "Abyssinica SIL",
    "FreeSerif",
    "Noto Sans Ethiopic",
    "Noto Sans Ethiopic Bold",
    # from washera fonts
    "Ethiopia Jiret",
    "Ethiopic WashRa Bold, Bold",
    "Ethiopic WashRa SemiBold, Bold",
    "Ethiopic Hiwua",  # 'Ethiopic Yebse', (very similar to Hiwua)
    "Ethiopic Wookianos",
    "Ethiopic Fantuwua",
    "Ethiopic Tint",
    # # from legally-free-geez-fonts-v1_0_0
    "Shiromeda",
    "A0 Addis Abeba Unicode",
]


# no of lines to process from txt file (comment out for all)
count = 10000
lines = lines[:count]

# input file name without extention
input_file_name = pathlib.Path(training_text_file).stem

# map of each font to its font name with space and comma replaced with `_`
font_name_dict = {
    font: re.sub(r"\,.+| ?Ethiopic ?", "", font).replace(" ", "_") for font in fonts
}

rand.shuffle(fonts)

line_count = 1


def parse_txt2img_log(line_no, font_name, output_files_base_name, result):
    if result.stdout:
        with open("./split_stdout", "a") as splt_out:
            splt_out.write(result.stdout)
    if result.stderr:
        with open("./split_stderr", "a") as splt_out:
            splt_out.write(result.stderr)

    if f"{output_files_base_name}.tif" not in result.stderr:
        with open("./skipped_err", "a") as err_file:
            err_file.write(f"File: {output_files_base_name}\nErr: {result.stderr}\n")

    if "Stripped" in result.stderr:
        with open("./stripped_err", "a") as err_file:
            err_file.write(f"File: {output_files_base_name}\nErr: {result.stderr}\n")

    if result.returncode != 0:
        with open("./split_error", "a") as err_file:
            err_file.writelines(
                [
                    f"Line: {line_no},  Font: {font_name}\n",
                    f"Stdout: {result.stdout}\n",
                    f"Stderr: {result.stderr}\n",
                ]
            )


for line in lines:
    # output files (box, text & image) line no.
    line_no = f"{line_count}"

    for font in fonts:
        # remove space and comma from font name & replace with `_`
        font_name = font_name_dict[font]

        # output files (box, text & image) base path for each line & font
        output_files_base_name = os.path.join(
            output_directory, f"{line_no}_{font_name}"
        )

        # write line to txt file
        line_training_text = f"{output_files_base_name}.gt.txt"
        with open(line_training_text, "w") as output_file:
            output_file.writelines([line])

        result = subprocess.run(
            # subprocess.run(
            [
                "text2image",
                f"--font={font}",
                "--fonts_dir=../fonts",
                f"--text={line_training_text}",
                f"--outputbase={output_files_base_name}",
                "--max_pages=1",
                "--strip_unrenderable_words",
                # "--leading=32",  # Inter-line space (in pixels) default:12
                "--xsize=2400",  # change xsize & ysize based on line length
                "--ysize=300",  # +  to minimize margin spaces around text
                "--unicharset_file=unicharset_files/Ethiopic.unicharset",
                "--distort_image=true",
                "--exposure=-1",
            ],
            encoding="utf8",  # to force str format for result attributes
            capture_output=True,  # to capture stdout & stderr
        )
        parse_txt2img_log(line_no, font_name, output_files_base_name, result)

    line_count += 1


"""
Font problems:
# from washera fonts
'Ethiopic Wookianos', 'Ethiopic Hiwua' and 'Ethiopic Tint', dont render ('ቨ - ቮ')

# from legally-free-geez-fonts-v1_0_0
"ahabesha'stypewriter", # geez no.s, brackets
'Chiret',               # geez no.s, brackets
'Geez Handwriting', 'Geez Handwriting Bold',    # geez no.s
'Shiromeda',    # similar chars like `<<`
"""
