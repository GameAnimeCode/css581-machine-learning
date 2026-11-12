-- Make the whole cross-reference clickable in PDF output.
-- Quarto emits "Figure", a non-breaking space, then a bare \ref{fig-x}, and
-- hyperref links only the number. This merges the three pieces into
-- \hyperref[fig-x]{Figure~\ref*{fig-x}}, so the link covers the object name too
-- ("Figure 5", "Table 2", ...).
-- Add it after Quarto's own filters in the document header:
--   filters:
--     - quarto
--     - ../../filters/crossref-link.lua

local NBSP = "\u{00A0}"

if FORMAT:match("latex") then
  function Inlines(inlines)
    local out = pandoc.Inlines({})
    local changed = false
    for _, el in ipairs(inlines) do
      local label = el.t == "RawInline" and el.format == "latex"
        and el.text:match("^\\ref{([^}]+)}$")
      local n = #out
      if label and n >= 2 and out[n].t == "Str" and out[n].text == NBSP
          and out[n - 1].t == "Str" and out[n - 1].text:match("^%a+$") then
        local name = out[n - 1].text
        out:remove(n)
        out:remove(n - 1)
        out:insert(pandoc.RawInline("latex",
          "\\hyperref[" .. label .. "]{" .. name .. "~\\ref*{" .. label .. "}}"))
        changed = true
      else
        out:insert(el)
      end
    end
    if changed then return out end
  end
end
