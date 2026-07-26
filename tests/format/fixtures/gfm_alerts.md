2023 Syntax
.
> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
.
> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
.

Replaces 2022 with 2023 Syntax
.
> **Note**
> This is a note

> **Warning**
> This is a warning
.
> [!NOTE]
> This is a note

> [!WARNING]
> This is a warning
.

Fixes formatting issues introduced without this extension
.
# Section A

- List A
  - List Nested

> **Note**: This is a note

>  \[!Note\] Useful information that users should know, even when skimming content.

> \[!cAUtIOn\]
> Advises about risks or negative outcomes of certain actions.
>
> ```py
> import antigravity
> ```
>
> - A quoted list
.
# Section A

- List A
  - List Nested

> [!NOTE]
> This is a note

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
>
> ```py
> import antigravity
> ```
>
> - A quoted list
.

Don't crash on incomplete alert (https://github.com/KyleKing/mdformat-obsidian/issues/5)
.
> **NOTE**
.
> [!NOTE]
.

Preserves an inline custom title on the canonical `[!TYPE]` form (Hugo/Obsidian extension)
.
> [!TIP] **When to use it:**
>
> - One bullet.
> - Another bullet.

> [!NOTE] Inline title with a colon:
>
> Body paragraph.

> [!WARNING] Plain inline text
>
> Body paragraph.
.
> [!TIP] **When to use it:**
> - One bullet.
> - Another bullet.

> [!NOTE] Inline title with a colon:
> Body paragraph.

> [!WARNING] Plain inline text
> Body paragraph.
.

Inline title with no body is emitted on the marker line
.
> [!TIP] **Standalone title:**
.
> [!TIP] **Standalone title:**
.

Inline title roundtrips through whitespace variations
.
> [!TIP]   **Spaced title:**
> Body.
.
> [!TIP] **Spaced title:**
> Body.
.

Alternate `**Note**` syntax still normalizes inline text into the body
.
> **Note**: A note line.

> **Warning**: A warning line.
.
> [!NOTE]
> A note line.

> [!WARNING]
> A warning line.
.

Escaped brackets still normalize inline text into the body
.
> \[!NOTE\] Useful information that users should know.
.
> [!NOTE]
> Useful information that users should know.
.
