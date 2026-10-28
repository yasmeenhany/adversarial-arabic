# original_text — 3-root-1 — anthropic/claude-sonnet-5.5

Date: 2026-10-24  
Answers: 5.5/14  
Restoration: 2/10 (77% characters, 54% words)  
Scored by: openai/gpt-5.6-terra  
Prompt: `experiments/original_text/3-root-1/original_text.3-root-1.prompt.txt`

## Answers

| Q | Question | Expected | anthropic/claude-sonnet-5.5 | Score | Judge's reason |
|---|---|---|---|---|---|
| 1 | What is the potter's full name? | Salim ibn Abd al-Rahim | Salim bin Abd al-Rahim (سالم بن عبد الرحيم). | 1 | “bin” and “ibn” are equivalent; full name matches. |
| 2 | At what age did he start making pottery? | 12 | The text doesn't say. | 0 | It does not give the expected age of 12. |
| 3 | Who taught him the craft? | His grandfather | This is unclear. The text mentions someone who taught him how to extract and treat the clay, but the word is garbled and gives no name. | 0 | It does not identify his grandfather as the teacher. |
| 4 | Where does he get his clay? | The eastern bank of the river | He takes it from a bank (ضفة), described as "النقر الضرعية". The wording is obscure. | 0.5 | It identifies a riverbank/bank but does not specify the eastern bank. |
| 5 | How many jars were ordered? | 120 | 190 jars. | 0 | It gives 190 instead of 120. |
| 6 | What colour were the jar handles to be? | Blue | The text doesn't say clearly. The handles are called "شحناء", which is unclear and not a colour. | 0 | It does not identify the handles as blue. |
| 7 | What was the delivery deadline? | Before the spring festival | Before "نفول فيل الربيع", a garbled phrase that seems to mean before a point in spring. No exact date is given. | 0.5 | It indicates a deadline sometime before spring but does not identify the spring festival. |
| 8 | How many jars fit in his old kiln at once? | 15 | The text is garbled here ("خمس سلمه هزه"), so I can only say it is about five. The exact number is not clear. | 0 | It says about five rather than the expected 15. |
| 9 | Where is the rare stone for the blue colour found? | Wadi al-Sidr | The text doesn't mention a rare stone or a blue colour. | 0 | It does not mention Wadi al-Sidr. |
| 10 | What is his daughter's name? | Layla | Laythi (ليثي). | 0 | It gives Laythi rather than Layla. |
| 11 | Who helped build the second kiln? | The neighbour, a blacksmith | His neighbour the blacksmith (الحداد). | 1 | It correctly identifies the neighbour who was a blacksmith. |
| 12 | How long did the work take? | 40 days | Forty days. | 1 | It correctly states forty days. |
| 13 | How many jars broke during firing? | 3 | Three jars. | 1 | It correctly states three jars. |
| 14 | What did he do about the broken jars? | Made three larger jars and gave them to the merchant as thanks | He made three replacement jars, larger and better than the broken ones, and sent them off. The wording is somewhat unclear. | 0.5 | It says he made three larger replacement jars, but omits that he gave them to the merchant as thanks. |

## Restoration

Judge: 2/10 — معظم الكلمات والمعلومات الأساسية استبدلت بكلمات مختلفة وغير مترابطة، مع بقاء بعض البنية العامة وأجزاء من الفقرة الأخيرة مثل سالم والحداد وأربعين يوما وانكسار ثلاث قطع.  
Similarity to the original: 77% characters, 54% words

| Original | Restored |
|---|---|
| قرية | ثنية |
| صغيرة | حثيثة |
| أشجار | أفخاذ |
| عاش | جلس |
| صناعة الفخار | حضانة الظلام |
| ورث | طوى |
| جده | شيخه |
| تاجر | رسول |
| مئة وعشرين جرة | مئة وتسعين هزة |
| عيد الربيع | نفوق فيل الربيع |

Restored:

