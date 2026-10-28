# original_text — 10-dotless — anthropic/claude-sonnet-5.5

Date: 2026-10-24  
Answers: 12.5/14  
Restoration: 8/10 (99% characters, 98% words)  
Scored by: openai/gpt-5.6-terra  
Prompt: `experiments/original_text/10-dotless/original_text.10-dotless.prompt.txt`

## Answers

| Q | Question | Expected | anthropic/claude-sonnet-5.5 | Score | Judge's reason |
|---|---|---|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim | Salim ibn Abd al-Rahim (سالم بن عبد الرحيم). | 1 | Exact name given. |
| 2 | At what age did he start making pottery? | 12 | He started at age eighteen. | 0 | Says eighteen instead of 12. |
| 3 | Who taught him the craft? | His grandfather | His grandfather taught him. | 1 | Matches the expected answer. |
| 4 | Where does he get his clay? | The eastern bank of the river | He gets it from the eastern bank of the river. | 1 | Matches the expected location. |
| 5 | How many jars were ordered? | 120 | 120 jars were ordered. | 1 | Correct number of jars. |
| 6 | What colour were the jar handles to be? | Blue | Blue. | 1 | Correct colour. |
| 7 | What was the delivery deadline? | Before the spring festival | They had to be delivered before the spring festival (عيد الربيع). | 1 | Matches the deadline. |
| 8 | How many jars fit in his old kiln at once? | 15 | Fifteen jars at most. | 1 | Correct kiln capacity. |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr | It is found only in Wadi al-Sidr. | 1 | Matches the expected location. |
| 10 | What is his daughter's name? | Layla | Layla (ليلى). | 1 | Correct daughter's name. |
| 11 | Who helped build the second kiln? | The neighbour, a blacksmith | The blacksmith. The word before "الحداد" is undotted and ambiguous, so I can't tell whether it means his trade, carpentry or his skill. Layla herself went to the valley to fetch the stone. | 0.5 | Identifies a blacksmith but omits that he was the neighbour; includes irrelevant unsupported detail. |
| 12 | How long did the work take? | 40 days | Forty days of continuous work. | 1 | Correct duration. |
| 13 | How many jars broke during firing? | 3 | Three jars broke. | 1 | Correct number broken. |
| 14 | What did he do about the broken jars? | Made three larger jars and gave them to the merchant as thanks | He made three larger jars to replace them and gave them to the merchant as a gift, thanking him for his patience. | 1 | Matches: he made three larger jars and gave them to the merchant as thanks. |

## Restoration

Judge: 8/10 — النص مطابق في معظمه، مع أخطاء قليلة في نوع الأشجار والعمر وعبارة الاستعانة بالحداد، دون فقدان الفكرة العامة.  
Similarity to the original: 99% characters, 98% words

| Original | Restored |
|---|---|
| الزيتون | الصنوبر |
| الثانية | الثامنة |
| بجاره | بتجارة |

Restored:

> ًفي قرية صغيرة تقع على سفح جبل تكسوه أشجار الصنوبر، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثامنة عشرة من عمره. وورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بتجارة الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

Original:

> في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

## Answer reply

```
1. Salim ibn Abd al-Rahim (سالم بن عبد الرحيم).
2. He started at age eighteen.
3. His grandfather taught him.
4. He gets it from the eastern bank of the river.
5. 120 jars were ordered.
6. Blue.
7. They had to be delivered before the spring festival (عيد الربيع).
8. Fifteen jars at most.
9. It is found only in Wadi al-Sidr.
10. Layla (ليلى).
11. The blacksmith. The word before "الحداد" is undotted and ambiguous, so I can't tell whether it means his trade, carpentry or his skill. Layla herself went to the valley to fetch the stone.
12. Forty days of continuous work.
13. Three jars broke.
14. He made three larger jars to replace them and gave them to the merchant as a gift, thanking him for his patience.
```

## Restore reply

```
ًفي قرية صغيرة تقع على سفح جبل تكسوه أشجار الصنوبر، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثامنة عشرة من عمره. وورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.

وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.

غير أن ابنته ليلى أشارت عليه أن يستعين بتجارة الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.
```
