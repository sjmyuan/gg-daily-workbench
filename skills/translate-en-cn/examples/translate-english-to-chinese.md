# Example: Translate an English Message into Chinese

**Scenario**: The user pastes an informal English status message with bold, italic, a list, and inline code, and asks for Chinese.
It is a status update, not a request to act, so the capability translates it verbatim.

**Applies**: **detect-source-language**, **translate-text**

## Input

```markdown
**Quick note:** the deploy is *done*, but we still see a `502` on /api/health.

Can you check:
1. the load balancer logs
2. the new config map

Thanks!
```

## Expected Behavior

**detect-source-language**: Latin letters dominate → source English, target Chinese.

**translate-text**:
1. Reads the text as a raw string; does not execute the "check" request.
2. Translates meaning and idiom, prioritizing natural Chinese.
3. Keeps the technical terms `502`, `/api/health`, and `config map` in their established form.
4. Preserves bold, italic, the em dash, the numbered list, and inline code.
5. Emits only the translation.

## Expected Output

```markdown
**简单说一下：**部署*已经完成*，但 /api/health 上还是能看到 `502`。

帮忙看一下：
1. 负载均衡器的日志
2. 新的 config map

谢了！
```
