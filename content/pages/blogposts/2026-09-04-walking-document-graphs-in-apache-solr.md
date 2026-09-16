Title: Walking Document Graphs in Apache Solr
category: solr/blogposts
summary: Solr can traverse multi-hop relationships already stored in the index — org charts, nested groups, product taxonomies — with the graph query parser. One hop is a join; the rest of the tree is a graph walk. Written by Prithvi S.
slug: walking-document-graphs-in-apache-solr
URL: blogposts/walking-document-graphs-in-apache-solr.html
save_as: blogposts/walking-document-graphs-in-apache-solr.html

# Walking Document Graphs in Apache Solr

Written by [Prithvi S](https://github.com/iprithv).

A surprising number of Solr indexes already contain a graph.

An employee document points at a manager. A group lists the groups it belongs to. A category records its parent. Those pointers are ordinary string fields, so they are easy to index and easy to ignore. Then a product question shows up: *all engineers under this VP*, *every document this nested group can see*, *the full subtree of Electronics*. A [join](https://solr.apache.org/guide/solr/latest/query-guide/join-query-parser.html) answers the one-hop version of that question. The recursive version is already built in: Solr's [`graph` query parser](https://solr.apache.org/guide/solr/latest/query-guide/other-parsers.html#graph-query-parser).

This post is a worked example of that parser. It is not a rewrite of the reference guide. The goal is to show a realistic schema, the `from`/`to` footgun that catches people coming from `{!join}`, and the cases where you should pick a different tool.

## One hop is a join. The tree is a graph.

Take a small org chart:

```
alice (CEO)
├── bob (Engineering Manager)
│   ├── dave (Engineer)
│   └── eve (Engineer, on leave)
└── carol (Design Manager)
    └── frank (Designer)
```

Each person is one Solr document. `id` is the person. `manager_id_s` is that person's pointer to their manager.

```json
[
  {"id":"alice", "name_s":"Alice", "title_s":"CEO",              "dept_s":"exec",    "status_s":"active"},
  {"id":"bob",   "name_s":"Bob",   "title_s":"Engineering Manager","dept_s":"eng",    "status_s":"active",  "manager_id_s":"alice"},
  {"id":"carol", "name_s":"Carol", "title_s":"Design Manager",    "dept_s":"design",  "status_s":"active",  "manager_id_s":"alice"},
  {"id":"dave",  "name_s":"Dave",  "title_s":"Engineer",          "dept_s":"eng",     "status_s":"active",  "manager_id_s":"bob"},
  {"id":"eve",   "name_s":"Eve",   "title_s":"Engineer",          "dept_s":"eng",     "status_s":"leave",   "manager_id_s":"bob"},
  {"id":"frank", "name_s":"Frank", "title_s":"Designer",          "dept_s":"design",  "status_s":"active",  "manager_id_s":"carol"}
]
```

A join finds Alice's **direct** reports — Bob and Carol, and nobody else:

```
q={!join from=id to=manager_id_s}id:alice
```

Join semantics are: run the inner query, collect values from `from`, return documents whose `to` field contains those values. One hop. Dave and Frank never appear.

The graph parser keeps walking until the frontier is empty.

## Index the org chart

These examples use Solr 10's `_default` configset. The `_s` suffix gives you indexed string fields, which the graph parser accepts. Point fields with docValues also work; analyzed text fields do not.

```bash
docker run --name solr-graph -d -p 8983:8983 solr:10.0.0 solr-precreate orgchart
until curl -sf http://localhost:8983/solr/orgchart/admin/ping >/dev/null; do sleep 1; done

curl -H 'Content-Type: application/json' \
  'http://localhost:8983/solr/orgchart/update?commit=true' \
  --data-binary '[
    {"id":"alice", "name_s":"Alice", "title_s":"CEO",                 "dept_s":"exec",   "status_s":"active"},
    {"id":"bob",   "name_s":"Bob",   "title_s":"Engineering Manager", "dept_s":"eng",    "status_s":"active", "manager_id_s":"alice"},
    {"id":"carol", "name_s":"Carol", "title_s":"Design Manager",      "dept_s":"design", "status_s":"active", "manager_id_s":"alice"},
    {"id":"dave",  "name_s":"Dave",  "title_s":"Engineer",            "dept_s":"eng",    "status_s":"active", "manager_id_s":"bob"},
    {"id":"eve",   "name_s":"Eve",   "title_s":"Engineer",            "dept_s":"eng",    "status_s":"leave",  "manager_id_s":"bob"},
    {"id":"frank", "name_s":"Frank", "title_s":"Designer",            "dept_s":"design", "status_s":"active", "manager_id_s":"carol"}
  ]'
```

## Walk down: everyone under Alice

```bash
curl -sG 'http://localhost:8983/solr/orgchart/query' \
  --data-urlencode 'fl=id,name_s,title_s,manager_id_s' \
  --data-urlencode 'sort=id asc' \
  --data-urlencode 'q={!graph from=manager_id_s to=id}id:alice'
```

That returns all six people. The parser:

1. Runs the wrapped query `id:alice` to get the root set.
2. Collects values from `to` (`id`) on the current frontier.
3. Finds documents whose `from` field (`manager_id_s`) matches those values.
4. Repeats until a hop discovers no new documents.

So the walk is: Alice → {Bob, Carol} → {Dave, Eve, Frank}. Cycles are skipped; a document already in the result set is not expanded again.

### `from` and `to` are reversed from `{!join}`

This is the detail that costs people an afternoon.

| Parser | Collect values from | Match those values on | Recurses |
|---|---|---|---|
| `{!join from=X to=Y}` | `X` | `Y` | no |
| `{!graph from=X to=Y}` | `Y` | `X` | yes |

For the org chart, the join that finds direct reports is `{!join from=id to=manager_id_s}id:alice`. The graph walk that finds the whole subtree is `{!graph from=manager_id_s to=id}id:alice`. Same two fields, opposite parameter names. The graph parser's defaults (`from=node_id`, `to=edge_ids`) match a "node identity / outgoing edges" model, which is why `to` is the field whose values you follow.

If a graph query returns only the root document, swap `from` and `to` before you debug anything else.

## Walk up: Dave's management chain

Follow `manager_id_s` instead of inverting it:

```bash
curl -sG 'http://localhost:8983/solr/orgchart/query' \
  --data-urlencode 'fl=id,name_s,title_s' \
  --data-urlencode 'sort=id asc' \
  --data-urlencode 'q={!graph from=id to=manager_id_s}id:dave'
```

Result: Dave, Bob, Alice. Same parser, opposite edge direction.

## Use it as a filter, not as the scoring query

Graph matches score as a constant `1.0`. That is the right behavior for "is this document in the subtree?" and the wrong behavior for "rank these people by title text." Production queries almost always belong in `fq`:

```bash
curl -sG 'http://localhost:8983/solr/orgchart/query' \
  --data-urlencode 'fl=id,name_s,title_s,score' \
  --data-urlencode 'q=title_s:Engineer' \
  --data-urlencode 'fq={!graph from=manager_id_s to=id}id:alice'
```

Dave and Eve match. Bob does not: his title is "Engineering Manager", and the filter only restricts the domain. Swap in `edismax` or a vector query for `q` and the graph filter still applies. This is the same pattern as any other filter query; the graph parser is just a way to *compute* that filter from edges in the index.

## Parameters worth knowing

The reference guide lists every parameter. These are the ones that change the org-chart queries above.

**`maxDepth`** — hop budget, counting the root as depth 0. `maxDepth=0` is only the root. `maxDepth=1` is the root plus one hop (Alice, Bob, Carol). Omit it, or leave the default `-1`, for an unbounded walk.

```bash
# Direct reports of Alice, including Alice
q={!graph from=manager_id_s to=id maxDepth=1}id:alice

# Direct reports only
q={!graph from=manager_id_s to=id maxDepth=1 returnRoot=false}id:alice
```

**`returnRoot`** — default `true`. Set `false` when the root is a container you do not want in the result (a VP, a parent category, a group). Combined with `maxDepth=1` this is the graph analogue of a join: one hop, same two fields, opposite `from`/`to`, root excluded.

**`traversalFilter`** — a query applied to **subsequent** hops, not to the root. To skip people on leave, and anyone reachable only through them:

```bash
q={!graph from=manager_id_s to=id traversalFilter='status_s:active'}id:alice
```

Alice is still returned (the root query is unfiltered). Eve is not. If Bob were on leave, Dave and Eve would both disappear, because the walk never enters Bob.

**`returnOnlyLeaf`** — keeps documents that have **no value in the `to` field**. That is useful when `to` is an outgoing-edge field that leaf nodes leave empty. It is *not* useful in this org chart: `to=id` is populated on every document, so the intersection is empty. Model leaves as "no outgoing edges," not as "bottom of the tree."

**`useAutn`** — default `false`. Compiling an automaton per hop may be faster for some wide frontiers. Leave it off unless you measure a gain.

## What the parser will not do

**It is not distributed.** The graph parser runs against a single shard. Standalone Solr is fine. SolrCloud is fine only when the collection has exactly one shard. On a multi-shard collection the coordinator still fans the query out; each shard walks only its local documents, and the client gets the union of those incomplete walks. Cross-shard edges are dropped with no error, which can look plausible and still be wrong. If the data has to be sharded, use [streaming `nodes()`](https://solr.apache.org/guide/solr/latest/query-guide/graph-traversal.html), which is built for distributed traversal and can span collections.

**It does not rank along the path.** There is no "closer to the root scores higher." If you need hop distance, walk with a few `maxDepth` queries, or use streaming `nodes()`, which emits a `level` field (root is 0). `scoreNodes` is a different tool: TF-IDF co-occurrence for recommendations, not path ranking.

**It is not a substitute for nested documents.** Parent/child block joins (`{!parent}` / `{!child}`) are the right tool when the relationship is physical adjacency in the index. Graph is the right tool when the relationship is *values in fields*, including cycles and variable depth.

**Wide, deep graphs are search, not a graph database.** Each hop is another query against `from`. That is fast on a subtree of tens or hundreds of thousands of nodes with a selective root. It is the wrong shape for "materialize the whole connected component of this 80-million-document corpus."

## Related tools, same edges

Solr has four ways to follow field values from one document to another. They share a mental model and do not share an implementation.

| Need | Tool |
|---|---|
| One hop, possibly across collections (`fromIndex`, `crossCollection`) | [`{!join}`](https://solr.apache.org/guide/solr/latest/query-guide/join-query-parser.html) |
| Multi-hop filter or query, single shard | [`{!graph}`](https://solr.apache.org/guide/solr/latest/query-guide/other-parsers.html#graph-query-parser) |
| Multi-hop domain for a JSON facet | [`domain: { graph: { ... } }`](https://solr.apache.org/guide/solr/latest/query-guide/json-faceting-domain-changes.html#graph-traversal-domain-changes) |
| Distributed walk, aggregations, recommendations | [streaming `nodes()`](https://solr.apache.org/guide/solr/latest/query-guide/graph-traversal.html) |

JSON faceting's graph domain takes the same `from`/`to` parameters as the query parser, including the one-shard limitation. The walk starts from the facet's current domain — here, the main query `id:alice` — and expands it before the terms facet runs:

```bash
curl -sS http://localhost:8983/solr/orgchart/query \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "id:alice",
    "facet": {
      "dept": {
        "type": "terms",
        "field": "dept_s",
        "domain": {
          "graph": {
            "from": "manager_id_s",
            "to": "id"
          }
        }
      }
    }
  }'
```

## Other graphs hiding in ordinary schemas

The org chart is one picture. The same parser covers:

- **Nested groups.** User → group → parent group. Walk `member_of` to compute the full set of groups a user inherits, then join that set against an ACL field on documents.
- **Product taxonomies.** Category → parent category. Filter a product search to "this node and every descendant."
- **Ticket / issue links.** `blocks_ss` / `depends_on_ss` with `maxDepth` to keep the walk in a neighborhood.
- **Document series.** `replaces_s` / `superseded_by_s` to find the current version or the full history.

If you can write the one-hop join, you can almost certainly write the graph walk. The extra cost is modeling the edge direction correctly and respecting the single-shard limit.

## See also

- [Graph Query Parser](https://solr.apache.org/guide/solr/latest/query-guide/other-parsers.html#graph-query-parser) in the Solr Reference Guide
- [Join Query Parser](https://solr.apache.org/guide/solr/latest/query-guide/join-query-parser.html)
- [Graph Traversal with streaming expressions](https://solr.apache.org/guide/solr/latest/query-guide/graph-traversal.html)
- [JSON Faceting: graph domain changes](https://solr.apache.org/guide/solr/latest/query-guide/json-faceting-domain-changes.html#graph-traversal-domain-changes)
