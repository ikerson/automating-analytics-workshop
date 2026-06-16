# Diagrams

Mermaid source files for diagrams used in the workshop modules. Each `.mmd` file is embedded directly in the relevant module as a fenced `mermaid` code block, which renders natively on GitHub and in the Quarto book.

## Files

| File | Used in | Description |
|---|---|---|
| `tool_relationships.mmd` | `modules/session_00.md` | Relationship between VS Code, conda, Git, GitHub, and pipeline outputs |

## Viewing

**GitHub** — Mermaid diagrams render automatically when you view any `.md` file that embeds the code block. The `.mmd` source files render as diagrams on GitHub as well.

**Quarto** — Diagrams render automatically during `quarto render`. No additional configuration required.

**Local (PNG export)** — Install the [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) and run:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagrams/tool_relationships.mmd -o diagrams/tool_relationships.png
```

## Adding a New Diagram

1. Create a `.mmd` file in this folder.
2. Add a row to the table above.
3. Embed in the relevant module with a fenced `mermaid` code block:

    ````markdown
    ```mermaid
    [paste contents of .mmd file here]
    ```
    ````
