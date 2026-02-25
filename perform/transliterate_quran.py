"""
Urdu -> Hindi Script Transliteration of quran_urdu_jalandhry.txt
Uses the rule-based transliteration system from urdu_to_hindi.py (ported to Python 3).
Output: quran_hindi_transliterated.txt
"""

import codecs
import os
import re

# ─────────────────────────────────────────────────────────────────────────────
# IPA → Hindi (Devanagari) dictionaries  (from urdu_to_hindi.py)
# ─────────────────────────────────────────────────────────────────────────────

ipa_hindi_dict_start = {}
ipa_hindi_dict       = {}

# ---- start-of-word vowels / signs ----
ipa_hindi_dict_start['\u0259'] = ['\u0905']   # A
ipa_hindi_dict_start['\u0061'] = ['\u0906']   # AA
ipa_hindi_dict_start['\u026A'] = ['\u0907']   # I
ipa_hindi_dict_start['\u0069'] = ['\u0908']   # II
ipa_hindi_dict_start['\u028A'] = ['\u0909']   # U
ipa_hindi_dict_start['\u0075'] = ['\u090A']   # UU
ipa_hindi_dict_start['\u0065'] = ['\u090F', '\u0945']  # E
ipa_hindi_dict_start['\u025B'] = ['\u0910']   # AI
ipa_hindi_dict_start['\u006F'] = ['\u0913']   # O
ipa_hindi_dict_start['\u0254'] = ['\u0914', '\u0913', '\u094b']  # AU
ipa_hindi_dict_start['\u0303'] = ['\u0901', '\u0902']  # candrabindu
ipa_hindi_dict_start['\u006E'] = ['\u0902']   # anusvara (noon)
ipa_hindi_dict_start['\u0266'] = ['\u0903']   # visarga

# ---- consonants (start position) ----
ipa_hindi_dict_start['\u006B']               = ['\u0915']  # KA
ipa_hindi_dict_start['\u02B0']               = ['\u0916']  # KHA
ipa_hindi_dict_start['\u0261']               = ['\u0917']  # GA
ipa_hindi_dict_start['\u0324']               = ['\u0918']  # GHA
ipa_hindi_dict_start['\u014B']               = ['\u0919']  # NGA
ipa_hindi_dict_start['\u0074\u0361\u0283']   = ['\u091A']  # CA
ipa_hindi_dict_start['\u0074\u0361\u0283\u02B0'] = ['\u091B']  # CHA
ipa_hindi_dict_start['\u0064\u0361\u0292']   = ['\u091C']  # JA
ipa_hindi_dict_start['\u0064\u0361\u0292\u0324'] = ['\u091D']  # JHA
ipa_hindi_dict_start['\u0272']               = ['\u091E']  # NYA
ipa_hindi_dict_start['\u0288']               = ['\u091F']  # TTA
ipa_hindi_dict_start['\u0288\u02B0']         = ['\u0920']  # TTHA
ipa_hindi_dict_start['\u0256']               = ['\u0921']  # DDA
ipa_hindi_dict_start['\u0256\u0324']         = ['\u0922']  # DDHA
ipa_hindi_dict_start['\u0273']               = ['\u0923']  # NNA
ipa_hindi_dict_start['\u0074\u032A']         = ['\u0924']  # TA
ipa_hindi_dict_start['\u0074\u032A\u02B0']   = ['\u0925']  # THA
ipa_hindi_dict_start['\u0064']               = ['\u0926']  # DA
ipa_hindi_dict_start['\u0064\u0324']         = ['\u0927']  # DHA
ipa_hindi_dict_start['\u0070']               = ['\u092A']  # PA
ipa_hindi_dict_start['\u0070\u02B0']         = ['\u092B']  # PHA
ipa_hindi_dict_start['\u0062']               = ['\u092C']  # BA
ipa_hindi_dict_start['\u0062\u0324']         = ['\u092D']  # BHA
ipa_hindi_dict_start['\u006D']               = ['\u092E']  # MA
ipa_hindi_dict_start['\u006A']               = ['\u092F']  # YA
ipa_hindi_dict_start['\u0072']               = ['\u0930']  # RA
ipa_hindi_dict_start['\u006C']               = ['\u0932']  # LA
ipa_hindi_dict_start['\u028B']               = ['\u0935']  # VA
ipa_hindi_dict_start['\u0283']               = ['\u0936']  # SHA
ipa_hindi_dict_start['\u0282']               = ['\u0937']  # SSA
ipa_hindi_dict_start['\u0073']               = ['\u0938']  # SA
ipa_hindi_dict_start['\u0071']               = ['\u0958']  # QA
ipa_hindi_dict_start['\u0078']               = ['\u0959']  # KHHA
ipa_hindi_dict_start['\u0263']               = ['\u095A']  # GHHA
ipa_hindi_dict_start['\u007A']               = ['\u095B']  # ZA
ipa_hindi_dict_start['\u027D']               = ['\u095C']  # DDDHA
ipa_hindi_dict_start['\u027D\u0324']         = ['\u095D']  # RHA
ipa_hindi_dict_start['\u0066']               = ['\u095E']  # FA

