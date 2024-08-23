#!/usr/bin/env python3
# source: https://github.com/astutejoe/tesseract_tutorial
# creates a text, image(tif) and box file for each line in a text file.
# output to be used as a ground truth for training tesseract

from datetime import datetime
import pathlib
import random
import re
import subprocess


OVERWRITE_FILES: "bool" = True
training_text_file = "amh-layer.training_txt"

output_directory = "./amh-layer-ground-truth"

output_dir_path = pathlib.Path(output_directory)


def setup_output_dir(OVERWRITE: bool, output_dir_path: pathlib.Path):
    """If output dir doesn't exist creates one. If it exists and has files
    in it, depending on `OVERWRITE`, either its contents are moved to
    backup dir, or will be overwritten after prompting for confirmation"""
    # if output dir doesn't exist create it
    if not output_dir_path.is_dir():
        output_dir_path.mkdir()
    else:
        # if dir has files in it
        if list(output_dir_path.glob("*.txt")):

            # move to a bak folder with time stamp
            if not OVERWRITE:
                # set backup dir name
                t = datetime.now().strftime("%b-%d-%H_%M_%S")
                move_to = output_dir_path.with_name(f"bak-{output_dir_path.name}-{t}")

                # rename to backup dir and create output dir
                output_dir_path.replace(move_to)
                output_dir_path.mkdir()
                print(f'Moved old files to: "{move_to}"')

            else:
                # confirm overwrite
                resp = input(f'OVERWRITE files in"{output_dir_path}"\nYes(Y) | No(N): ')
                if not resp.lower() in ["yes", "y"]:
                    exit(1)
                print(f'Overwriting files in "{output_dir_path}"')


setup_output_dir(OVERWRITE_FILES, output_dir_path)

lines: "list[str]" = []
with open(training_text_file, "r") as input_file:
    for line in input_file:
        lines.append(line.strip())

# set random seed and shuffle lines
rand = random.Random(23)
rand.shuffle(lines)

# list of fonts to use (must be found in --fonts_dir param of text2image)
# to install fonts: copy to `/usr/share/fonts` and `fc-cache -fv`
# to list all available fonts: `fc-list :[lang=am] family style | sort`
fonts = [
    # from okfonts of lstmdata/amh (except droid sans)
    "Abyssinica SIL",
    "FreeSerif",
    "Noto Sans Ethiopic",
    "Noto Sans Ethiopic Bold",
    # from washera fonts
    "Ethiopia Jiret",
    "Ethiopic WashRa Bold, Bold",  # very similar to Abyssinica SIL
    "Ethiopic WashRa SemiBold, Bold",  # v similar to WasheRa Bold, but compacter
    "Ethiopic Wookianos",  # skip 1268 ቨ - 126F ቯ
    "Ethiopic Fantuwua",  # confusing አ - ኦ
    # # from legally-free-geez-fonts-v1_0_0
    "A0 Addis Abeba Unicode",  # similar to Noto Sans but wider
]

# no of lines to process from txt file (comment out for all)
# count = 3
# lines = lines[:count]


# map of each font to its font name, with space replaced with `_` and
# some extraneous words removed or abrreviated to shorten file names
font_name_dict = {
    font: re.sub(r"\,.+| ?Ethiopi(c|a) ?| Abeba Unicode|A0 ", "", font)
    .replace(" ", "_")
    .replace("Bold", "B")
    .replace("SemiBold", "SB")
    .replace("Abyssinica", "Abys")
    for font in fonts
}


