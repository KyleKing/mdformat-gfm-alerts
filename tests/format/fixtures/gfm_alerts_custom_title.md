With `custom_title=True`, an inline custom title on the canonical `[!TYPE]` form round-trips (Obsidian callout convention, mirrored by Hugo's alert syntax)
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

With `custom_title=True`, an inline title with no body is emitted on the marker line
.
> [!TIP] **Standalone title:**
.
> [!TIP] **Standalone title:**
.

With `custom_title=True`, an inline title round-trips through whitespace variations
.
> [!TIP]   **Spaced title:**
> Body.
.
> [!TIP] **Spaced title:**
> Body.
.

With `custom_title=True`, alternate `**Note**` syntax still normalizes into the body (only the canonical unescaped `[!TYPE]` form carries a title)
.
> **Note**: A note line.
.
> [!NOTE]
> A note line.
.

With `custom_title=True`, escaped brackets still normalize inline text into the body
.
> \[!NOTE\] Useful information that users should know.
.
> [!NOTE]
> Useful information that users should know.
.
