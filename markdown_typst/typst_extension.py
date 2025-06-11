from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from textwrap import dedent
import typst
import uuid
import os
import re
import traceback


def minify_xml(svg_str):
    s = re.sub(r">\s+<", "><", svg_str)
    s = s.strip()
    return s

class TypstPreprocessor(Preprocessor):
    # Regular expression to match fenced code blocks from fenced_code extension.
    FENCED_BLOCK_RE = re.compile(
        dedent(r'''
            (?P<indent>^[ \t]*)
            (?P<fence>(?:~{3,}|`{3,}))[ ]*                           # opening fence
            ((\{(?P<attrs>[^\n]*)\})|                                # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=indent)(?P=fence)[ ]*$                               # closing fence
        '''),
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    def run(self, lines):
        text = "\n".join(lines)
        new_text = ""
        pos = 0
        for match in self.FENCED_BLOCK_RE.finditer(text):
            start, end = match.span()
            indent = match.group("indent")
            code = match.group("code")
            lang = match.group("lang") or ""
            attrs = match.group("attrs") or ""
            # Append text before this block
            new_text += text[pos:start]
            # Process typst code blocks with preview
            if lang.strip() == "typst" and "typst-preview" in code.splitlines()[0]:
                filename = f"markdown-typst-{uuid.uuid4()}.typ"
                with open(filename, "w") as f:
                    f.write(code)
                try:
                    svg_bytes = typst.compile(filename, format="svg")
                    if isinstance(svg_bytes, bytes):
                        svg_str = svg_bytes.decode("utf-8")
                        svg_str = minify_xml(svg_str)
                    elif isinstance(svg_bytes, list):
                        if "column" in code.splitlines()[0]:
                            svg_str = "<br>".join(minify_xml(svg_bytes_item.decode("utf-8"))
                                for svg_bytes_item in svg_bytes
                            )
                        else:
                            svg_str = "".join(minify_xml(svg_bytes_item.decode("utf-8"))
                                for svg_bytes_item in svg_bytes
                            )
                    else:
                        raise ValueError("Unexpected type from typst.compile")

                    style = ''
                    if "center" in code.splitlines()[0]:
                        style += "text-align: center;"
                    if style:
                        svg_str = indent + f'<div style="{style}">{svg_str}</div>'
                    else:
                        svg_str = indent + svg_str
                except Exception as e:
                    if "debug" in code.splitlines()[0]:
                        svg_str = indent + "!!! failure \"Error processing Typst code\"\n" \
                                         + (indent + "    ```" + "\n" + indent + "    ") \
                                         + ("\n" + indent + "    ").join(traceback.format_exc().splitlines()) + "\n" \
                                         + (indent + "    ```")
                    else:
                        svg_str = indent + "!!! failure \"Error processing Typst code\"\n" \
                                         + (indent + "    Use `typst-preview debug` to show details")
                    print(svg_str)
                finally:
                    os.remove(filename)
                # Insert SVG directly
                new_text += svg_str + "\n"
            else:
                # Keep as fenced code block
                new_text += match.group(0)
            pos = end

        # Append any remaining text
        new_text += text[pos:]
        return new_text.splitlines()

class TypstExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(TypstPreprocessor(md), 'typst', 40)
