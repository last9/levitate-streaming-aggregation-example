# levitate-streaming-aggregation-automation

This is an example repository which stores the streaming-aggregation config, as well as aggregation pipelines to be executed on the metrics. Feel free to fork.

Read more about streaming aggregates in Levitate [here](https://docs.last9.io/docs/streaming-aggregations).

## Config file

We need to have a config file for each cluster on which we want to run out aggregations on.
This is present in [config.json](.github/workflows/config.json)

```json
{
  "clusters": {
    "cluster-name": {
      "region": "cluster-region",
      "tenant": "tenant-name",
      "cluster_id": "70fb636d-11e8-7b6a-bd3c-789b991ad626"
    }
  }
}
```

## Aggregations file

The aggregations are stored in a file called `cluser-name.yaml` in the root of the repository.

### How to define the streaming aggregated metric?

Update the `cluser-name.yaml` file with as follows:

```yaml
- promql: 'sum2 by (stack, le) (http_requests_duration_seconds_bucket{service="pushnotifs"}[1m])'
  as: aggregated_http_requests_duration_seconds_bucket
```

`promql` is the definition of the aggregated metric.
`as` is the name of the new aggregated metric available for further querying.

### Supported functions

| Function Name | Description                                |
| ------------- | ------------------------------------------ |
| sum           | Total to be used for other metric types    |
| count         | A count of the number of samples.          |
| max           | The Maximum value of the samples           |
| sum2          | Sum, but for counters and reset awareness. |
| increase      | The increase in counter value.             |
| min           | The minimum value of the samples           |
| avg           | The average value of the samples.          |
