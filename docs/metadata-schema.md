# Metadata schema

Canonical machine form is YAML. Schema file: `/.omnikali-schema.yml`.

Required: `name`, `url`, `kind`, `statusTag`, `lastUpdated`.

`statusTag` is one of `PROVEN`, `OBSERVED`, `HYPOTHESIS`, `PLANNED`.

- PROVEN requires re-checkable evidence.
- OBSERVED needs a timestamp and source.
- HYPOTHESIS is the default for registry hits.
- PLANNED is not implemented capability.
