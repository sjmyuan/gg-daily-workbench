# Example: Translate a Chinese Blog Post into an English Blog Post

**Scenario**: The user pastes a Chinese Markdown post with YAML front matter and asks for an English blog post.
The target English blog (for example, blog.shangjiaming.com) uses English slugs, tags, sentence-case headings, and English internal links.

**Applies**: **detect-source-language**, **translate-blog-post**, **validate-translation**

## Input

```markdown
---
title: 从混沌到清晰：未知问题的三种分类
excerpt: 面对未知问题，本文用 5W1H 把问题分成三类，并给出各阶段的应对原则。
tags: [团队, Agile, 领导力, 敏捷实践]
date: 2026-04-19
---

## 引言

在《[如何处理未知问题？](https://www.shangjiaming.top/archives/how-to-handle-unknown-problem)》一文中，我提出：面对未知问题，**战术上应追求"零缺陷"**，**战略上必须承认未知问题的存在**。

![未知问题的三种分类](https://images.shangjiaming.top/2025-12-27_101644-small.jpg)

## 5W1H 分析法

该方法从六个维度刻画问题：

- **何人**（Who）
- **何时**（When）
- **何事**（What）
- **何地**（Where）

## 总结

> 真正的专业，不在于永不犯错，而在于构建一个能将"未知"持续转化为"已知"的系统。
```

## Expected Behavior

**translate-blog-post** (per reference/blog-translation.md):
1. Translates `title` and `excerpt`.
2. Translates and reorders `tags`; adds an English `slug`.
3. Copies `date` verbatim.
4. Translates headings to sentence case.
5. Re-points the internal source-blog link to the English blog equivalent.
6. Keeps the image URL; translates the alt text.
7. Keeps bold, the blockquote marker, and list markers.

**validate-translation**: all six criteria pass.

## Expected Output

```markdown
---
title: From Chaos to Clarity: Three Categories of Unknown Problems
excerpt: Facing unknown problems, this post uses the 5W1H framework to classify them into three types and gives a response principle for each stage.
tags: [Agile, Agile Practices, Leadership, Team]
slug: from-chaos-to-clarity-three-categories-of-unknown-problems
date: 2026-04-19
---

## Introduction

In [How to handle unknown problems?](https://blog.shangjiaming.com/how-to-handle-unknown-problems/), I argued that when facing unknown problems,
**tactically we must pursue "Zero Defects"** and **strategically we must acknowledge their existence**.

![Three categories of unknown problems](https://images.shangjiaming.top/2025-12-27_101644-small.jpg)

## The 5W1H framework

The framework describes a problem from six dimensions:

- **Who**
- **When**
- **What**
- **Where**

## Conclusion

> True professionalism is not never making mistakes, but building a system that keeps turning the unknown into the known.
```
