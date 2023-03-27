# cs-streaming-aggregation-automation

This is an example repository which stores the streaming-aggregation config, as well as aggregation pipelines to be executed on the metrics. Feel free to fork.

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

The aggregations are stored in a file called `cluser-name.yaml' in the root of the repository.
