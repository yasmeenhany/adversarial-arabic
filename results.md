# Results

Each row: obfuscated text given to a model (pasted into its chat app, or sent
through OpenRouter by `run_llm.py`), followed by the questions in `data/<text>.questions.txt` (the `.prompt.txt` files written by
`obfuscate.py` combine both). Scoring: 1 = correct, 0.5 = partly correct,
0 = wrong. Rows added by `score.py` or `run_llm.py` have a per-question
breakdown in `experiments/<text>/<mode>/<text>.<mode>.<model>.judge-<scored by>.scores.md`
(API runs also keep the raw reply there; earlier runs are in `runs/` and
`output/`). "Scored by" is a judge model,
`manual` (scored by hand) or `keywords` (keyword suggestions accepted as-is).
Since 2026-10-24 each method also has a separate restore prompt
(`.restore-prompt.txt`, sent as its own request) asking the model to rewrite
the text as the original. Restoration is the judge's score out of 10, with the
automatic similarity of the restored text to the original (characters, and
words recovered in order, ignoring diacritics and punctuation); "—" means no
restoration was run.

| Date | Text | Mode | Model | Answers | Restoration | Scored by | Notes |
|---|---|---|---|---|---|---|---|
| 2026-10-10 | tariq_ibn_ziyad_speech | both (homoglyph+presentation) | Gemini | n/a | — | manual | Read it easily; speech is famous, so likely memorised |
| 2026-10-10 | original_text | both (homoglyph+presentation) | Gemini | 14/14 | — | manual | Quoted the Arabic back in standard codepoints |
| 2026-10-10 | original_text | tashkeel stacked (assumed) | Gemini | 14/14 | — | manual | |
| 2026-10-10 | original_text | dotless | Gemini | 13.5/14 | — | manual | Misread skeletons (صفة, حطاب, حرار); Q11 lost "neighbour" |
| 2026-10-10 | original_text | dotless+disconnect+tashkeel | Gemini | 5.5/14 | — | manual | Wrong numbers (170, 50, 20, ten); invented the Q13/Q14 story |
| 2026-10-24 | akkad | 3-root-permute+18-pattern | Gemini | 10/10 | — | manual |  |
| 2026-10-24 | akkad | 2-homoglyph | Gemini | 9.5/10 | — | manual |  |
| 2026-10-24 | akkad | 2-homoglyph | google/gemini-3.8-flash | 9.5/10 | — | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 2-homoglyph | anthropic/claude-sonnet-5.5 | 10/10 | — | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 2-homoglyph | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 98% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 10-dotless | anthropic/claude-sonnet-5.5 | 9/10 | 9/10 (98% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 12-arabizi-0.3-word | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 12-arabizi | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 3-root-1 | anthropic/claude-sonnet-5.5 | 0/10 | 2/10 (75% characters, 51% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 3-root-1-permute | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 4-gender | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 98% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 5-number | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (98% characters, 88% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 15-dialect | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (98% characters, 96% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 4-gender-1 | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 5-number-1 | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 96% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 12-arabizi-word | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 15-dialect-full | anthropic/claude-sonnet-5.5 | 10/10 | 7/10 (95% characters, 91% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 16-conjunction | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (99% characters, 95% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 17-case | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 17-case | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 18-pattern-1 | anthropic/claude-sonnet-5.5 | 8.5/10 | 6/10 (94% characters, 80% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 1-zwc | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 8-tashkeel-stacked | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 9-kashida-1 | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 19-blank-0.5-mix | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 97% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 20-space-1 | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 21-huruf-0.5 | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 95% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 22-silent | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 22-silent-0.5 | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 98% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 6-order-shuffle | anthropic/claude-sonnet-5.5 | 9.5/10 | 8/10 (94% characters, 93% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 11-shuffle | anthropic/claude-sonnet-5.5 | 10/10 | 8/10 (99% characters, 96% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 3-root-1-on-content | anthropic/claude-sonnet-5.5 | 0/10 | 0/10 (70% characters, 36% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 3-root-1-on-function | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 3-root-1-on-random | anthropic/claude-sonnet-5.5 | 6.5/10 | 6/10 (90% characters, 80% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 18-pattern-1+10-dotless+8-tashkeel-on-content | anthropic/claude-sonnet-5.5 | 8/10 | 3/10 (91% characters, 75% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 2-homoglyph+13-presentation+1-zwc | anthropic/claude-sonnet-5.5 | 10/10 | 9/10 (100% characters, 99% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 11-shuffle+disconnect-0.5+9-kashida-1 | anthropic/claude-sonnet-5.5 | 10/10 | 7/10 (98% characters, 90% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | akkad | 0-no-text | anthropic/claude-sonnet-5.5 | 4.5/10 | — | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 0-no-text | anthropic/claude-sonnet-5.5 | 4.5/14 | — | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 10-dotless | anthropic/claude-sonnet-5.5 | 12.5/14 | 8/10 (99% characters, 98% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 11-shuffle+disconnect-0.5+9-kashida-1 | anthropic/claude-sonnet-5.5 | 12/14 | 6/10 (98% characters, 93% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 18-pattern-1+10-dotless+8-tashkeel-on-content | anthropic/claude-sonnet-5.5 | 9/14 | 6/10 (92% characters, 81% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 18-pattern-1 | anthropic/claude-sonnet-5.5 | 11/14 | 7/10 (98% characters, 94% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 2-homoglyph+13-presentation+1-zwc | anthropic/claude-sonnet-5.5 | 14/14 | 10/10 (100% characters, 100% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 3-root-1-on-random | anthropic/claude-sonnet-5.5 | 7.5/14 | 5/10 (91% characters, 83% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 3-root-1 | anthropic/claude-sonnet-5.5 | 5.5/14 | 2/10 (77% characters, 54% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | 6-order-shuffle | anthropic/claude-sonnet-5.5 | 13/14 | 6/10 (85% characters, 86% words) | openai/gpt-5.6-terra |  |
| 2026-10-24 | original_text | disconnect+10-dotless+8-tashkeel | anthropic/claude-sonnet-5.5 | 13/14 | 9/10 (99% characters, 99% words) | openai/gpt-5.6-terra |  |

## dotless+disconnect+tashkeel, per question

| Q | Question | Expected | Gemini | Score |
|---|---|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim | Salam Abd al-Rahim | 0.5 |
| 2 | At what age did he start making pottery? | 12 | 10 | 0 |
| 3 | Who taught him the craft? | Grandfather | Grandfather | 1 |
| 4 | Where does he get his clay? | Eastern bank of the river | Bank of the lower river | 0.5 |
| 5 | How many jars were ordered? | 120 | 170 | 0 |
| 6 | What colour were the jar handles to be? | Blue | (Dark) blue | 1 |
| 7 | What was the delivery deadline? | Before the spring festival | Before spring (عيد الربيع) | 1 |
| 8 | How many jars fit in his old kiln at once? | 15 | 50 | 0 |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr | وادي الصدر, "Valley of Cedar" | 0.5 |
| 10 | What is his daughter's name? | Layla | Layla | 1 |
| 11 | Who helped build the second kiln? | Neighbour, a blacksmith | His daughter Layla | 0 |
| 12 | How long did the work take? | 40 days | 20 days | 0 |
| 13 | How many jars broke during firing? | 3 | None broke, only the handles cracked | 0 |
| 14 | What did he do about the broken jars? | Made 3 larger jars as a gift | Made new handles | 0 |

## Texts and questions

### original_text

`data/original_text.txt`:

> في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

| Q | Question | Expected answer |
|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim |
| 2 | At what age did he start making pottery? | 12 |
| 3 | Who taught him the craft? | His grandfather |
| 4 | Where does he get his clay? | The eastern bank of the river |
| 5 | How many jars were ordered? | 120 |
| 6 | What colour were the jar handles to be? | Blue |
| 7 | What was the delivery deadline? | Before the spring festival |
| 8 | How many jars fit in his old kiln at once? | 15 |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr |
| 10 | What is his daughter's name? | Layla |
| 11 | Who helped build the second kiln? | The neighbour, a blacksmith |
| 12 | How long did the work take? | 40 days |
| 13 | How many jars broke during firing? | 3 |
| 14 | What did he do about the broken jars? | Made three larger jars and gave them to the merchant as thanks |

### akkad

`data/akkad.txt`:

> إنَّ التَّفْكِيرَ فَرِيضَةٌ لا رُخْصَةَ فِيهَا وَلا تَعْطِيلَ لَهَا، وَالعَقْلُ البَشَرِيُّ لَمْ يُخْلَقْ لِيَكُونَ أَمِينًا عَلَى مَنُقُولاتٍ يَتَلَقَّاهَا بِالتَّسْلِيمِ وَالأَعْمَى، بَلْ خُلِقَ لِيَكُونَ حَكَمًا يُمَيِّزُ بَيْنَ الصَّوَابِ وَالخَطَأِ، وَيَقِيسُ الأُمُورَ بِمِقْيَاسِ المَنْطِقِ وَالبُرْهَانِ. إنَّ التَّخَلِّيَ عَنِ التَّفْكِيرِ المُنْصِفِ المُنْتَجِ هُوَ جَنَايَةٌ يَرْتَكِبُهَا المَرْءُ فِي حَقِّ نَفْسِهِ قَبْلَ أَنْ تَكُونَ هَضْمًا لِحُقُوقِ الآخَرِينَ.
>
> وَكُلُّ مُحَاوَلَةٍ لِحَجْرِ العَقْلِ أَوْ مَنْعِهِ مِنَ النَّظَرِ فِي حَقَائِقِ الكَوْنِ وَالحَيَاةِ هيَ صَدٌّ عَنْ سَبِيلِ المَعْرِفَةِ. إنَّ الإِنْسَانَ الَّذِي يُسَلِّمُ عَقْلَهُ لِغَيْرِهِ يَفْقِدُ خَاصِيَّتَهُ الأُولَى الَّتِي كُرِّمَ بِهَا، وَيَغْدُو عَاجِزًا عَنْ مُوَاجَهَةِ التَّحَدِّيَاتِ الحَضَارِيَّةِ الَّتِي تَطْلُبُ مِنَ النَّفْسِ الإِنْسَانِيَّةِ صَمُودًا وَشَجَاعَةً فِي ارْتِقَاءِ مَرَاتِبِ الفَهْمِ وَالوَعْيِ.

| Q | Question | Expected answer |
|---|---|---|
| 1 | What does the author call thinking? | A duty (fariḍa) that allows no exemption or suspension |
| 2 | What was the human mind NOT created to be? | A custodian of transmitted ideas accepted through blind submission |
| 3 | What was the human mind created to be instead? | A judge that tells right from wrong |
| 4 | By what standard should the mind measure things? | Logic and proof |
| 5 | What does the author call abandoning fair, productive thinking? | A crime (jināya) |
| 6 | Against whom is that act committed first? | Against oneself, before it wrongs the rights of others |
| 7 | What does the author call any attempt to restrict the mind or stop it from contemplating the truths of the universe and life? | Blocking the path to knowledge |
| 8 | What does a person who hands their mind over to others lose? | The first trait they were honoured with |
| 9 | What does that person become unable to face? | Civilizational challenges |
| 10 | What does the author say is demanded of the human soul? | Steadfastness and courage in rising through the levels of understanding and awareness |
