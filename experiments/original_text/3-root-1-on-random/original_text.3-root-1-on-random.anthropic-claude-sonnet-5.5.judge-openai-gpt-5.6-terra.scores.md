# original_text — 3-root-1-on-random — anthropic/claude-sonnet-5.5

Date: 2026-10-24  
Answers: 7.5/14  
Restoration: 5/10 (91% characters, 83% words)  
Scored by: openai/gpt-5.6-terra  
Prompt: `experiments/original_text/3-root-1-on-random/original_text.3-root-1-on-random.prompt.txt`

## Answers

| Q | Question | Expected | anthropic/claude-sonnet-5.5 | Score | Judge's reason |
|---|---|---|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim | Salem bin Abd al-Rahim (سالم بن عبد الرحيم). | 1 | “Salem bin Abd al-Rahim” is the same name as Salim ibn Abd al-Rahim. |
| 2 | At what age did he start making pottery? | 12 | At ten. The text says he started work when he reached ten, though the word "الراخية" is garbled. | 0 | It gives age ten instead of 12. |
| 3 | Who taught him the craft? | His grandfather | His grandfather. | 1 | Matches: his grandfather taught him. |
| 4 | Where does he get his clay? | The eastern bank of the river | From the eastern bank of the "الكبل". The text names the place but does not say clearly what "الكبل" is. | 0.5 | It identifies the eastern bank but does not identify it as the river. |
| 5 | How many jars were ordered? | 120 | 120 jars. | 1 | Matches: 120 jars. |
| 6 | What colour were the jar handles to be? | Blue | The text does not say clearly. The description "ذات مطامر شزراء" is garbled, and no handle colour is given. | 0 | It does not provide the expected blue colour. |
| 7 | What was the delivery deadline? | Before the spring festival | Before the "نشور تيه الربيع", which seems to mean before the start of spring. The wording is unclear. | 0.5 | It gives a deadline before spring/start of spring, but omits the spring festival. |
| 8 | How many jars fit in his old kiln at once? | 15 | The text is garbled here ("خمس بكره جرة"). It seems to mean about five jars, but this is uncertain. | 0 | It suggests about five jars rather than 15. |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr | The text does not say, and it never mentions blue. It says only that something yellow ("اللوح الأصفر") is found only in a place called "وأسى الفسق", which is unclear. | 0 | It does not give Wadi al-Sidr. |
| 10 | What is his daughter's name? | Layla | Laythi (ليثي). | 0 | It gives Laythi rather than Layla. |
| 11 | Who helped build the second kiln? | The neighbour, a blacksmith | His neighbour, the blacksmith. | 1 | Matches: the neighbour, who was a blacksmith. |
| 12 | How long did the work take? | 40 days | Forty days. | 1 | Matches: 40 days. |
| 13 | How many jars broke during firing? | 3 | Three jars. | 1 | Matches: three jars. |
| 14 | What did he do about the broken jars? | Made three larger jars and gave them to the merchant as thanks | He made three larger pieces ("ثلاث عقاد أكبر") from the broken ones. He then gave them as a gift to "الفالج", apparently in gratitude, but the wording is unclear. | 0.5 | It mentions making three larger items and giving them as a gift, but does not clearly identify the merchant and adds that they were made from the broken jars. |

## Restoration

Judge: 5/10 — النص يحافظ على القصة الأساسية، لكنه يغيّر تفاصيل كثيرة مهمة تتعلق بالعمر والطلب ومصدر الحجر والكمية والجهة التي أُهديت إليها الجرار.  
Similarity to the original: 91% characters, 83% words

| Original | Restored |
|---|---|
| الثانية عشرة | الخامسة عشرة |
| رسالة من صاحب نزل كبير | يقود حمارا محملا بالأقمشة |
| خمس عشرة | خمس وعشرين |
| حجر نادر | حجر خاص |
| وادي السدر | أقصى الشرق |
| الحجر | الحطب |
| للتاجر | للحداد |
| صبره | صنيعه |
| تكسوه | تحميه |
| ورث | تعلم |

Restored:

> في قرية صغيرة تقع على سفح جبل تحميه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الخامسة عشرة من عمره. وتعلم سالم هذه المهنة عن جده، الذي علمه كيف يستخرج الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي أواخر أيام الشتاء، جاءه تاجر من المدينة يقود حمارا محملا بالأقمشة، يطلب منه مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس وعشرين جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر خاص لا يوجد إلا في أقصى الشرق.
>
> غير أن ابنته ليلى أقنعته بأن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالذهاب إلى الوادي لجلب الحطب. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار جميعها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للحداد عرفانا له على صنيعه.

Original:

> في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

## Answer reply

```
1. Salem bin Abd al-Rahim (سالم بن عبد الرحيم).
2. At ten. The text says he started work when he reached ten, though the word "الراخية" is garbled.
3. His grandfather.
4. From the eastern bank of the "الكبل". The text names the place but does not say clearly what "الكبل" is.
5. 120 jars.
6. The text does not say clearly. The description "ذات مطامر شزراء" is garbled, and no handle colour is given.
7. Before the "نشور تيه الربيع", which seems to mean before the start of spring. The wording is unclear.
8. The text is garbled here ("خمس بكره جرة"). It seems to mean about five jars, but this is uncertain.
9. The text does not say, and it never mentions blue. It says only that something yellow ("اللوح الأصفر") is found only in a place called "وأسى الفسق", which is unclear.
10. Laythi (ليثي).
11. His neighbour, the blacksmith.
12. Forty days.
13. Three jars.
14. He made three larger pieces ("ثلاث عقاد أكبر") from the broken ones. He then gave them as a gift to "الفالج", apparently in gratitude, but the wording is unclear.
```

## Restore reply

```
في قرية صغيرة تقع على سفح جبل تحميه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الخامسة عشرة من عمره. وتعلم سالم هذه المهنة عن جده، الذي علمه كيف يستخرج الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.

وفي أواخر أيام الشتاء، جاءه تاجر من المدينة يقود حمارا محملا بالأقمشة، يطلب منه مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس وعشرين جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر خاص لا يوجد إلا في أقصى الشرق.

غير أن ابنته ليلى أقنعته بأن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالذهاب إلى الوادي لجلب الحطب. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار جميعها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للحداد عرفانا له على صنيعه.
```
