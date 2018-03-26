# The Versioned-PROV namespace

The namespace name https://dew-uff.github.io/versioned-prov/ns# is intended for use with the PROV family of documents to represent Versioned-PROV extension.


## Attributes

### access

The attribute `version:access` in `prov:wasDerivedFrom` indicates whether the derivation was a read (`r`) or a write (`w`). The only valid values are `r` and `w`.

### checkpoint

The attribute `version:checkpoint` in `prov:wasDerivedFrom` indicates the moment a derivation occurred. It is required when the `prov:type` is `version:Reference`.

The attribute `version:checkpoint` in `prov:hadMember` indicates the moment a member were inserted or removed from the a collection.

The checkpoint can be any sortable data type (e.g., datetime, int), but it has to be consistent across all the document.

### key

The attribute `version:key` in `prov:hadMember` indicates which key/position a member represents in a collection.

The attribute `version:key` in `prov:wasDerivedFrom` indicates which key/position were accessed/changed from the collection represented by `version:collection`.

### collection

The attribute `version:collection` in `prov:wasDerivedFrom` indicates which entity was accesses/changed by the derivation.

## Types

### Add

The `version:Add` type of `prov:hadMember` indicates that a member was inserted into a list/set collection at a given checkpoint.
If `prov:hadMember` has a `version:key`, it shifts all keys that occur after the inserted `version:key`. Otherwise, it adds the element at the end of the collection.

### Del

The `version:Add` type of `prov:hadMember` indicates that a member was removed from a collection at a given checkpoint.
If a `version:key` is provided, it shifts all keys that occur after it.

### Put

The `version:Put` type of `prov:hadMember` indicates that a member was added or deleted from a collection in a given `version:key` at a given `version:checkpoint`. If the member is a placeholder or a VoidEntity, it means that the member at the specific `version:key` position was removed.

### Reference

The `version:Reference` type of `prov:wasDerivedFrom` indicates that an entity was derived from another through a binding of a reference. Thus, both entities share the same members.

### VoidEntity

The `version:VoidEntity` type of `prov:entity` represents an empty entity that can be used as member of `prov:hadMember` with type `version:Put` to remove elements from a collection.