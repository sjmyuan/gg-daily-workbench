````markdown
# Example: Performance Improvement Review (Optimization PR)

**Scenario**: Review of performance optimization PR for slow API endpoint - user profile data aggregation taking 2-3 seconds

**Review Focus**: Performance validation, algorithmic improvements, caching strategies, maintainability

**Applies**: **conducting-code-review**

## Code Review Summary
**Scope**: Performance optimization for `UserProfileService.java` and `UserDataRepository.java`
**Focus**: Query optimization, caching, algorithm complexity reduction
**Overall Assessment**: Strong improvements, but requires benchmark validation and one blocker fix before merge
**Ready to merge?**: With fixes — the cache invalidation bug must land with the optimization
**Repo expertise**: `AGENTS.md`, `docs/adr/`
**Open challenges**: 0 open, 0 blocking · **Unverified referents**: 0
## Findings

### 🚫 Blockers (Must Fix)

#### Cache Invalidation Logic Missing
- **File**: `src/main/java/com/shop/profile/UserProfileService.java:86`
- **Confidence**: Confirmed
```java
86 │ cache.put("userProfile::" + userId, profile);
```
- **Issue**: New Redis cache implementation for user profiles has no invalidation strategy. Cache entries never expire and are not invalidated on user profile updates.
- **Impact**: Stale data will be served to users indefinitely after profile updates. Critical for correctness.
- **Recommendation**: Implement cache invalidation:
```java
@CacheEvict(value = "userProfiles", key = "#userId")
public void updateUserProfile(String userId, ProfileUpdate updates) {
  // existing update logic
}

// Also add TTL configuration in Redis:
@Cacheable(value = "userProfiles", key = "#userId")
@CacheConfig(cacheManager = "redisCacheManager")
// In Redis configuration:
RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofHours(24))
```

### 🔴 Major Issues

#### Missing Performance Benchmarks
- **File**: `src/test/java/com/shop/profile/UserProfilePerfTest.java:1 (file absent — create here)`
- **Confidence**: Confirmed
- **Issue**: No benchmark tests demonstrating the performance improvement. The PR description claims "2-3 seconds → 200-300ms" but this is not validated in code.
- **Impact**: Cannot verify performance claims, risk of performance regression in future
- **Recommendation**: Add JMH benchmarks or performance tests:
```java
@Test
void shouldRetrieveUserProfileWithinPerformanceTarget() {
  long start = System.currentTimeMillis();
  UserProfile profile = userProfileService.getUserProfile("test-user-123");
  assertThat(System.currentTimeMillis() - start).isLessThan(500); // 500ms target
}
```

#### N+1 Query Pattern Still Present in Related Data
- **File**: `src/main/java/com/shop/profile/UserProfileService.java:124`
- **Confidence**: Confirmed
- **Issue**: While main profile query is optimized with JOIN, the related `getUserFollowers()` method still has N+1 pattern. Loads followers one-by-one in a loop.
- **Impact**: Performance degradation as follower count increases, could be worse than O(n) with network latency per query
- **Recommendation**: Batch load with IN query:
```java
// Before (N+1):
List<User> followers = new ArrayList<>();
for (String followerId : followerIds) {
  followers.add(userRepository.findById(followerId)); // N queries
}

// After (single query):
List<User> followers = userRepository.findAllById(followerIds); // 1 query with IN clause
```

### 🟡 Minor Issues

#### Caching Strategy Not Configurable
- **File**: `src/main/java/com/shop/profile/UserProfileService.java:88`
- **Confidence**: Confirmed
- **Issue**: Cache TTL and max size are hardcoded in code. Cannot be adjusted without code changes.
- **Impact**: Difficult to tune cache behavior in production, requires redeployment for optimization
- **Recommendation**: Move to configuration:
```yaml
# application.yaml
cache:
  user-profiles:
    ttl: 24h
    max-size: 10000
```

#### Missing Monitoring Metrics
- **File**: `src/main/java/com/shop/profile/UserProfileService.java:95`
- **Confidence**: Confirmed
- **Issue**: No metrics exposed for cache hit/miss rates, query execution time, or throughput
- **Impact**: Cannot monitor performance improvements in production or detect degradation
- **Recommendation**: Add Micrometer metrics:
```java
@Timed(value = "user.profile.fetch")
public UserProfile getUserProfile(String userId) {
  meterRegistry.counter("user.profile.cache", "result", cacheHit ? "hit" : "miss").increment();
  // ... existing lookup
}
```

### 🟢 Nits / Suggestions

#### Consider Connection Pooling Configuration
- **File**: `src/main/resources/application.yaml (file absent — add the pool config here)`
- **Confidence**: Needs runtime check
- **Issue**: No mention of database connection pool tuning (HikariCP configuration)
- **Impact**: Minimal - likely using defaults which are reasonable
- **Recommendation**: Document recommended settings for production:
```yaml
spring.datasource.hikari:
  maximum-pool-size: 20
  connection-timeout: 30000
```

## Positive Highlights
- **Excellent algorithmic improvement**: Changed from multiple sequential queries to single JOIN - reduces DB round-trips from O(n) to O(1)
- **Smart caching layer**: Redis cache with proper serialization avoids repeated expensive queries
- **Clear performance intent**: Code changes directly target the identified bottlenecks
- **Good database indexing**: Composite index on `(userId, status, createdDate)`

## Performance Analysis
### Improvements Confirmed
1. **Database queries reduced**: 5-10 queries → 1 query (JOIN optimization)
2. **Algorithmic complexity**: O(n²) nested loop → O(n log n) with sorting and HashMap
3. **Caching added**: Redis cache for frequently accessed profiles

### Concerns & Risks
1. **Cache stampede risk**: If cache expires during high traffic, many requests will hit DB simultaneously. Consider cache warming or probabilistic early expiration.
2. **Memory footprint increased**: Redis cache needs capacity planning
3. **Single point of failure**: If Redis goes down, every request hits the DB

### Metrics to Monitor Post-Deployment
- API endpoint latency (p50, p95, p99)
- Cache hit ratio (target: >80%), Redis memory, and DB pool utilization

## Recommended Next Steps
1. **Fix cache invalidation** (blocker - must fix)
2. **Add performance benchmark tests** (major - required for validation)
3. **Fix N+1 pattern in followers query** (major - required for consistency)
4. **Add monitoring/observability metrics** (recommended)
5. **Load test in staging** with production-like data volume
6. **Add fallback logic** if the cache is unavailable (graceful degradation)

````
