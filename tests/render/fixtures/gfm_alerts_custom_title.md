With `custom_title=True`, canonical unescaped `[!TYPE]` with an inline custom title renders the title in place of the type name
.
> [!TIP] **When to use it:**
>
> Body paragraph.
.
<div class="markdown-alert markdown-alert-tip">
<p class="markdown-alert-title"><strong>When to use it:</strong></p>
<p>Body paragraph.</p>
</div>
.

With `custom_title=True`, an inline title without a body still renders
.
> [!NOTE] Custom title:
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Custom title:</p>
</div>
.

With `custom_title=True`, escaped brackets still fall back to the type name (only the canonical unescaped form carries a title)
.
> \[!Note\] This is an inline "Note"
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Note</p>
<p>This is an inline &quot;Note&quot;</p>
</div>
.
