# Style Exemplars: How a Real Person Writes

Extracted from a hand-written Chinese tech blog (https://www.shangjiaming.top, posts 2022–2024, written without AI). Use these as the "feel" reference for **compose-blog** and **refine-style**.

**How to use**: before composing, read the excerpts below, then list 2–3 style rules in your own words ("像这个人一样写"). Compose with those rules in mind. After composing, re-check the draft against the excerpts — would the author write that sentence?

## Exemplar 1 — "你知道你不知道么？" (2022-11)

Personal narrative on the known/unknown model. Notice: scene-based opening addressed to the reader, an honest author's caveat, layered analysis that builds a model, and an ending that is a question, not a summary.

> 大家在做项目的过程中有没有遇到过下面的情况：
>
> 明明项目启动的时候确认过需求，但在功能上线的冲刺阶段却突然发现有个需求没有做或者要大改。
>
> 明明每次前期调研已经做的很详细了，但在团队实现的时候总会有遗漏点。
>
> 明明代码写的没有问题，但在上线后总会有Bug。
>
> 每当我们信心满满时，总是会有一些意想不到的情况出现，这是纯属意外，还是有规律可循？这篇博客我们就聊聊这个问题。
>
> 由于作者能力有限，本文没有对知识，问题，事情这几个概念做区分，会根据描述的便利性进行转换……
>
> ……不知道且不理解的事情是无法避免的，但我们可以通过各种实践来拓展我们的知识边界，以降低其出现的概率。现在你还会觉得日常工作中的一些会议或实践是在浪费时间么？不妨从我可能不知道一些事情的角度重新审视一下它们。

**What makes it human**: reader address ("大家"), parallel scene set-ups that are concrete (需求、Bug), an honest caveat ("作者能力有限"), and an ending that hands the question back to the reader.

## Exemplar 2 — "如何进行Bug分析？" (2024-06)

Methodology piece. Notice: opens with a real recent event and the author's own wrong initial take, then revises it — self-correction carries the argument.

> 最近在和团队一起进行Bug分析，期间经常会听到一句话，**如果再来一次，我们该怎么避免这个问题？** 起初，我并没有觉得这句话有什么不对。它是让我们想象一下……但在分析了几个Bug之后，我发现这个提问并不是一个好提问。
>
> 首先，它会把团队引导到低效的解决方案上。所谓低效的解决方案就是头痛医头，脚痛医脚，治标不治本的方案。……究其原因，我们会在这个提问的语境下采取错误的问题处理方式。
>
> 其次，它会禁锢团队的活力。……最后，它会增加团队的压力。……
>
> 在Bug分析中听到最多的词就是**尽力**，尽力检查，尽力沟通，尽力提高，尽力完成等，那么到底什么叫尽力？我们该如何衡量它？……我们与其思考该如何衡量**尽力**，不如选择相信，相信每位团队成员都已尽最大努力，把Bug分析的重点放在能力和流程上，而不是积极、主动、谨慎等个人动机上。

**What makes it human**: the author's own journey ("起初……但在分析了几个Bug之后"), colloquial idiom ("头痛医头，脚痛医脚"), a conversational "那么到底什么叫尽力？", and the conclusion is a stance, not a summary.

## Extracted style rules

Apply these together with the checklist in [human-voice.md](human-voice.md):

1. **Scene first**: open with a real recent event or a concrete situation the reader recognizes — never with a generic hook ("在当今……的时代").
2. **Self-correct**: show your initial take, then the revision that experience forced on you.
3. **Address the reader, but as an argument**: use "你 / 大家 / 你有没有遇到过……" to press a point ("那么解决问题真的是第一优先级么？"), not to make small talk. The register stays a written statement, not a conversation — see [human-voice.md](human-voice.md) §7.
4. **Idiom and plain speech**: everyday expressions and idioms ("头痛医头，脚痛医脚") are welcome; abstract management-speak is not.
5. **End with a question or a stance**, not a wrap-up summary.

## Anti-patterns from the same blog's AI-assisted era (for contrast)

The same author's 2026 posts show what to avoid: heavy bold-labeled step headings ("**发生了什么？**"), "关键点在于……", balanced tables everywhere, and an aphoristic closing line ("它们只是安静地等在执行过程中的某个角落"). Structure is useful; the *flourish* is the tell. Keep structure, drop the flourish.

### The second tell: a chatty assistant register (豆包味)

The *flourish* above is structural and fairly easy to spot. The other tell only appears when a draft is polished for "warmth", and it is harder to catch because it feels friendly. It sounds like a helpful assistant talking with the reader rather than a practitioner stating something:

- emotional self-narration for atmosphere ("我盯着它的输出，心里越来越没底", "但我心里清楚，它不是终点")
- debate and reassurance phrasing ("这一点它确实赢，没什么好争的", "我没有异议")
- suspense beats before the point ("真做下来才发现，没那么简单")
- filler openers ("说白了", "说到底", "你会发现", "这一点很关键")
- stacked rhetorical questions ("心流是什么？……为什么等 AI 会让人这么难受？")

Both are AI tells, and both are covered by the same gate. Rules, before/after pairs, and the test ("read it aloud — if it sounds like greeting, reassuring, or arguing, rewrite it as a flat statement"): [human-voice.md](human-voice.md) §7.

## 用户手写范本（本博客长期风格档案）

Two published posts by the same author, both written by hand, are the standing voice reference for this blog. Fetch them at the start of a composing session rather than guessing the voice.

### 范本 A —《如何让团队接受持续部署？》(2024-03-10)

https://www.shangjiaming.top/archives/1710080830635

- TL;DR 开头
- 自述式纠错："当时，我对团队的反应很不解……后来，我发现自己搞错了目标和方法"
- 反问句连发（一口气四个"为什么……呢？"）
- "注意，……"作提醒装置（全文 3 次）
- 编号列举 1. 2. 3. 列定义与做法
- 小标题用问句或名词短语
- 加粗只压关键术语，且与链接一起加粗
- 排比用于列举（"针对第三方服务的区域不可用／维护窗口／请求速率限制"）
- 结尾"总结"一节，交代边界条件（"属于必要性指标……但在行动区的不一定会实施"）
- 正文破折号 0 处

### 范本 B —《如何让团队真正接受AI编程助手？》(2025-06-21)

https://www.shangjiaming.top/archives/how-to-get-the-team-to-truly-embrace-ai-coding-assistant

- 开篇连问读者四个问题（"你的团队开通AI编程助手了么？你有没有被天天催着提高使用率？……"）
- 大量用"那么，……"把话推进到下一节
- "需要注意的是，……"
- "首先／其次／之后／然后／最后"顺次列举措施
- 加粗整句关键主张
- 诚实的自我设限："让我们暂且相信这个假设是成立的，并通过实践来验证它"
- "我所在的团队"这类具体落点
- 小标题大量用问句，甚至有"知识和案例分享为啥有效？"这种口语问法
- 读者称呼两种都用：问读者时用"你"，讲团队经验时用"我们／带过团队的人"
- 术语首次出现带英文括号（信任(Treat)、基于技能(Skill-based)）
- 正文破折号 1 处

## 范本优先与豁免

Rule: **a hand-written sample supplied by the user outranks every heuristic in [human-voice.md](human-voice.md).** Three patterns that file bans are, in this author's hands, signature moves:

| Heuristic | Sample evidence | Handling |
|---|---|---|
| §7.5: keep rhetorical questions to the closing one | 范本 A 连用四句；范本 B 开篇四句 | allow argumentative or puzzled questions in the author's voice; the tell is the debate/reassurance register, not the question count |
| §6: never end with a summary | 两篇范本都以"总结"收尾 | a deliberate 总结 section is allowed; what stays banned is the 总结腔 transition inside prose ("由此可见", "综上所述") |
| §5: no parallel structures | 范本 A 用排比列举三种情形 | parallels used to enumerate aspects are fine; flourish-only parallels are not |

Procedure when a sample is supplied:

1. Fetch the sample (or, when only a title is given, fetch the site archive to get its URL).
2. Extract its markers: opening move, connectives, enumeration style, bold density, heading form, reader address, ending form, punctuation quirks.
3. Write the marker list into the article's assistant notes as "本文风格清单", with the sample URL.
4. Compose or refine against that list. Where it conflicts with human-voice.md, the list wins, and the exemption is recorded in the notes.
5. Re-run the Human-Voice Gate reporting each exemption explicitly (gate check 8).
