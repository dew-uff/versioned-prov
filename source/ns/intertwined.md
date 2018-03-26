# The Intertwined-PROV namespace

The namespace name https://dew-uff.github.io/versioned-prov/ns/intertwined# is intended for use with the PROV family of documents to represent Intertwined-PROV extension.


## Attributes

### access

The attribute `intertwined:access` in `prov:wasDerivedFrom` indicates whether the derivation was a read (`r`) or a write (`w`). The only valid values are `r` and `w`.

### checkpoint

The attribute `intertwined:checkpoint` in `prov:wasDerivedFrom` indicates the moment a derivation occurred. It is required when the `prov:type` is `intertwined:Reference`.

The attribute `intertwined:checkpoint` in `prov:Entity` indicates the moment a checkpoint were created. It is required when the `prov:type` is `intertwined:Version`.

### key

The attribute `intertwined:key` in `prov:wasDerivedFrom` indicates which key/position were accessed/changed from the collection represented by `intertwined:collection`.

### collection

The attribute `intertwined:collection` in `prov:wasDerivedFrom` indicates which entity was accesses/changed by the derivation.

## Types

### Version

The `intertwined:Version` type of `prov:Entity` indicates that the entity is a version. `intertwined:Version` is a subtype of `prov:Dictionary`.

### Reference

The `intertwined:Reference` type of `prov:wasDerivedFrom` indicates that an entity was derived from another through a binding of a reference. Thus, both entities share the same members.