> في ثنية حثيثة تطل على سفح جبل تكسوه أفخاذ الزيتون، جلس سالم بن عبد الرحيم، وكان يعمل في حضانة الظلام منذ أن منح الصباح تبغه من سهده. وطوى سالم هذه الرزمة عن شيخه، الذي علمه كيف يغتال الزيت من ضفة النقر الضرعية، وكيف يدمنه بالماء والنار حتى يصير لينا مطواعا.
>
> وفي أيام الغذاء الأليمة، جاءه رسول من الطليعة يحمل خزامة من كامل بحث متين، يطلب فيها مئة وتسعين هزة ذات مصاعد شحناء، على أن تصفد قبل نفوق فيل الربيع. تشتت سالم في الرعاية، لأن فحمه الخضير لا يكفي إلا لأصلد من خمس وسبعين هزة في الحلة الواقدة، كما أن اللوح الأربع يحتاج إلى هرم فاضح لا يولم إلا في أواسط الشرش.
>
> غير أن ابنته ليثي أشارت عليه أن يستعين بجاره الحداد في حانوته الثاني، وتطوعت هي بالذهاب إلى الوالي لنقص الشرج. وبعد أربعين يوما من العمل المتواصل، اكتملت النكات كلها إلا ثلاثا انكسرت أثناء العتمة، فعوضها سالم بثلاث نجام أكبر نفعا، وأهداها للسابق ردا له على قنصه.

Original:

> في قرية صغيرة تقع على سفح جبل تكسوه أشجار الزيتون، عاش رجل يدعى سالم بن عبد الرحيم، وكان يعمل في صناعة الفخار منذ أن بلغ الثانية عشرة من عمره. ورث سالم هذه الحرفة عن جده، الذي علمه كيف يختار الطين من ضفة النهر الشرقية، وكيف يعجنه بالماء والرماد حتى يصير لينا مطواعا.
>
> وفي صباح أحد أيام الشتاء، جاءه تاجر من المدينة يحمل رسالة من صاحب نزل كبير، يطلب فيها مئة وعشرين جرة ذات مقابض زرقاء، على أن تسلم قبل حلول عيد الربيع. تردد سالم في البداية، لأن فرنه القديم لا يتسع لأكثر من خمس عشرة جرة في المرة الواحدة، كما أن اللون الأزرق يحتاج إلى حجر نادر لا يوجد إلا في وادي السدر.
>
> غير أن ابنته ليلى أشارت عليه أن يستعين بجاره الحداد في بناء فرن ثان، وتطوعت هي بالسفر إلى الوادي لجلب الحجر. وبعد أربعين يوما من العمل المتواصل، اكتملت الجرار كلها إلا ثلاثا انكسرت أثناء الحرق، فصنع سالم بدلا منها ثلاث جرار أكبر حجما، وأهداها للتاجر شكرا له على صبره.

## Answer reply

```
1. Salim bin Abd al-Rahim (سالم بن عبد الرحيم).
2. The text doesn't say.
3. This is unclear. The text mentions someone who taught him how to extract and treat the clay, but the word is garbled and gives no name.
4. He takes it from a bank (ضفة), described as "النقر الضرعية". The wording is obscure.
5. 190 jars.
6. The text doesn't say clearly. The handles are called "شحناء", which is unclear and not a colour.
7. Before "نفول فيل الربيع", a garbled phrase that seems to mean before a point in spring. No exact date is given.
8. The text is garbled here ("خمس سلمه هزه"), so I can only say it is about five. The exact number is not clear.
9. The text doesn't mention a rare stone or a blue colour.
10. Laythi (ليثي).
11. His neighbour the blacksmith (الحداد).
12. Forty days.
13. Three jars.
14. He made three replacement jars, larger and better than the broken ones, and sent them off. The wording is somewhat unclear.
```

## Restore reply

```
في ثنية حثيثة تطل على سفح جبل تكسوه أفخاذ الزيتون، جلس سالم بن عبد الرحيم، وكان يعمل في حضانة الظلام منذ أن منح الصباح تبغه من سهده. وطوى سالم هذه الرزمة عن شيخه، الذي علمه كيف يغتال الزيت من ضفة النقر الضرعية، وكيف يدمنه بالماء والنار حتى يصير لينا مطواعا.

وفي أيام الغذاء الأليمة، جاءه رسول من الطليعة يحمل خزامة من كامل بحث متين، يطلب فيها مئة وتسعين هزة ذات مصاعد شحناء، على أن تصفد قبل نفوق فيل الربيع. تشتت سالم في الرعاية، لأن فحمه الخضير لا يكفي إلا لأصلد من خمس وسبعين هزة في الحلة الواقدة، كما أن اللوح الأربع يحتاج إلى هرم فاضح لا يولم إلا في أواسط الشرش.

غير أن ابنته ليثي أشارت عليه أن يستعين بجاره الحداد في حانوته الثاني، وتطوعت هي بالذهاب إلى الوالي لنقص الشرج. وبعد أربعين يوما من العمل المتواصل، اكتملت النكات كلها إلا ثلاثا انكسرت أثناء العتمة، فعوضها سالم بثلاث نجام أكبر نفعا، وأهداها للسابق ردا له على قنصه.
```
