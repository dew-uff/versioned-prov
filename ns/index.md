# The Versioned-PROV namespace

The namespace name https://dew-uff.github.io/versioned-prov/ns# is intended for use with the PROV family of documents to represent Versioned-PROV extension.


## Attributes

### access

The attribute `versioned:access` in `prov:wasDerivedFrom` indicates whether the derivation was a read (`r`) or a write (`w`). The only valid values are `r` and `w`.

### key

The attribute `versioned:key` in `prov:hadMember` indicates which key/position a member represents in a collection.

The attribute `versioned:key` in `prov:wasDerivedFrom` indicates which key/position were accessed/changed from the collection represented by `versioned:whole`.

### moment

The attribute `versioned:moment` in `prov:wasDerivedFrom` indicates the moment a derivation occurred. It is required when the `prov:type` is `versioned:Reference`.

The attribute `versioned:moment` in `prov:hadMember` indicates the moment a member were inserted or removed from the a collection.

### whole

The attribute `versioned:whole` in `prov:wasDerivedFrom` indicates which entity was accesses/changed by the derivation.

## Types

### Insertion

The `versioned:Insertion` type of `prov:hadMember` indicates that a member was inserted in a collection.

### Reference

The `versioned:Reference` type of `prov:wasDerivedFrom` indicates that an entity was derived from another through a binding of a reference. Thus, both entities share the same members.

### Removal

The `versioned:Removal` type of `prov:hadMember` indicates that a member was removed from a collection.