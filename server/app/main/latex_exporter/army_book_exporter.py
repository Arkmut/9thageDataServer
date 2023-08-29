import logging
import os, re
import subprocess
import tempfile
from subprocess import PIPE
from ..models import format_template_all, format_template_all_readable, LatexTemplate, generate_filename_zip, \
    generate_filename, gen_army_name, RSC_PATH
import shutil

logger_latex = logging.getLogger(__name__)


def latex_topdf_from_string(latexes: {str: str}, army):
    zip = None
    log = ""
    with tempfile.TemporaryDirectory() as td:
        os.mkdir(td + "/res")
        directory = td + "/res"

        for language in latexes.keys():
            filename = generate_filename(army, language)
            f = open(directory + f"/{filename}.tex", 'w')
            f.write(latexes[language])
            f.close()
            fp = subprocess.run(
                ["lualatex", "-synctex=1", "-interaction=nonstopmode", "-output-directory=" + directory,
                 "-file-line-error",
                 "-recorder", f"{filename}.tex"],
                timeout=120,
                stdout=PIPE, stderr=PIPE)
            # double try for latex
            fp = subprocess.run(
                ["lualatex", "-synctex=1", "-interaction=nonstopmode", "-output-directory=" + directory,
                 "-file-line-error",
                 "-recorder", f"{filename}.tex"],
                timeout=120,
                stdout=PIPE, stderr=PIPE)
            # triple try for latex
            fp = subprocess.run(
                ["lualatex", "-synctex=1", "-interaction=nonstopmode", "-output-directory=" + directory,
                 "-file-line-error",
                 "-recorder", f"{filename}.tex"],
                timeout=120,
                stdout=PIPE, stderr=PIPE)
            logger_latex.info("printing stdout...")
            for l in fp.stdout.decode("utf-8").split("\n"):
                logger_latex.info(l)
            logger_latex.info("printing stderr...")
            for l in fp.stderr.decode("utf-8").split("\n"):
                logger_latex.info(l)

        for f in os.listdir(directory):
            if not re.search(r".*\.pdf$", f):
                os.remove(os.path.join(directory, f))
        archive = shutil.make_archive(os.path.join(td, 'file'), 'zip', directory)
        with open(archive, 'rb') as f:
            zip = f.read()
    return zip


def parse_and_zip_latex(latexes: {str: {str: [tuple[str, str, str]]}}, army):
    zip = None
    with tempfile.TemporaryDirectory() as td:
        os.mkdir(td + "/res")
        directory = td + "/res"
        logger_latex.info(f"files: {latexes}")
        for language in latexes.keys():
            for folder, files in latexes[language].items():
                if "/" in folder:
                    total = ""
                    for subfolder in folder.split("/"):
                        total+=subfolder+"/"
                        if not os.path.exists(directory + f"/{total}"):
                            os.mkdir(directory + f"/{total}")
                else:
                    if not os.path.exists(directory + f"/{folder}/"):
                        os.mkdir(directory + f"/{folder}/")
                for filename, content, extension in files:
                    f = open( f"{directory}/{folder}/{filename}.{extension}", 'w')
                    logger_latex.info(f"write: {directory}/{folder}/{filename}.{extension}")
                    f.write(content)
                    f.close()

        # copy rsc
        shutil.copytree(RSC_PATH + "/" + gen_army_name(army) + "/pics", os.path.join(directory, 'pics'))
        archive = shutil.make_archive(os.path.join(td, 'file'), 'zip', directory)
        with open(archive, 'rb') as f:
            zip = f.read()
    return zip


def export_armybook(name: str, date, gen_pdf: bool, global_language: {}, army: {}, template: LatexTemplate):
    latex = template.getWithSubImports(True)
    if gen_pdf:
        formattedLatex = format_template_all(army, date, "%B %d, %Y", latex, global_language)
        return latex_topdf_from_string(formattedLatex, army), generate_filename_zip(army)
    else:
        formattedLatex = format_template_all_readable(army, date, "%B %d, %Y", latex, global_language)
        return parse_and_zip_latex(formattedLatex, army),generate_filename_zip(army)
