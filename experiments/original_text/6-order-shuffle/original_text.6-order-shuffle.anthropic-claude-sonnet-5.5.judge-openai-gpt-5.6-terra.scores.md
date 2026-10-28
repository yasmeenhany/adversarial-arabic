# original_text — 6-order-shuffle — anthropic/claude-sonnet-5.5

Date: 2026-10-24  
Answers: 13/14  
Restoration: 6/10 (85% characters, 86% words)  
Scored by: openai/gpt-5.6-terra  
Prompt: `experiments/original_text/6-order-shuffle/original_text.6-order-shuffle.prompt.txt`

## Answers

| Q | Question | Expected | anthropic/claude-sonnet-5.5 | Score | Judge's reason |
|---|---|---|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim | Salim ibn Abd al-Rahim. | 1 | Exact name match. |
| 2 | At what age did he start making pottery? | 12 | At twelve. | 1 | Twelve matches 12. |
| 3 | Who taught him the craft? | His grandfather | His grandfather. | 1 | Exact match. |
| 4 | Where does he get his clay? | The eastern bank of the river | From the east bank of the river. | 1 | East bank is equivalent to eastern bank. |
| 5 | How many jars were ordered? | 120 | 120 jars. | 1 | Exact quantity match. |
| 6 | What colour were the jar handles to be? | Blue | The text doesn't give a colour for the handles. It says only that the jars were blue and had handles. | 0 | Expected blue, but the answer denies that the handle colour is given. |
| 7 | What was the delivery deadline? | Before the spring festival | Before the spring festival. | 1 | Exact match. |
| 8 | How many jars fit in his old kiln at once? | 15 | Fifteen. | 1 | Fifteen matches 15. |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr | In Wadi al-Sidr. | 1 | Exact location match. |
| 10 | What is his daughter's name? | Layla | Layla. | 1 | Exact name match. |
| 11 | Who helped build the second kiln? | The neighbour, a blacksmith | His neighbour, the blacksmith. The text says Layla advised him to get the blacksmith's help in building the second kiln. | 1 | Identifies the neighbour, a blacksmith, as expected. |
| 12 | How long did the work take? | 40 days | Forty days of continuous work. | 1 | Forty days matches 40 days. |
| 13 | How many jars broke during firing? | 3 | Three. | 1 | Three matches 3. |
| 14 | What did he do about the broken jars? | Made three larger jars and gave them to the merchant as thanks | He made three replacement jars, larger than the originals, and gave them to the merchant as a gift to thank him for his patience. | 1 | Matches making three larger jars and giving them to the merchant as thanks. |

## Restoration

Judge: 6/10 — معظم النص مطابق، لكن توجد زيادة افتتاحية مكررة وتبديل جوهري بين التاجر وصاحب النزل، كما تغيّرت فكرة بناء الفرن الثاني إلى استخدام فرن الجار مع نفي ضرورة البناء.  
Similarity to the original: 85% characters, 86% words

| Original | Restored |
|---|---|
| جاءه تاجر | جاءه صاحب نزل كبير |
| من صاحب نزل كبير | من تاجر |
| أن يستعين بجاره الحداد في بناء فرن ثان | أن بناء فرن ثان ليس ضروريا |
| في بناء فرن ثان | بفرن جاره الحداد |
| — | جبل تكسوه أشجار الزيتون عاش رجل يدعى سالم بن عبد الرحيم |
| — | ويحتاج إلى السفر إليه |

Restored:

> جبل تكسوه أشجار الزيتون... عاش رجل يدعى سالم بن عبد الرحيم في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، وكان يعمل في صناعة الفخار منذ بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء جاءه صاحب نزل كبير من المدينة يحمل رسالة من تاجر، يطلب فيها مئة وعشرين جرة زرقاء ذات مقابض، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع في المرة الواحدة لأكثر من خمس عشرة جرة، كما أن الحجر الذي يعطي اللون الأزرق نادر لا يوجد إلا في وادي السدر، ويحتاج إلى السفر إليه.
>
> غير أن ابنته ليلى أشارت إلى أن بناء فرن ثان ليس ضروريا، فبإمكانه أن يستعين بفرن جاره الحداد، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

Original:

> في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

## Answer reply

```
1. Salim ibn Abd al-Rahim.
2. At twelve.
3. His grandfather.
4. From the east bank of the river.
5. 120 jars.
6. The text doesn't give a colour for the handles. It says only that the jars were blue and had handles.
7. Before the spring festival.
8. Fifteen.
9. In Wadi al-Sidr.
10. Layla.
11. His neighbour, the blacksmith. The text says Layla advised him to get the blacksmith's help in building the second kiln.
12. Forty days of continuous work.
13. Three.
14. He made three replacement jars, larger than the originals, and gave them to the merchant as a gift to thank him for his patience.
```

## Restore reply

```
جبل تكسوه أشجار الزيتون... عاش رجل يدعى سالم بن عبد الرحيم في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، وكان يعمل في صناعة الفخار منذ بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.

وفي صباح أحد أيام الشتاء جاءه صاحب نزل كبير من المدينة يحمل رسالة من تاجر، يطلب فيها مئة وعشرين جرة زرقاء ذات مقابض، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع في المرة الواحدة لأكثر من خمس عشرة جرة، كما أن الحجر الذي يعطي اللون الأزرق نادر لا يوجد إلا في وادي السدر، ويحتاج إلى السفر إليه.

غير أن ابنته ليلى أشارت إلى أن بناء فرن ثان ليس ضروريا، فبإمكانه أن يستعين بفرن جاره الحداد، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.
```
