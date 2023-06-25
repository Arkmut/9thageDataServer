import logging
import os
import subprocess
import tempfile
from subprocess import PIPE

from ..models import format_template, LatexTemplate, generate_filename

logger_latex = logging.getLogger(__name__)


def latex_topdf_from_string(latex: str):
    logger_latex.info("latex: " + latex)
    pdf = ""
    log = ""
    with tempfile.TemporaryDirectory() as td:
        f = open(td + "/file.tex", 'w')
        f.write(latex)
        f.close()
        fp = subprocess.run(
            ["lualatex", "--interaction=batchmode", "-output-directory=" + td, "-jobname=file", 'file.tex'], timeout=15,
            stdout=PIPE, stderr=PIPE)
        logger_latex.info("printing stdout...")
        for l in fp.stdout.decode("utf-8").split("\n"):
            logger_latex.info(l)
        logger_latex.info("printing stderr...")
        for l in fp.stderr.decode("utf-8").split("\n"):
            logger_latex.info(l)
        logger_latex.info("printing logs...")
        with open(os.path.join(td, 'file.log'), 'rb') as f:
            log = f.read()
            for l in log.decode("utf-8").split("\n"):
                logger_latex.info(l)
        with open(os.path.join(td, 'file.pdf'), 'rb') as f:
            pdf = f.read()
    return pdf, log, fp


def export_armybook(name: str, language: str, army: {}, template: LatexTemplate):
    latex = template.getWithSubImports()
    formattedLatex = format_template(army, template.lastModified, "%d %B, %Y", latex,language)
    return latex_topdf_from_string(formattedLatex), generate_filename(army)