# ---- middle/end-of-word vowels / signs ----
ipa_hindi_dict['\u0259'] = ['\u0905']
ipa_hindi_dict['\u0061'] = ['\u0906', '\u093E']   # AA / matra aa
ipa_hindi_dict['\u026A'] = ['\u0907', '\u093F']   # I / matra i
ipa_hindi_dict['\u0069'] = ['\u0908', '\u0940']   # II / matra ii
ipa_hindi_dict['\u028A'] = ['\u0909', '\u0941']   # U / matra u
ipa_hindi_dict['\u0075'] = ['\u090A', '\u0942']   # UU / matra uu
ipa_hindi_dict['\u0065'] = ['\u090F', '\u0947', '\u0946', '\u0945']  # E
ipa_hindi_dict['\u025B'] = ['\u0910', '\u0948']   # AI
ipa_hindi_dict['\u006F'] = ['\u0913', '\u094B', '\u094A']  # O
ipa_hindi_dict['\u0254'] = ['\u0914', '\u094C', '\u0913', '\u094b']  # AU
ipa_hindi_dict['\u0303'] = ['\u0901', '\u0902']
ipa_hindi_dict['\u006E'] = ['\u0928']   # NA
ipa_hindi_dict['\u0266'] = ['\u0939']   # HA

# ---- consonants (middle/end position) ----
ipa_hindi_dict['\u006B']               = ['\u0915']
ipa_hindi_dict['\u02B0']               = ['\u0916']
ipa_hindi_dict['\u0261']               = ['\u0917']
ipa_hindi_dict['\u0324']               = ['\u0918']
ipa_hindi_dict['\u014B']               = ['\u0919']
ipa_hindi_dict['\u0074\u0361\u0283']   = ['\u091A']
ipa_hindi_dict['\u0074\u0361\u0283\u02B0'] = ['\u091B']
ipa_hindi_dict['\u0064\u0361\u0292']   = ['\u091C']
ipa_hindi_dict['\u0064\u0361\u0292\u0324'] = ['\u091D']
ipa_hindi_dict['\u0272']               = ['\u091E']
ipa_hindi_dict['\u0288']               = ['\u091F']
ipa_hindi_dict['\u0288\u02B0']         = ['\u0920']
ipa_hindi_dict['\u0256']               = ['\u0921']
ipa_hindi_dict['\u0256\u0324']         = ['\u0922']
ipa_hindi_dict['\u0273']               = ['\u0923']
ipa_hindi_dict['\u0074\u032A']         = ['\u0924']
ipa_hindi_dict['\u0074\u032A\u02B0']   = ['\u0925']
ipa_hindi_dict['\u0064']               = ['\u0926']
ipa_hindi_dict['\u0064\u0324']         = ['\u0927']
ipa_hindi_dict['\u027D\u0324']         = ['\u095D']
ipa_hindi_dict['\u0070']               = ['\u092A']
ipa_hindi_dict['\u0070\u02B0']         = ['\u092B']
ipa_hindi_dict['\u0062']               = ['\u092C']
ipa_hindi_dict['\u0062\u0324']         = ['\u092D']
ipa_hindi_dict['\u006D']               = ['\u092E']
ipa_hindi_dict['\u006A']               = ['\u092F']
ipa_hindi_dict['\u0072']               = ['\u0930']
ipa_hindi_dict['\u006C']               = ['\u0932']
ipa_hindi_dict['\u028B']               = ['\u0935']
ipa_hindi_dict['\u0283']               = ['\u0936']
ipa_hindi_dict['\u0282']               = ['\u0937']
ipa_hindi_dict['\u0073']               = ['\u0938']
ipa_hindi_dict['\u0071']               = ['\u0958']
ipa_hindi_dict['\u0078']               = ['\u0959']
ipa_hindi_dict['\u0263']               = ['\u095A']
ipa_hindi_dict['\u007A']               = ['\u095B']
ipa_hindi_dict['\u027D']               = ['\u095C']
ipa_hindi_dict['\u0066']               = ['\u095E']

