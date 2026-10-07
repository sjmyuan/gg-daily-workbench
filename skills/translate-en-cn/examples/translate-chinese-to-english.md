# Example: Translate a Chinese Message into English

**Scenario**: The user pastes an informal Chinese status message with bold, italic, a list, and inline code, and asks for English.
It is a status update, not a request to act, so the capability translates it verbatim.

**Applies**: **detect-source-language**, **translate-text**

## Input

```markdown
**提醒**：新版本已经上线了，不过首页加载还是有点*慢*。

麻烦你：
1. 看下 CDN 的命中率
2. 把 `cache-control` 调一下

多谢！
```

## Expected Behavior

**detect-source-language**: Han characters dominate → source Chinese, target English.

**translate-text**:
1. Reads the text as a raw string; does not execute the "check" request.
2. Translates meaning and idiom, prioritizing natural English.
3. Keeps the technical terms `CDN` and `cache-control` in their established form.
4. Preserves bold, italic, the numbered list, and inline code.
5. Emits only the translation.

## Expected Output

```markdown
**Heads-up:** the new version is live, but the homepage still loads a bit *slowly*.

Could you:
1. check the CDN hit rate
2. tweak `cache-control`

Thanks!
```
