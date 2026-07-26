2023 Syntax
.
> [!NOTE]
> Useful information that users should know, even when skimming content.
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Note</p>
<p>Useful information that users should know, even when skimming content.</p>
</div>
.

Replaces 2022 with 2023 Syntax
.
> **Warning**
> This is a warning
.
<div class="markdown-alert markdown-alert-warning">
<p class="markdown-alert-title">Warning</p>
<p>This is a warning</p>
</div>
.

Test inline syntax
.
> \[!Note\] This is an inline "Note"
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Note</p>
<p>This is an inline &quot;Note&quot;</p>
</div>
.

Strict GFM (default) folds trailing text on the canonical `[!TYPE]` line into the body instead of treating it as a title
.
> [!TIP] **When to use it:**
>
> Body paragraph.
.
<div class="markdown-alert markdown-alert-tip">
<p class="markdown-alert-title">Tip</p>
<p><strong>When to use it:</strong></p>
<p>Body paragraph.</p>
</div>
.

Strict GFM (default) folds a title-only marker line into the alert body
.
> [!NOTE] Custom title:
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Note</p>
<p>Custom title:</p>
</div>
.