# ─────────────────────────────────────────────────────────────────────────────
# Urdu → IPA dictionaries  (position-dependent: start / middle / end)
# ─────────────────────────────────────────────────────────────────────────────

urdu_ipa_hindi_dict_start  = {}
urdu_ipa_hindi_dict_middle = {}
urdu_ipa_hindi_dict_end    = {}

# ---------- START ----------
urdu_ipa_hindi_dict_start['\u094D'] = []
urdu_ipa_hindi_dict_start['\u0651'] = ['\u0651']
urdu_ipa_hindi_dict_start['\u0627'] = ['\u0259', '\u0061', '\u028A', '\u0075']
urdu_ipa_hindi_dict_start['\u0639'] = ['\u0259', '\u0061']
urdu_ipa_hindi_dict_start['\u0622'] = ['\u0061', '\u0259']
urdu_ipa_hindi_dict_start['\u0627\u06CC'] = ['\u0069', '\u0065']
urdu_ipa_hindi_dict_start['\u0627\u0648'] = ['\u0075', '\u006F', '\u0254']
urdu_ipa_hindi_dict_start['\u0627\u0624'] = ['\u0075', '\u006F', '\u0254']
urdu_ipa_hindi_dict_start['\u0631']       = ['\u090B']
urdu_ipa_hindi_dict_start['\u0627\uFBFE'] = ['\u0065', '\u025B']
urdu_ipa_hindi_dict_start['\u0646'] = ['\u006E', '\u0303', '\u014B', '\u0272', '\u0273', '\u006E', '\u006D', '\u0303']
urdu_ipa_hindi_dict_start['\u067e\u06be'] = ['\u0070\u02B0']
urdu_ipa_hindi_dict_start['\u06be']       = ['\u0266']
urdu_ipa_hindi_dict_start['\u06D2']       = ['\u006A', '\u0065']
urdu_ipa_hindi_dict_start['\u06A9']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_start['\u0642']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_start['\u06A9\u06BE'] = ['\u02B0']
urdu_ipa_hindi_dict_start['\u062E']       = ['\u02B0', '\u0078']
urdu_ipa_hindi_dict_start['\u06AF']       = ['\u0261']
urdu_ipa_hindi_dict_start['\u063A']       = ['\u0261', '\u0263']
urdu_ipa_hindi_dict_start['\u06AF\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_start['\u063A\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_start['\u0686']       = ['\u0074\u0361\u0283']
urdu_ipa_hindi_dict_start['\u0686\u06BE'] = ['\u0074\u0361\u0283\u02B0']
urdu_ipa_hindi_dict_start['\u062C']       = ['\u0064\u0361\u0292']
urdu_ipa_hindi_dict_start['\u062C\u06BE'] = ['\u0064\u0361\u0292\u0324']
urdu_ipa_hindi_dict_start['\u0679']       = ['\u0288']
urdu_ipa_hindi_dict_start['\u0679\u06BE'] = ['\u0288\u02B0']
urdu_ipa_hindi_dict_start['\u0688']       = ['\u0256']
urdu_ipa_hindi_dict_start['\u0691']       = ['\u0256', '\u027D']
urdu_ipa_hindi_dict_start['\u0688\u06BE'] = ['\u0256\u0324']
urdu_ipa_hindi_dict_start['\u0691\u06BE'] = ['\u0256\u0324', '\u027D\u0324']
urdu_ipa_hindi_dict_start['\u062a']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_start['\u0637']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_start['\u062a\u06BE'] = ['\u0074\u032A\u02B0']
urdu_ipa_hindi_dict_start['\u0637\u06BE'] = ['\u0074\u032A\u02B0']
urdu_ipa_hindi_dict_start['\u062F']       = ['\u0064']
urdu_ipa_hindi_dict_start['\u062F\u06BE'] = ['\u0064\u0324']
urdu_ipa_hindi_dict_start['\u067e']       = ['\u0070']
urdu_ipa_hindi_dict_start['\u0641']       = ['\u0070\u02B0', '\u0066']
urdu_ipa_hindi_dict_start['\u0628']       = ['\u0062']
urdu_ipa_hindi_dict_start['\u0628\u06BE'] = ['\u0062\u0324']
urdu_ipa_hindi_dict_start['\u0645']       = ['\u006D']
urdu_ipa_hindi_dict_start['\u06CC']       = ['\u006A']
urdu_ipa_hindi_dict_start['\u0644']       = ['\u006C']
urdu_ipa_hindi_dict_start['\u0648']       = ['\u028B']
urdu_ipa_hindi_dict_start['\u0634']       = ['\u0283', '\u0282']
urdu_ipa_hindi_dict_start['\u0633']       = ['\u0073']
urdu_ipa_hindi_dict_start['\u062B']       = ['\u0073']
urdu_ipa_hindi_dict_start['\u0635']       = ['\u0073']
urdu_ipa_hindi_dict_start['\u062D']       = ['\u0266']
urdu_ipa_hindi_dict_start['\u06C1']       = ['\u0266']
urdu_ipa_hindi_dict_start['\u0630']       = ['\u007A']
urdu_ipa_hindi_dict_start['\u0632']       = ['\u007A', '\u0064\u0361\u0292']
urdu_ipa_hindi_dict_start['\u0636']       = ['\u007A']
urdu_ipa_hindi_dict_start['\u0638']       = ['\u007A']
urdu_ipa_hindi_dict_start['\u0698']       = ['\u0292']

# ---------- MIDDLE ----------
urdu_ipa_hindi_dict_middle['\u094D'] = []
urdu_ipa_hindi_dict_middle['\u0651'] = ['\u0651']
urdu_ipa_hindi_dict_middle['\u0627'] = ['\u0061']
urdu_ipa_hindi_dict_middle['\u0622'] = ['\u0061']
urdu_ipa_hindi_dict_middle['\u0670'] = ['\u0061']
urdu_ipa_hindi_dict_middle['\u0626'] = ['\u026A', '\u0069', '\u006A']
urdu_ipa_hindi_dict_middle['\u0648'] = ['\u028A', '\u0075', '\u006F', '\u028B', '\u0254']
urdu_ipa_hindi_dict_middle['\u0624'] = ['\u0075', '\u006F', '\u028B', '\u0254']
urdu_ipa_hindi_dict_middle['\u0631'] = ['\u090B', '\u0072']
urdu_ipa_hindi_dict_middle['\u06CC'] = ['\u0065', '\u006A', '\u025B', '\u0069']
urdu_ipa_hindi_dict_middle['\u0646'] = ['\u006E', '\u0303', '\u014B', '\u0272', '\u0273', '\u006E', '\u006D', '\u0303']
urdu_ipa_hindi_dict_middle['\u067e\u06be'] = ['\u0070\u02B0']
urdu_ipa_hindi_dict_middle['\u06be']       = ['\u0266']
urdu_ipa_hindi_dict_middle['\u06D2']       = ['\u006A', '\u0065', '\u026A', '\u0069']
urdu_ipa_hindi_dict_middle['\u0639']       = ['\u0259', '\u0061']
urdu_ipa_hindi_dict_middle['\u06A9']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_middle['\u0642']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_middle['\u06A9\u06BE'] = ['\u02B0']
urdu_ipa_hindi_dict_middle['\u062E']       = ['\u02B0', '\u0078']
urdu_ipa_hindi_dict_middle['\u06AF']       = ['\u0261']
urdu_ipa_hindi_dict_middle['\u063A']       = ['\u0261', '\u0263']
urdu_ipa_hindi_dict_middle['\u06AF\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_middle['\u063A\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_middle['\u0686']       = ['\u0074\u0361\u0283']
urdu_ipa_hindi_dict_middle['\u0686\u06BE'] = ['\u0074\u0361\u0283\u02B0']
urdu_ipa_hindi_dict_middle['\u062C']       = ['\u0064\u0361\u0292']
urdu_ipa_hindi_dict_middle['\u062C\u06BE'] = ['\u0064\u0361\u0292\u0324']
urdu_ipa_hindi_dict_middle['\u0679']       = ['\u0288']
urdu_ipa_hindi_dict_middle['\u0679\u06BE'] = ['\u0288\u02B0']
urdu_ipa_hindi_dict_middle['\u0688']       = ['\u0256', '\u027D']
urdu_ipa_hindi_dict_middle['\u0691']       = ['\u0256']
urdu_ipa_hindi_dict_middle['\u0688\u06BE'] = ['\u0256\u0324']
urdu_ipa_hindi_dict_middle['\u0691\u06BE'] = ['\u0256\u0324', '\u027D\u0324']
urdu_ipa_hindi_dict_middle['\u062a']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_middle['\u0637']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_middle['\u062a\u06BE'] = ['\u0074\u032A\u02B0']
urdu_ipa_hindi_dict_middle['\u062F']       = ['\u0064']
urdu_ipa_hindi_dict_middle['\u062F\u06BE'] = ['\u0064\u0324']
urdu_ipa_hindi_dict_middle['\u06BA']       = ['\u006E', '\u0902']
urdu_ipa_hindi_dict_middle['\u067e']       = ['\u0070']
urdu_ipa_hindi_dict_middle['\u0641']       = ['\u0070\u02B0', '\u0066']
urdu_ipa_hindi_dict_middle['\u0628']       = ['\u0062']
urdu_ipa_hindi_dict_middle['\u0628\u06BE'] = ['\u0062\u0324']
urdu_ipa_hindi_dict_middle['\u0645']       = ['\u006D']
urdu_ipa_hindi_dict_middle['\u0644']       = ['\u006C']
urdu_ipa_hindi_dict_middle['\u0634']       = ['\u0283', '\u0282']
urdu_ipa_hindi_dict_middle['\u0633']       = ['\u0073']
urdu_ipa_hindi_dict_middle['\u062B']       = ['\u0073']
urdu_ipa_hindi_dict_middle['\u0635']       = ['\u0073']
urdu_ipa_hindi_dict_middle['\u062D']       = ['\u0266']
urdu_ipa_hindi_dict_middle['\u06C1']       = ['\u0266']
urdu_ipa_hindi_dict_middle['\u0630']       = ['\u007A']
urdu_ipa_hindi_dict_middle['\u0632']       = ['\u007A']
urdu_ipa_hindi_dict_middle['\u0636']       = ['\u007A']
urdu_ipa_hindi_dict_middle['\u0638']       = ['\u007A']
urdu_ipa_hindi_dict_middle['\u0698']       = ['\u0292']

# ---------- END ----------
urdu_ipa_hindi_dict_end['\u094D'] = []
urdu_ipa_hindi_dict_end['\u0651'] = ['\u0651']
urdu_ipa_hindi_dict_end['\u0626'] = ['\u026A', '\u0069', '\u006A']
urdu_ipa_hindi_dict_end['\u0639'] = ['\u0259', '\u0061']
urdu_ipa_hindi_dict_end['\u0622'] = ['\u0061']
urdu_ipa_hindi_dict_end['\u06CC'] = ['\u026A', '\u0069', '\u0065']
urdu_ipa_hindi_dict_end['\u0627'] = ['\u0259', '\u0061']
urdu_ipa_hindi_dict_end['\u06CC\u0670'] = ['\u0061']
urdu_ipa_hindi_dict_end['\u06C1'] = ['\u0061', '\u0266']
urdu_ipa_hindi_dict_end['\u0648'] = ['\u0075', '\u006F', '\u028B', '\u0254']
urdu_ipa_hindi_dict_end['\u0624'] = ['\u0075', '\u006F', '\u028B', '\u0254']
urdu_ipa_hindi_dict_end['\u0631'] = ['\u090B']
urdu_ipa_hindi_dict_end['\u06D2'] = ['\u0065', '\u006A', '\u025B']
urdu_ipa_hindi_dict_end['\u06BA'] = ['\u0303', '\u014B', '\u0272', '\u0273', '\u006E', '\u006D', '\u0303', '\u028A']
urdu_ipa_hindi_dict_end['\u067e\u06be'] = ['\u0070\u02B0']
urdu_ipa_hindi_dict_end['\u06be']       = ['\u0266']
urdu_ipa_hindi_dict_end['\u06A9']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_end['\u0642']       = ['\u006B', '\u0071']
urdu_ipa_hindi_dict_end['\u06A9\u06BE'] = ['\u02B0']
urdu_ipa_hindi_dict_end['\u062E']       = ['\u02B0', '\u0078']
urdu_ipa_hindi_dict_end['\u06AF']       = ['\u0261']
urdu_ipa_hindi_dict_end['\u063A']       = ['\u0261', '\u0263']
urdu_ipa_hindi_dict_end['\u06AF\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_end['\u063A\u06BE'] = ['\u0324']
urdu_ipa_hindi_dict_end['\u0686']       = ['\u0074\u0361\u0283']
urdu_ipa_hindi_dict_end['\u0686\u06BE'] = ['\u0074\u0361\u0283\u02B0']
urdu_ipa_hindi_dict_end['\u062C']       = ['\u0064\u0361\u0292']
urdu_ipa_hindi_dict_end['\u062C\u06BE'] = ['\u0064\u0361\u0292\u0324']
urdu_ipa_hindi_dict_end['\u0679']       = ['\u0288']
urdu_ipa_hindi_dict_end['\u0679\u06BE'] = ['\u0288\u02B0']
urdu_ipa_hindi_dict_end['\u0688']       = ['\u0256']
urdu_ipa_hindi_dict_end['\u0691']       = ['\u0256', '\u027D']
urdu_ipa_hindi_dict_end['\u0688\u06BE'] = ['\u0256\u0324']
urdu_ipa_hindi_dict_end['\u0691\u06BE'] = ['\u0256\u0324', '\u027D\u0324']
urdu_ipa_hindi_dict_end['\u062a']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_end['\u0637']       = ['\u0074\u032A']
urdu_ipa_hindi_dict_end['\u062a\u06BE'] = ['\u0074\u032A\u02B0']
urdu_ipa_hindi_dict_end['\u062F']       = ['\u0064']
urdu_ipa_hindi_dict_end['\u062F\u06BE'] = ['\u0064\u0324']
urdu_ipa_hindi_dict_end['\u0646']       = ['\u006E']
urdu_ipa_hindi_dict_end['\u067e']       = ['\u0070']
urdu_ipa_hindi_dict_end['\u0641']       = ['\u0070\u02B0', '\u0066']
urdu_ipa_hindi_dict_end['\u0628']       = ['\u0062']
urdu_ipa_hindi_dict_end['\u0628\u06BE'] = ['\u0062\u0324']
urdu_ipa_hindi_dict_end['\u0645']       = ['\u006D']
urdu_ipa_hindi_dict_end['\u0631']       = ['\u0072']
urdu_ipa_hindi_dict_end['\u0644']       = ['\u006C']
urdu_ipa_hindi_dict_end['\u0634']       = ['\u0283', '\u0282']
urdu_ipa_hindi_dict_end['\u0633']       = ['\u0073']
urdu_ipa_hindi_dict_end['\u062B']       = ['\u0073']
urdu_ipa_hindi_dict_end['\u0635']       = ['\u0073']
urdu_ipa_hindi_dict_end['\u062D']       = ['\u0266']
urdu_ipa_hindi_dict_end['\u0630']       = ['\u007A']
urdu_ipa_hindi_dict_end['\u0632']       = ['\u007A']
urdu_ipa_hindi_dict_end['\u0636']       = ['\u007A']
urdu_ipa_hindi_dict_end['\u0638']       = ['\u007A']
urdu_ipa_hindi_dict_end['\u0698']       = ['\u0292']

# ─────────────────────────────────────────────────────────────────────────────
# Core transliteration functions  (ported from urdu_to_hindi.py to Python 3)
# ─────────────────────────────────────────────────────────────────────────────

def ipa_to_hindi_char(sym, is_start):
    """Return the first (most likely) Hindi character for an IPA symbol."""
    d = ipa_hindi_dict_start if is_start else ipa_hindi_dict
    if sym in d and d[sym]:
        return d[sym][0]
    return ''


def transliterate_word(urdu_word):
    """Transliterate a single Urdu word to Hindi using a greedy first-match
    strategy (fast, O(n) per word)."""
    if not urdu_word:
        return urdu_word

    chars = list(urdu_word)
    n = len(chars)
    result = []
    idx = 0

    # ---- FIRST position: look-ahead up to 3 chars ----
    found = False
    for j in range(min(3, n), 0, -1):
        combo = ''.join(chars[0:j])
        if combo in urdu_ipa_hindi_dict_start and urdu_ipa_hindi_dict_start[combo]:
            ipa = urdu_ipa_hindi_dict_start[combo][0]
            result.append(ipa_to_hindi_char(ipa, True))
            idx = j
            found = True
            break
    if not found:
        idx = 1   # skip unrecognised first character

    # ---- MIDDLE positions ----
    while idx < n - 1:
        found = False
        for j in range(min(3, n - idx), 0, -1):
            combo = ''.join(chars[idx: idx + j])
            if combo in urdu_ipa_hindi_dict_middle and urdu_ipa_hindi_dict_middle[combo]:
                ipa = urdu_ipa_hindi_dict_middle[combo][0]
                result.append(ipa_to_hindi_char(ipa, False))
                idx += j
                found = True
                break
        if not found:
            idx += 1   # skip unrecognised character

    # ---- LAST position ----
    if n > 0:
        last = chars[-1]
        if last in urdu_ipa_hindi_dict_end and urdu_ipa_hindi_dict_end[last]:
            ipa = urdu_ipa_hindi_dict_end[last][0]
            result.append(ipa_to_hindi_char(ipa, False))

    hindi = ''.join(result)
    return hindi if hindi else urdu_word


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

# Unicode ranges for Urdu / Arabic script characters
URDU_RANGE = re.compile(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+')


def is_urdu_char(ch):
    return '\u0600' <= ch <= '\u06FF' or '\uFB50' <= ch <= '\uFDFF' or '\uFE70' <= ch <= '\uFEFF'


def transliterate_line(line):
    """Transliterate all Urdu tokens in a line, keeping non-Urdu parts intact."""
    # Split into tokens while preserving separators
    parts = re.split(r'(\s+)', line)
    result = []
    for part in parts:
        if URDU_RANGE.search(part):
            result.append(transliterate_word(part))
        else:
            result.append(part)
    return ''.join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    input_path  = os.path.join(script_dir, 'quran_urdu_jalandhry.txt')
    output_path = os.path.join(script_dir, 'quran_hindi_transliterated.txt')

    with codecs.open(input_path, encoding='utf-8') as fin, \
         codecs.open(output_path, 'w', encoding='utf-8') as fout:

        for line_num, line in enumerate(fin, 1):
            line = line.rstrip('\n')
            transliterated = transliterate_line(line)
            fout.write(transliterated + '\n')

            if line_num % 500 == 0:
                print(f'  Processed {line_num} lines…')

    print(f'Done. Output written to: {output_path}')


if __name__ == '__main__':
    main()
