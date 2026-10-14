## Cascaded Intent Development Script (CIDEr)

**Cascaded Intent Development Script**, or **CIDEr**, is an intentful programming DSL that enables its users to compile source code in a programming language of their choice without actually writing the desired code themselves. Instead of writing a program directly, CIDEr allows users to express its intended logic using structured and intentful pseudocode using an AI-backed compilation pipeline to translate these specifications into code in a selected target language. Note that at present **CIDEr is only a functional prototype** and technically work-in-progress (WIP). The current implementation supports Python and C as target languages, and it is not yet packaged as an installable command-line tool. All generated code should be reviewed and tested before use.

### 1. Design motivation

AI programming tools and coding agents can generate substantial amounts of code from NL descriptions. However, when a specification leaves implementation choices implicit, the generated program may make decisions that do not match the developer's intentions. CIDEr is meant to explore an alternative workflow, that is: explicitly express program logic in a light and intentful source language, then translate that representation into a conventional programming language. Rather than requiring users to specify every implementation detail, CIDEr allows statements to combine identifiable program constructs with descriptions of the operations or behaviour that is intended for them. Related statements are organized into blocks and connected by the **cascade operator (`>>`)**. While one could technically explain all intent in a single block, CIDEr does not encourage that by design. The quality and correctness of the generated code however still depends on the quality of the AI model (LLM) used. 

### 2. How CIDEr works
1. Reads a `.ci` file and identifies its statement blocks.
2. Validates the target-language directive, block structure, and basic statement formatting (linting).
3. Converts the extracted statements into a compact textual representation that preserves block identifiers/source-line ranges.
4. Forwards the compact representation to a configured language model to translate it into the selected target language.
5. Submits the generated code to a second model pass to organize, document, and optimize it.
6. Writes the resulting source code to a file with the appropriate target-language extension.

By default the backend uses Google's Gemini API. Alternatively, you may use a locally available Ollama model. Since the current implementation relies on model-generated code rather than a deterministic or language-specific translation backend, the equivalent CIDEr specifications may produce different implementations, and successful compilation would not necessary guarantee correctness.

### 3. Setup for usage/testing
**Prerequisites:** Python 3.10 or later is recommended. A Gemini API key is needed for the default backend, or a working local Ollama installation for the alternative backend.

#### Clone the repository

```bash
git clone https://github.com/0ameyasr/CIDEr.git
cd CIDEr
```

#### Install dependencies

```bash
python -m pip install pandas jinja2 rich python-dotenv google-genai ollama
```

#### Configure the Gemini backend

Create a `.env` file in the repository root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=your_available_gemini_model
OLLAMA_MODEL_NAME=your_local_ollama_model
```

Replace the placeholders with your actual API key and model names. The Gemini SDK usually uses `GEMINI_API_KEY` for authentication, while CIDEr reads the model names from the environment. Similarly, the `OLLAMA_MODEL_NAME` setting is only needed when using the Ollama backend.

#### Configure the Ollama backend (optional)

If your hardware is appropriate, install Ollama and download a model compatible with the local installation. Ensure the Ollama service is running and that the model name matches `OLLAMA_MODEL_NAME` in `.env`. Ollama will run locally, but compilation performance and output quality are dependent on the model, available compute, and memory.

### 4. Writing CIDEr scripts

CIDEr source files use the `.ci` extension.

#### 4.1. Comments and documentation

All text outside recognized CIDEr blocks is ignored by the parser; you can hence write unlimited explanatory prose, examples, and documentation.

```cider
This script demonstrates a basic CIDEr program.
The first block selects the target language, and is mandatory.

:: use : py ::
```

The `use` directive must appear in the first recognized block. The current implementation recognizes target extensions configured in `build.json`, which presently lists `py` (for Python) and `c` (for C).

#### 4.2. Blocks and statements

CIDEr uses double-colon delimiters to identify blocks. The cascade operator `>>` separates intentful statements within a block; the basic statement forms are:

**Subject-intent form**

```cider
:: total : initialize to zero ::
```

Here, `total` is the subject and `initialize to zero` describes the intended operation.

**Intent-only form**

```cider
:: initialize a running total to zero ::
```

An intent-only statement has no explicit subject, so its intended behaviour should therefore be self-descriptive and unambiguous. Both forms are supported at present. The subject, if present, is expected to identify a variable, function, or some other program entity, optionally with a type or other specifier.

#### 4.3. A small example

The following illustrates the intended source notation:

```cider
A program that reads two numbers and displays their sum.

