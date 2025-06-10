# markdown-typst

A Python Markdown extension that compiles `typst` fenced code blocks into inline SVG images.

## Features

- Detects fenced code blocks labeled as `typst` with `typst-preview` in the first line.
- Compiles the Typst code into SVG format using the `typst` compiler.

## Installation

```bash
pip install markdown-typst
```

## Usage

````python
import markdown
import markdown_typst

md = markdown.Markdown(extensions=["markdown_typst.typst_extension"])
input_text = '''
```typst
// typst-preview
# Your Typst code here
```

'''

html = md.convert(input_text)
print(html)

````

## Requirements

* `markdown`
* `typst`

## License

MIT License
