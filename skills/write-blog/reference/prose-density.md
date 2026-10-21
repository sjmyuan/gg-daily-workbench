# Prose Density: Writing Loose Without Sounding Like a Chatbot

Used by **compose-blog** and **refine-style** together with [human-voice.md](human-voice.md).
That file bans the chatty-assistant register; this one bans the opposite failure, **over-compression**.
A draft can clear every blacklist and still read as AI: every sentence carries a claim, every paragraph lands on a conclusion, nothing rambles.

## 1. Compression tells

| Tell | Looks like | Why it reads as AI |
|---|---|---|
| One claim per sentence | 上下文是脏的。AI 读不懂。所以改不对。 | 每句都在干活，没有一句在解释 |
| Abstract noun standing alone | 上下文缺失导致准确率下降 | 没有画面：谁、什么时候、改了什么 |
| No long breath | 全篇句子 15–30 字，长度齐整 | 人写长句会一口气带三四个分句 |
| Conclusion-first paragraph | 每段首句就是判断，后面全是支撑 | 人常常先铺垫，再落到判断 |
| Zero restatement | 一个意思只说一遍 | 人会换个说法再说一遍，怕对方没跟上 |

## 2. Deletion test (the only gate)

Ask of every extra sentence: **删掉它，读者少知道什么？**

| Extra words | 读者少知道什么 | Verdict |
|---|---|---|
| "也就是说，它只读得到你给它的那部分" | 一句更直白的同义解释 | 保留，这是换说法重述 |
| "我们当时试了两周，前后换了三个方案" | 过程、时间、代价 | 保留，这是有信息的啰嗦 |
| "我盯着它的输出，心里越来越没底" | 只少了情绪 | 删（human-voice §7.1） |
| "说白了就是上下文不干净" | 只少了口头的热度 | 删（§7.4） |
| "这一点很关键" | 什么都不少 | 删（§7.4） |

Rule: §7 stays in force unchanged. This file only licenses words that survive the deletion test.

## 3. Density floors (measured on the full body of 范本 A and 范本 B)

Whole-article body, headings / lists / images / captions excluded. An earlier version of this table sampled 8 loose paragraphs and set the paragraph median at 131; the full-body count is 99 and 86, so that floor was wrong and has been recalculated here.

| Metric | 范本 A | 范本 B | Floor for a draft |
|---|---|---|---|
| 句子平均字数 | 41.5 | 48.1 | ≥ 40 |
| 句子中位字数 | 40 | 45 | ≥ 38 |
| 句长标准差 | 19.8 | 25.1 | ≥ 19 |
| ≥60 字的句子 | 19% | 25% | ≥ 18% |
| ≤12 字的句子 | 6% | 4% | ≤ 15% |
| 段落中位字数 | 99 | 86 | ≥ 90 |
| 正文破折号 | 0 | 1 | ≤ 2 |

**Watch the median and the tail, not the mean.** A draft can match the mean (41.7 vs 41.5) while its median sits 7 characters low and its long sentences are half as frequent — that draft is the one that reads as AI, and the mean hides it.

**Floors are not quotas.** A section that cannot reach them with real material is a gap, not a padding job:
ask the author for the missing process, example, or number. Never add adjectives, never invent a scene.

## 4. Six expansion moves (add words that carry content)

1. **Replay the reasoning**: 一开始我以为是 X → 后来发现是 Y → 原因是 Z. Do not ship the conclusion alone.
2. **Turn the abstract noun into a scene**: 人 + 时间 + 动作. "命名不统一" → "同一个函数在三年前的代码里叫 A，去年重构后叫 B，新人两个名字都搜一遍".
3. **One example per claim**, concrete enough to picture. 判断值一句，例子值三句。
4. **Say what it means**: 补一句"所以对我们来说，真正要改的是……"。
5. **Restate once per section** in plainer words (也就是说／换句话说). Not twice.
6. **State the boundary**: 这条在什么情况下不成立、例外是什么. 人写经验会顺手交代边界，AI 不会。

## 5. Two budgets besides length

Length is measurable, and a model optimizes whatever is measured. These two are what a length-compliant draft still fails.

### 5.1 One deep dive per section (铺开段)

Every section carries at least one paragraph that goes deeper than the argument needs: a file's actual contents, a real status list, a timeline, a pile of numbers, a full quote. Test: **delete it — is the argument still intact?** If yes, it is a deep dive, keep it. If no, the section is still written at minimum size.

范本 A spends two screens on testing strategy (four quadrants, nine practices, a 5-minute budget). 范本 B spends a whole section on the SRK model and its three error types. Neither is required by the thesis.

### 5.2 One verifiable quantity per section (可核对的量)

At least one number, file name, command, status symbol, or quoted sentence the reader could check in their own repo. "哪一步完成、哪一步在做、哪一步失败" becomes the actual `⏳ 🔄 ✅ ❌ 🚫` list.

A judgement ("可逆的自己定，不可逆的先问") is not a quantity until it lands on a verb list: 提交、推送、改 PR 描述.

**Never fabricate one.** A number or quote the author did not supply is a fabricated anchor (human-voice §4): ask for it, or mark a gap.

## 6. Colloquial ladder

| Register | Examples | Verdict |
|---|---|---|
| 内容型口语 | 也就是说／换句话说／这么一来／后来／结果／当时／其实／举个例／万一 | 保留，删掉有信息损失 |
| 论证型反问（作者本色） | 那么，我们真的需要……么？ | 保留，human-voice §7.5 |
| 温度型口语 | 说白了／说实话／你会发现／这一点很关键 | 删，删掉无信息损失 |
| 情绪型口语 | 心里没底／急得要死／写到这我想收个尾 | 删，human-voice §7.1／§7.3 |

判别只用一条：把词换成书面说法，句子还成立吗？换掉后信息不变的是温度，换不掉的才是口语的内容。

## 7. Procedure while composing

1. Dictate first: write each section as if explaining it to a colleague out loud. Allow repetition, detours, and half-sentences.
2. Then edit for the written register: remove chatty fills, keep the explanatory slack.
3. Measure the draft against the §3 floors; record the numbers in the assistant notes.
4. Where a section falls short, apply a §4 move or mark a gap — never pad.

## 8. Gate coverage

The Human-Voice Gate in [human-voice.md](human-voice.md) §8 carries this file: check 2 measures the §3 floors, check 9 runs the deletion test, check 10 checks for one deep dive and one verifiable quantity per section.
Report the four density numbers by name: paragraph median, mean sentence length, count of ≥ 60-character sentences, share of ≤ 12-character sentences.