:: use : py ::

:: a,b : input two numbers ::
:: total : compute the sum of a and b ::
:: display total ::
```

Instead of multiple single statement blocks, you may use one block with multiple cascaded intent statements.

If compiled, the above script should yield something like:
```
import sys

def main() -> None:
    """
    Reads two integers from standard input, calculates their sum,
    and outputs the total.
    """
    try:
        line = sys.stdin.readline().strip()
        if line:
            a, b = map(int, line.split()[:2])
            total = a + b
            print(total)
    except (ValueError, IndexError) as err:
        print(f"Error processing input: {err}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

#### 4.4. Cascaded statements

The cascade operator `>>` connects statements in a block:

```cider
:: a,b : input two numbers >> total : compute a + b >> display total ::
```

The operator is used to separate statements in the intermediate representation and should not be confused with a target-language operator.

### 5. Linter and source format rules

CIDEr performs a limited set of structural checks in its linting phase before invoking the AI compiler. The checks will often help catch malformed source files, but they do not constitute a complete grammar or type system.

#### 5.1. Target directive
The first recognized block must contain a valid `use` directive.

```cider
:: use : py ::
```

```cider
:: use : c ::
```

The directive must specify a target extension present in `build.json`. The linter reports errors when the directive is absent, incomplete, or uses an unsupported target.

#### 5.2. Block delimiters

Recognized blocks are delimited using `::`, empty or unclosed blocks will be rejected by the linter. 

#### 5.3. Statement formatting

The linter checks statements containing a colon using a basic subject-intent convention:

```text
subject : intent
```

It checks that the subject and intent are not empty. Intent-only forms need not use a colon, as aforementioned. At present the linter does not fully validate whether a subject is a legal identifier in the target language, whether an intent is semantically meaningful, or whether the generated code will compile.

#### 5.4. Cascading

For multiline blocks, the current linter expects each subsequent line to begin with `>>`, a line that does not follow this convention triggers an out-of-cascade error.

#### 5.5. Error reporting
The implementation provides errors and warnings for conditions including:
- Missing or invalid target directives
- Empty scripts or missing recognizable blocks
- Empty or unclosed blocks
- Malformed cascading
- Missing subjects or intents in colon-separated statements
- Compilation failures or invalid model-generated responses

### 6. Compiling a script
You can compile CIDEr source files in two ways.

#### 6.1. Compile an individual file
Create a file such as `script.ci` in the repository root, then run:

```bash
python cider.py script.ci
```

The generated source file will be written to the current working directory. 

#### 6.2. Compile a project directory

CIDEr also supports compiling `.ci` files contained in a project's `.cider` directory.

For example:

```text
dummy/
|__.cider/
|____first.ci
|____second.ci
```

Run the compiler from the repository root:

```bash
python cider.py dummy
```

When given a directory, CIDEr looks for a `.cider` subdirectory and compiles the `.ci` files found directly inside it. The generated files will be directed to the project directory. Note that the current implementation does not recursively discover arbitrary nested `.ci` files inside `.cider`. For now you may place source files directly in `.cider` for this workflow.

#### 6.3. Use the Ollama backend
To use a local Ollama model instead of Gemini:

```bash
python cider.py script.ci --ollama
```

For project-directory compilation:

```bash
python cider.py dummy --ollama
```

The model name is read from `OLLAMA_MODEL_NAME`, and the compiler is expected to print a warning about performance when using local models.

### 7. Configuration and extensibility

#### Target languages

The file `build.json` currently specifies the target extensions:

```json
{
    "targets": [
        "py",
        "c"
    ]
}
```

This configuration is used by the linter to validate the `use` directive. Listing an extension here will not by itself provide a complete target-language implementation unless the source file, intermediate representation, and underlying AI model must also support the desired language.

#### Prompt templates

The `prompts/` directory contains two Jinja templates:
- `compile.jinja` describes the expected input representation, translation rules, and JSON response format for the first compilation pass.
- `optimize.jinja` instructs the model to organize and optimize the generated code while preserving its intended behaviour.

The templates form part of the compilation mechanism and can be freely inspected or modified when experimenting with the translation process.
___
CIDEr is an exploratory prototype and is best suited to small, controlled experiments exploring intentful source representations and subsequent generation. Since the project is still WIP, bug reports, suggestions, and experiments that can help improve the project and its scope are welcome.