def parse_txt2img_log(line_no, font_name, output_base, result, is_beginning):
    """Parses text2image logs and writes normal output, skipped lines,
    stripped words and Exception errors to log files."""

    # truncate files and add time header if its beginning
    if is_beginning:
        t = datetime.now().strftime("%b-%d-%H_%M_%S")
        for f in {"split_out", "skipped_err", "stripped_err", "split_err"}:
            with open(f"./log/{f}", "w") as log_file:
                log_file.write(f"------- {t} -------\n")

    # normal output
    if result.stderr:
        with open("./log/split_out", "a") as splt_out:
            splt_out.write(result.stderr)

    # skipped lines (mostly due to small image height or width)
    if f"{output_base}.tif" not in result.stderr:
        with open("./log/skipped_err", "a") as err_file:
            err_file.write(f"File: {output_base}\nErr: {result.stderr}\n")

    # stripped words due to font error
    if "Stripped" in result.stderr:
        with open("./log/stripped_err", "a") as err_file:
            err_file.write(f"File: {output_base}\nErr: {result.stderr}\n")

    # exceptions
    if result.returncode != 0:
        with open("./log/split_err", "a") as err_file:
            err_file.writelines(
                [
                    f"Line: {line_no},  Font: {font_name}\n",
                    f"Stderr: {result.stderr}\n",
                ]
            )
        exit(1)


def skip_line_for_font(line: str, font: str) -> "bool":
    """Returns true if line containes chars not properly rendered by font."""

    # letters ቨ - ቯ
    if any(
        [
            f in font
            for f in {"Fantuwua", "Jiret", "Tint", "WashRa SemiBold", "Wookianos"}
        ]
    ) and re.search(r"[\u1268-\u1268]", line):
        return True

    # letter ጷ
    if any([f in font for f in {"Fantuwua", "Tint", "Wookianos"}]) and re.search(
        r"[\u1268-\u1268]", line
    ):
        return True
    return False


# shuffle fonts to randomize font order
rand.shuffle(fonts)
# start line count from 1 for convinience
line_count = 1

# loop over lines and fonts
for line in lines:
    for font in fonts:
        # skip line if it contains chars unsuitable for font
        if skip_line_for_font(line, font):
            continue

        # remove space and comma from font name & replace with `_`
        font_name = font_name_dict[font]

        # output files (box, text & image) base path for each line & font
        output_base = output_dir_path.joinpath(f"{line_count}_{font_name}")

        # write line to txt file
        line_text = output_base.with_suffix(".gt.txt")
        with open(line_text, "w") as output_file:
            output_file.writelines([line])

        result = subprocess.run(
            # subprocess.run(
            [
                "text2image",
                f"--font={font}",
                "--fonts_dir=../fonts",
                f"--text={line_text}",
                f"--outputbase={output_base}",
                "--max_pages=1",
                "--strip_unrenderable_words",
                "--leading=0",  # Inter-line space (in pixels) default:12
                "--margin=10",
                "--xsize=1800",  # change xsize & ysize based on line length
                "--ysize=120",  # +  to minimize margin spaces around text
                "--unicharset_file=unicharset_files/Ethiopic.unicharset",
                "--exposure=-1",
            ],
            encoding="utf8",  # to force str format for result attributes
            capture_output=True,  # to capture stdout & stderr
        )

        # parse subprocess result logs & write to log files
        is_begining = line_count == 1 and font == fonts[0]
        parse_txt2img_log(line_count, font_name, output_base, result, is_begining)

    line_count += 1


"""
Font info & problems:
# from washera fonts
'Ethiopic Wookianos', 'Ethiopic Hiwua' and 'Ethiopic Tint':
    dont render ቬ (poor ቨ - ቯ), ጷ, ፗ
"Ethiopic Fantuwua",    # confusing አ - ኦ, dont render ጷ
"Ethiopic Tint",    # confusing for ltrs like ሐ፣ መ፣ ጠ፣ ሠ
"Ethiopic Hiwua",   # unusual representaion of freq. letters like እ
"Ethiopic WashRa Bold, Bold", # very similar to Abyssinica SIL
"Ethiopic WashRa SemiBold, Bold", # v similar to WasheRa Bold, but compacter

# from legally-free-geez-fonts-v1_0_0
"ahabesha'stypewriter", # geez no.s, brackets
'Chiret',               # geez no.s, brackets
'Geez Handwriting', 'Geez Handwriting Bold',    # geez no.s
'Shiromeda',    # dont render chars like `<<`, v. similar to Noto Sans Ethiopic
"A0 Addis Abeba Unicode",   # similar to Noto Sans but wider

"""
"""
text2image args:
# "--distort_image=true", # noise, blur, invert # def: false
# "--invert=false",    # def: true

# "--smooth_noise=false", # no effect when --distort_image=false, but useful when true
"""
